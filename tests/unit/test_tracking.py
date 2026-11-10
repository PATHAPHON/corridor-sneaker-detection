import numpy as np
import pytest
from unittest.mock import MagicMock, patch

from src.tracking.anchor import calculate_ground_anchor_point
from src.tracking.person_tracker import PersonTracker, TrackedPerson


def test_calculate_ground_anchor_point_exact_formula():
    """Ground anchor point must strictly be bottom-center: ((x_min + x_max)/2, y_max)."""
    box = (100.0, 50.0, 200.0, 350.0)
    anchor = calculate_ground_anchor_point(box)
    assert anchor == (150.0, 350.0)


def test_calculate_ground_anchor_point_asymmetric():
    """Verify calculation with arbitrary bounding box float coordinates."""
    box = (10.5, 20.0, 30.5, 100.0)
    anchor = calculate_ground_anchor_point(box)
    assert anchor == (20.5, 100.0)


def test_person_tracker_detection_filtering_and_tracking():
    """PersonTracker should parse tracked detections and compute ground anchors."""
    with patch("src.tracking.person_tracker.YOLO") as mock_yolo_cls, \
         patch("src.tracking.person_tracker.sv.Detections.from_ultralytics") as mock_from_ultralytics:

        mock_model = MagicMock()
        mock_yolo_cls.return_value = mock_model

        tracker_service = PersonTracker(
            model_path="yolo11n.pt",
            confidence_threshold=0.5,
            device="cpu",
        )

        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        mock_model.track.return_value = [MagicMock()]

        # Mock supervision Detections output
        mock_detections = MagicMock()
        mock_detections.xyxy = np.array([[100.0, 100.0, 200.0, 300.0]])
        mock_detections.confidence = np.array([0.85])
        mock_detections.tracker_id = np.array([42])
        mock_from_ultralytics.return_value = mock_detections

        tracked_people = tracker_service.process_frame(frame)

        assert len(tracked_people) == 1
        person = tracked_people[0]
        assert person.track_id == 42
        assert person.confidence == pytest.approx(0.85)
        assert person.box == (100.0, 100.0, 200.0, 300.0)
        assert person.anchor_point == (150.0, 300.0)

        # Verify track was called with classes=[0] (person) and persist=True
        mock_model.track.assert_called_once_with(
            source=frame,
            persist=True,
            tracker="src/config/bytetrack.yaml",
            classes=[0],
            conf=0.5,
            device="cpu",
            verbose=False,
        )


def test_person_tracker_reset_resets_track_id():
    """Verify PersonTracker.reset() resets STrack._count and clears trackers."""
    from ultralytics.trackers.byte_tracker import STrack
    STrack.next_id()
    assert STrack._count > 0

    with patch("src.tracking.person_tracker.YOLO"):
        tracker = PersonTracker(model_path="yolo11n.pt")
        tracker.reset()
        assert STrack._count == 0


def test_person_tracker_device_auto_detection():
    """PersonTracker should auto-detect mps if available."""
    with patch("src.tracking.person_tracker.YOLO") as mock_yolo_cls, \
         patch("src.tracking.person_tracker.torch.backends.mps.is_available", return_value=True):
        tracker = PersonTracker(model_path="yolo11n.pt")
        assert tracker.device == "mps"
