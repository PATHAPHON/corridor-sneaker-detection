"""Two-stage decoupled video capture and processing pipeline coordinator."""
from dataclasses import dataclass
from datetime import datetime
import json
import logging
import queue
import threading
import time
from typing import Callable, List, Optional
import cv2
import numpy as np

from src.capture.base import FrameSource
from src.config.settings import PipelineConfig
from src.footwear.inspector import FootwearInspectionResult, FootwearInspector
from src.footwear.roi import extract_lower_body_roi
from src.pipeline.hud import PipelineHud
from src.storage.evidence_writer import EvidenceWriter
from src.storage.repository import CrossingRecord, EventRepository
from src.tracking.person_tracker import PersonTracker
from src.tripwire.zone import TripwireCrossing, TripwireZone

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CrossingTask:
    """Inter-thread work item dispatched to the background worker."""
    frame_id: int
    timestamp: float
    frame: np.ndarray
    crossing: TripwireCrossing


@dataclass(frozen=True)
class ProcessedCrossingEvent:
    """Completed crossing event inspected by the background worker."""
    track_id: int
    timestamp: float
    frame: np.ndarray
    roi_crop: np.ndarray
    inspection: FootwearInspectionResult
    record_id: Optional[int] = None
    full_image_path: Optional[str] = None
    crop_image_path: Optional[str] = None


