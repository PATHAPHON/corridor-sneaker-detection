import queue
import threading
import time
from typing import List
import numpy as np
import pytest

from src.capture.synthetic import SyntheticFrameSource
from src.config.settings import PipelineConfig
from src.footwear.inspector import FootwearInspectionResult, FootwearInspector
from src.pipeline.coordinator import CrossingTask, PipelineCoordinator, ProcessedCrossingEvent
from src.tracking.person_tracker import PersonTracker, TrackedPerson
from src.tripwire.zone import TripwireCrossing, TripwireZone


class MockTracker:
    """Mock tracker that outputs deterministic pedestrian movement across the tripwire."""

    def __init__(self):
        self.frame_idx = 0

    def process_frame(self, frame: np.ndarray) -> List[TrackedPerson]:
        self.frame_idx += 1
        # Frame 1: Person in Zone A (y=100)
        # Frame 2: Person in Zone B (y=300) -> crosses line at y=200
        # Frame 3: Person in Zone B (y=320)
        if self.frame_idx == 1:
            return [TrackedPerson(track_id=1, box=(100, 50, 150, 100), confidence=0.9, anchor_point=(125, 100))]
        elif self.frame_idx == 2:
            return [TrackedPerson(track_id=1, box=(100, 250, 150, 300), confidence=0.9, anchor_point=(125, 300))]
        elif self.frame_idx == 3:
            return [TrackedPerson(track_id=1, box=(100, 270, 150, 320), confidence=0.9, anchor_point=(125, 320))]
        return []


class MockInspector:
    """Mock footwear inspector."""

    def inspect(self, crop: np.ndarray) -> FootwearInspectionResult:
        return FootwearInspectionResult(
            shoes_detected=True,
            sneaker_count=2,
            boxes=[(10.0, 10.0, 40.0, 30.0), (50.0, 10.0, 80.0, 30.0)],
            confidences=[0.92, 0.89],
        )


def test_pipeline_bounded_queue_invariant():
    """Inter-stage event queue must enforce maxsize=20 and drop on full without blocking."""
    config = PipelineConfig(queue_maxsize=20)
    coordinator = PipelineCoordinator(
        frame_source=SyntheticFrameSource(total_frames=1),
        config=config,
    )
    assert coordinator.event_queue.maxsize == 20

    # Fill the queue to capacity
    dummy_task = CrossingTask(
        frame_id=0,
        timestamp=0.0,
        frame=np.zeros((10, 10, 3), dtype=np.uint8),
        crossing=TripwireCrossing(track_id=1, timestamp=0.0, direction="ENTRY", box=(0, 0, 10, 10), anchor_point=(5, 10)),
    )
    for _ in range(20):
        coordinator.enqueue_crossing(dummy_task)

    assert coordinator.event_queue.full()

    # Attempting to enqueue 21st task must NOT block and must gracefully drop
    dropped = coordinator.enqueue_crossing(dummy_task)
    assert dropped is False
    assert coordinator.dropped_events_count == 1


def test_pipeline_end_to_end_integration():
    """PipelineCoordinator should run capture, tracking, crossing, and worker inspection end-to-end."""
    config = PipelineConfig(
        tripwire_start=(0, 200),
        tripwire_end=(600, 200),
        tripwire_cooldown_seconds=2.0,
        queue_maxsize=20,
    )

    frame_source = SyntheticFrameSource(width=600, height=400, fps=30.0, total_frames=3)
    mock_tracker = MockTracker()
    tripwire = TripwireZone(start=config.tripwire_start, end=config.tripwire_end, cooldown_seconds=config.tripwire_cooldown_seconds)
    mock_inspector = MockInspector()

    processed_events: List[ProcessedCrossingEvent] = []

    coordinator = PipelineCoordinator(
        frame_source=frame_source,
        config=config,
        tracker=mock_tracker,
        tripwire=tripwire,
        inspector=mock_inspector,
        on_event_processed=lambda ev: processed_events.append(ev),
    )

    # Run pipeline to completion
    coordinator.run()

    # Verify that exactly 1 crossing event was detected and processed by the worker
    assert len(processed_events) == 1
    event = processed_events[0]
    assert event.track_id == 1
    assert event.inspection.shoes_detected is True
    assert event.inspection.sneaker_count == 2
    assert event.roi_crop.shape[0] > 0
    assert event.roi_crop.shape[1] > 0


class MockLateralTracker:
    """Simulates a pedestrian walking horizontally past the camera (Lateral Side View)."""

    def __init__(self):
        self.frame_idx = 0

    def process_frame(self, frame: np.ndarray) -> List[TrackedPerson]:
        self.frame_idx += 1
        # Vertical line at x=300 (width=600, height=400)
        # Frame 1: Person on Left (x_anchor=150)
        # Frame 2: Person crosses to Right (x_anchor=400)
        # Frame 3: Person continues on Right (x_anchor=450)
        if self.frame_idx == 1:
            return [TrackedPerson(track_id=7, box=(100, 100, 200, 380), confidence=0.95, anchor_point=(150, 380))]
        elif self.frame_idx == 2:
            return [TrackedPerson(track_id=7, box=(350, 100, 450, 380), confidence=0.95, anchor_point=(400, 380))]
        elif self.frame_idx == 3:
            return [TrackedPerson(track_id=7, box=(400, 100, 500, 380), confidence=0.95, anchor_point=(450, 380))]
        return []


def test_pipeline_lateral_side_view_end_to_end_integration():
    """PipelineCoordinator should automatically configure vertical line for lateral side view."""
    # Omit tripwire_start/end so it defaults to vertical bisector (x=300 in 600x400)
    config = PipelineConfig(
        tripwire_cooldown_seconds=2.0,
        queue_maxsize=20,
    )

    frame_source = SyntheticFrameSource(width=600, height=400, fps=30.0, total_frames=3)
    mock_tracker = MockLateralTracker()
    mock_inspector = MockInspector()

    processed_events: List[ProcessedCrossingEvent] = []

    coordinator = PipelineCoordinator(
        frame_source=frame_source,
        config=config,
        tracker=mock_tracker,
        inspector=mock_inspector,
        on_event_processed=lambda ev: processed_events.append(ev),
    )

    coordinator.run()

    assert len(processed_events) == 1
    event = processed_events[0]
    assert event.track_id == 7
    assert event.inspection.shoes_detected is True
    assert event.roi_crop.shape[0] > 0
    assert event.roi_crop.shape[1] > 0
