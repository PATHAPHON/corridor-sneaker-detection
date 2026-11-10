"""Integration tests for end-to-end pipeline storage persistence."""
from pathlib import Path
import pytest
import numpy as np

from src.capture.synthetic import SyntheticFrameSource
from src.config.settings import PipelineConfig
from src.pipeline.coordinator import PipelineCoordinator, CrossingTask
from src.storage.repository import EventRepository
from src.storage.evidence_writer import EvidenceWriter
from src.tripwire.zone import TripwireCrossing


def test_coordinator_worker_persists_event_and_evidence(tmp_path: Path):
    """Test background worker automatically persists crossing event to SQLite and disk."""
    db_file = tmp_path / "test_events.db"
    capture_dir = tmp_path / "captures"

    config = PipelineConfig(
        enable_storage=True,
        db_path=str(db_file),
        capture_dir=str(capture_dir),
    )

    frame_source = SyntheticFrameSource(total_frames=5, simulate_wall_clock=False)
    coordinator = PipelineCoordinator(
        frame_source=frame_source,
        config=config,
        show_preview=False,
    )

    # Start worker thread
    coordinator.start_worker()

    # Create dummy frame and crossing task
    frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    crossing = TripwireCrossing(
        track_id=101,
        timestamp=1.23,
        direction="A_TO_B",
        box=np.array([500, 200, 780, 700], dtype=np.float32),
        anchor_point=(640, 700),
    )
    task = CrossingTask(
        frame_id=1,
        timestamp=1.23,
        frame=frame,
        crossing=crossing,
    )

    # Enqueue crossing
    success = coordinator.enqueue_crossing(task)
    assert success is True

    # Stop worker and drain queue
    coordinator.stop_worker()

    # Verify SQLite record persisted
    repo = EventRepository(db_path=str(db_file))
    events = repo.get_events_by_track(track_id=101)
    assert len(events) == 1
    event = events[0]
    assert event.track_id == 101
    assert event.direction == "A_TO_B"
    assert Path(event.full_image_path).exists()
    assert Path(event.crop_image_path).exists()