class PipelineCoordinator:
    """Decoupled coordinator running lightweight capture and background inspection."""

    def __init__(
        self,
        frame_source: FrameSource,
        config: Optional[PipelineConfig] = None,
        tracker: Optional[object] = None,
        tripwire: Optional[object] = None,
        inspector: Optional[object] = None,
        repository: Optional[EventRepository] = None,
        evidence_writer: Optional[EvidenceWriter] = None,
        on_event_processed: Optional[Callable[[ProcessedCrossingEvent], None]] = None,
        show_preview: bool = False,
        window_name: str = "Pedestrian Footwear Monitoring",
    ) -> None:
        self.frame_source = frame_source
        self.config = config or PipelineConfig()
        self.on_event_processed = on_event_processed
        self.show_preview = show_preview
        self.window_name = window_name

        # Determine tripwire endpoints (Lateral Side View default per ADR-0005: vertical center line)
        src_w = getattr(self.frame_source, "width", 1920) or 1920
        src_h = getattr(self.frame_source, "height", 1080) or 1080
        cx = int(src_w // 2)
        tripwire_start = self.config.tripwire_start or (cx, 0)
        tripwire_end = self.config.tripwire_end or (cx, src_h)

        # Lazy initialize components if not injected
        self.tracker = tracker or PersonTracker(
            model_path=self.config.person_model_path,
            confidence_threshold=self.config.person_confidence,
            tracker_config=self.config.tracker_config,
            device=self.config.device,
        )
        self.tripwire = tripwire or TripwireZone(
            start=tripwire_start,
            end=tripwire_end,
            cooldown_seconds=self.config.tripwire_cooldown_seconds,
        )
        self.inspector = inspector or FootwearInspector(
            model_path=self.config.sneaker_model_path,
            confidence_threshold=self.config.sneaker_confidence,
            device=self.config.device,
        )
        self.hud = PipelineHud(
            tripwire_start=tripwire_start,
            tripwire_end=tripwire_end,
        )

        # Storage & Evidence Persistence per ADR-0004
        self.repository = repository
        self.evidence_writer = evidence_writer
        if self.config.enable_storage:
            if self.repository is None:
                self.repository = EventRepository(db_path=self.config.db_path)
                self.repository.initialize()
            if self.evidence_writer is None:
                self.evidence_writer = EvidenceWriter(base_dir=self.config.capture_dir)

        # Bounded event queue per Invariant 2 (maxsize=20)
        self.event_queue: queue.Queue = queue.Queue(maxsize=self.config.queue_maxsize)
        self.dropped_events_count = 0
        self.crossing_counter = 0

        self._stop_event = threading.Event()
        self._worker_thread: Optional[threading.Thread] = None

    def enqueue_crossing(self, task: CrossingTask) -> bool:
        """Enqueue crossing task without blocking the capture loop.

        Returns:
            True if enqueued successfully, False if queue was full (dropped).
        """
        try:
            self.event_queue.put_nowait(task)
            return True
        except queue.Full:
            self.dropped_events_count += 1
            logger.warning(
                "Event queue full (capacity %d). Dropped crossing event for track %d.",
                self.config.queue_maxsize,
                task.crossing.track_id,
            )
            return False

    def _worker_loop(self) -> None:
        """Background worker thread consuming crossing tasks."""
        while not self._stop_event.is_set() or not self.event_queue.empty():
            try:
                task = self.event_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            if task is None:  # Sentinel shutdown
                self.event_queue.task_done()
                break

            try:
                # 1. Extract lower-body ROI
                roi = extract_lower_body_roi(task.frame, task.crossing.box)

                # 2. Execute sneaker inference
                inspection = self.inspector.inspect(roi.crop)

                # 3. Persist visual evidence and SQLite record if storage enabled
                record_id = None
                full_image_path = None
                crop_image_path = None

                if self.config.enable_storage and self.evidence_writer and self.repository:
                    self.crossing_counter += 1
                    now = datetime.now()
                    if task.timestamp > 1_000_000_000:
                        iso_timestamp = datetime.fromtimestamp(task.timestamp).strftime("%Y-%m-%d %H:%M:%S.%f")
                    else:
                        iso_timestamp = now.strftime("%Y-%m-%d %H:%M:%S.%f")

                    saved_paths = self.evidence_writer.save_evidence(
                        timestamp=iso_timestamp,
                        track_id=task.crossing.track_id,
                        full_frame=task.frame,
                        roi_crop=roi.crop,
                        boxes=inspection.boxes,
                        confidences=inspection.confidences,
                        event_id=self.crossing_counter,
                    )
                    full_image_path = saved_paths.full_image_path
                    crop_image_path = saved_paths.crop_image_path

                    bboxes_list = [
                        {"box": [float(coord) for coord in b], "confidence": float(c)}
                        for b, c in zip(inspection.boxes, inspection.confidences)
                    ] if inspection.boxes is not None else []

                    record = CrossingRecord(
                        timestamp=iso_timestamp,
                        track_id=task.crossing.track_id,
                        direction=task.crossing.direction,
                        shoes_detected=inspection.shoes_detected,
                        shoe_count=inspection.sneaker_count,
                        max_confidence=max(inspection.confidences) if inspection.confidences else None,
                        bboxes_json=json.dumps(bboxes_list),
                        full_image_path=full_image_path,
                        crop_image_path=crop_image_path,
                    )
                    record_id = self.repository.insert_event(record)

                # 4. Assemble processed event
                event = ProcessedCrossingEvent(
                    track_id=task.crossing.track_id,
                    timestamp=task.timestamp,
                    frame=task.frame,
                    roi_crop=roi.crop,
                    inspection=inspection,
                    record_id=record_id,
                    full_image_path=full_image_path,
                    crop_image_path=crop_image_path,
                )

                # 5. Trigger HUD visual alert
                status_msg = (
                    f"Track #{event.track_id}: SNEAKERS DETECTED ({inspection.sneaker_count})"
                    if inspection.shoes_detected
                    else f"Track #{event.track_id}: NO SNEAKERS DETECTED"
                )
                self.hud.trigger_alert(status_msg, is_compliant=inspection.shoes_detected)

                # 5. Dispatch callback if registered
                if self.on_event_processed:
                    self.on_event_processed(event)

            except Exception as e:
                logger.error("Error processing crossing task: %s", e, exc_info=True)
            finally:
                self.event_queue.task_done()

    def start_worker(self) -> None:
        """Start the background worker thread."""
        self._stop_event.clear()
        self._worker_thread = threading.Thread(
            target=self._worker_loop,
            name="SneakerWorkerThread",
            daemon=True,
        )
        self._worker_thread.start()

    def stop_worker(self) -> None:
        """Stop worker and drain remaining queued items."""
        self._stop_event.set()
        # Enqueue sentinel to unblock worker if waiting
        try:
            self.event_queue.put_nowait(None)
        except queue.Full:
            pass

        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=5.0)

    def reset_tracking(self) -> None:
        """Reset person tracker IDs and tripwire cooldowns."""
        if hasattr(self.tracker, "reset"):
            self.tracker.reset()
        if hasattr(self.tripwire, "reset"):
            self.tripwire.reset()
        self.hud.trigger_alert("TRACKING & IDs RESET", is_compliant=True)
        logger.info("Tracking reset: Track IDs and cooldowns restarted to 1.")

    def run(self) -> None:
        """Execute the real-time capture and tracking loop."""
        self.start_worker()

        prev_time = time.time()
        fps = 30.0

        try:
            for frame_id, timestamp, frame in self.frame_source.stream():
                if self._stop_event.is_set():
                    break

                curr_time = time.time()
                dt = curr_time - prev_time
                if dt > 0:
                    fps = 0.9 * fps + 0.1 * (1.0 / dt)
                prev_time = curr_time

                # Lightweight tracking and crossing in main loop
                tracked = self.tracker.process_frame(frame)
                crossings = self.tripwire.update(tracked, timestamp)

                # Dispatch heavy work to background worker
                for crossing in crossings:
                    task = CrossingTask(
                        frame_id=frame_id,
                        timestamp=timestamp,
                        frame=frame.copy(),
                        crossing=crossing,
                    )
                    self.enqueue_crossing(task)

                # Real-time visual GUI preview
                if self.show_preview:
                    display_frame = self.hud.render(
                        frame=frame,
                        tracked_people=tracked,
                        fps=fps,
                        queue_size=self.event_queue.qsize(),
                    )
                    cv2.imshow(self.window_name, display_frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord("q") or key == 27:  # 'q' or ESC
                        logger.info("Exit key pressed. Stopping preview...")
                        self._stop_event.set()
                        break
                    elif key == ord("r"):
                        self.reset_tracking()
        finally:
            if self.show_preview:
                cv2.destroyAllWindows()
            self.stop_worker()
            self.frame_source.close()
