"""Unit tests for date-partitioned visual evidence filesystem writer."""
from pathlib import Path
import cv2
import numpy as np
import pytest

from src.storage.evidence_writer import EvidenceWriter, SavedEvidencePaths


@pytest.fixture
def temp_capture_dir(tmp_path: Path) -> Path:
    """Fixture providing a temporary captures directory."""
    return tmp_path / "captures"


def test_evidence_writer_creates_date_directory_and_saves_images(temp_capture_dir: Path):
    """Test saving full scene and annotated cropped feet ROI images."""
    writer = EvidenceWriter(base_dir=str(temp_capture_dir))

    full_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    roi_crop = np.full((100, 150, 3), 128, dtype=np.uint8)

    boxes = np.array([[20, 30, 80, 90]], dtype=np.float32)
    confidences = [0.88]

    timestamp_str = "2026-11-10T18-58-16.718000"
    track_id = 42

    paths = writer.save_evidence(
        timestamp=timestamp_str,
        track_id=track_id,
        full_frame=full_frame,
        roi_crop=roi_crop,
        boxes=boxes,
        confidences=confidences,
    )

    assert isinstance(paths, SavedEvidencePaths)
    assert Path(paths.full_image_path).exists()
    assert Path(paths.crop_image_path).exists()

    # Verify filenames match naming specification
    assert "2026-11-10" in paths.full_image_path
    assert f"{timestamp_str}_{track_id}_full.jpg" in paths.full_image_path
    assert f"{timestamp_str}_{track_id}_crop.jpg" in paths.crop_image_path

    # Verify readable valid JPEGs
    read_full = cv2.imread(paths.full_image_path)
    read_crop = cv2.imread(paths.crop_image_path)
    assert read_full is not None
    assert read_crop is not None
    assert read_full.shape == (480, 640, 3)
    assert read_crop.shape == (100, 150, 3)


def test_evidence_writer_handles_empty_detections(temp_capture_dir: Path):
    """Test saving evidence when no sneakers were detected."""
    writer = EvidenceWriter(base_dir=str(temp_capture_dir))

    full_frame = np.zeros((100, 100, 3), dtype=np.uint8)
    roi_crop = np.zeros((50, 50, 3), dtype=np.uint8)

    paths = writer.save_evidence(
        timestamp="2026-11-10T19-00-00.000000",
        track_id=99,
        full_frame=full_frame,
        roi_crop=roi_crop,
        boxes=np.empty((0, 4)),
        confidences=[],
    )

    assert Path(paths.full_image_path).exists()
    assert Path(paths.crop_image_path).exists()


def test_evidence_writer_with_event_id_prefix(temp_capture_dir: Path):
    """Test that event_id is formatted as a 5-digit prefix ordering files naturally."""
    writer = EvidenceWriter(base_dir=str(temp_capture_dir))
    full_frame = np.zeros((100, 100, 3), dtype=np.uint8)
    roi_crop = np.zeros((50, 50, 3), dtype=np.uint8)

    paths = writer.save_evidence(
        timestamp="2026-11-10T20-00-00.000000",
        track_id=7,
        full_frame=full_frame,
        roi_crop=roi_crop,
        event_id=42,
    )

    assert "00042_2026-11-10T20-00-00.000000_7_full.jpg" in paths.full_image_path
    assert "00042_2026-11-10T20-00-00.000000_7_crop.jpg" in paths.crop_image_path
    assert Path(paths.full_image_path).exists()
    assert Path(paths.crop_image_path).exists()


def test_evidence_writer_fallbacks_for_epoch_1970(temp_capture_dir: Path):
    """Test that relative video timestamp (1970-01-01) falls back to current date folder."""
    writer = EvidenceWriter(base_dir=str(temp_capture_dir))
    full_frame = np.zeros((100, 100, 3), dtype=np.uint8)
    roi_crop = np.zeros((50, 50, 3), dtype=np.uint8)

    paths = writer.save_evidence(
        timestamp="1970-01-01T07-01-49.335867",
        track_id=9,
        full_frame=full_frame,
        roi_crop=roi_crop,
        event_id=1,
    )

    # Must NOT put file in 1970-01-01 folder
    assert "1970-01-01" not in Path(paths.full_image_path).parent.name
    assert Path(paths.full_image_path).exists()
    assert Path(paths.crop_image_path).exists()
