"""Person detector and ByteTrack multi-object tracking module."""
from dataclasses import dataclass
import logging
from typing import List, Optional, Tuple
import numpy as np
import supervision as sv
import torch
from ultralytics import YOLO

from src.tracking.anchor import calculate_ground_anchor_point

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TrackedPerson:
    """Immutable representation of a tracked pedestrian in a video frame."""
    track_id: int
    box: Tuple[float, float, float, float]
    confidence: float
    anchor_point: Tuple[float, float]


def get_default_device() -> str:
    """Auto-detect optimal hardware acceleration device."""
    if torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


class PersonTracker:
    """Detects persons using YOLO11n and tracks them across frames via ByteTrack."""

    def __init__(
        self,
        model_path: str = "yolo11n.pt",
        confidence_threshold: float = 0.50,
        tracker_config: str = "src/config/bytetrack.yaml",
        device: Optional[str] = None,
    ) -> None:
        self.device = device if device is not None else get_default_device()
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.tracker_config = tracker_config
        self.model = YOLO(model_path)
        self.reset()

    def reset(self) -> None:
        """Reset ByteTrack tracker IDs and clear tracker predictor state."""
        try:
            from ultralytics.trackers.byte_tracker import STrack
            STrack.reset_id()
            logger.debug("ByteTrack STrack IDs successfully reset to 0.")
        except Exception as e:
            logger.debug("Failed to reset STrack ID: %s", e)

        if hasattr(self.model, "predictor") and self.model.predictor is not None:
            self.model.predictor.trackers = []

    def process_frame(self, frame: np.ndarray) -> List[TrackedPerson]:
        """Detect and track persons in a single frame.

        Args:
            frame: BGR numpy image frame.

        Returns:
            List of TrackedPerson objects with active track IDs and ground anchors.
        """
        results = self.model.track(
            source=frame,
            persist=True,
            tracker=self.tracker_config,
            classes=[0],
            conf=self.confidence_threshold,
            device=self.device,
            verbose=False,
        )

        if not results:
            return []

        detections = sv.Detections.from_ultralytics(results[0])

        tracked_people: List[TrackedPerson] = []
        if len(detections.xyxy) == 0 or detections.tracker_id is None:
            return tracked_people

        for i in range(len(detections.xyxy)):
            track_id = int(detections.tracker_id[i])

            box_arr = detections.xyxy[i]
            box: Tuple[float, float, float, float] = (
                float(box_arr[0]),
                float(box_arr[1]),
                float(box_arr[2]),
                float(box_arr[3]),
            )
            conf = (
                float(detections.confidence[i])
                if detections.confidence is not None
                else 1.0
            )
            anchor = calculate_ground_anchor_point(box)

            tracked_people.append(
                TrackedPerson(
                    track_id=track_id,
                    box=box,
                    confidence=conf,
                    anchor_point=anchor,
                )
            )

        return tracked_people
