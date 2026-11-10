"""Unit tests for active dataset curation and export utility."""
import json
from pathlib import Path
import cv2
import numpy as np
import pytest
import yaml

from src.storage.dataset_exporter import DatasetExporter, ExportSummary
from src.storage.repository import CrossingRecord, EventRepository


@pytest.fixture
def populated_db_and_images(tmp_path: Path):
    """Fixture creating mock SQLite events and associated dummy crop images."""
    db_path = tmp_path / "test_events.db"
    images_dir = tmp_path / "crops"
    images_dir.mkdir(parents=True)

    repo = EventRepository(db_path=str(db_path))
    repo.initialize()

    # Create dummy crop image: 100 x 200 (H=100, W=200)
    img = np.full((100, 200, 3), 150, dtype=np.uint8)

    # 1. Event with 2 detected sneakers
    p1 = images_dir / "crop_1.jpg"
    cv2.imwrite(str(p1), img)
    # Box 1: [20, 10, 60, 50] (x1, y1, x2, y2) -> W=40, H=40, cx=40/200=0.20, cy=30/100=0.30, w=40/200=0.20, h=40/100=0.40
    # Box 2: [100, 20, 180, 80] -> W=80, H=60, cx=140/200=0.70, cy=50/100=0.50, w=80/200=0.40, h=60/100=0.60
    bboxes1 = [
        {"box": [20.0, 10.0, 60.0, 50.0], "confidence": 0.85},
        {"box": [100.0, 20.0, 180.0, 80.0], "confidence": 0.72},
    ]
    repo.insert_event(
        CrossingRecord(
            timestamp="2026-11-10T19:00:01",
            track_id=1,
            direction="A_TO_B",
            shoes_detected=True,
            shoe_count=2,
            max_confidence=0.85,
            bboxes_json=json.dumps(bboxes1),
            full_image_path="",
            crop_image_path=str(p1),
        )
    )

    # 2. Event with 0 detected sneakers (negative sample)
    p2 = images_dir / "crop_2.jpg"
    cv2.imwrite(str(p2), img)
    repo.insert_event(
        CrossingRecord(
            timestamp="2026-11-10T19:00:02",
            track_id=2,
            direction="A_TO_B",
            shoes_detected=False,
            shoe_count=0,
            max_confidence=None,
            bboxes_json="[]",
            full_image_path="",
            crop_image_path=str(p2),
        )
    )

    return db_path, tmp_path / "yolo_export"


def test_dataset_exporter_creates_yolo_structure_and_labels(populated_db_and_images):
    """Test exporting dataset from SQLite creates standard YOLO directory format and labels."""
    db_path, export_dir = populated_db_and_images

    exporter = DatasetExporter(db_path=str(db_path), output_dir=str(export_dir))
    summary = exporter.export(train_ratio=1.0)  # All to train split for determinism

    assert isinstance(summary, ExportSummary)
    assert summary.total_exported == 2
    assert summary.train_count == 2
    assert summary.val_count == 0

    # Verify directory structure
    assert (export_dir / "images" / "train").exists()
    assert (export_dir / "labels" / "train").exists()
    assert (export_dir / "data.yaml").exists()

    # Verify data.yaml content
    with open(export_dir / "data.yaml", "r") as f:
        config = yaml.safe_load(f)
    assert config["names"][0] == "sneaker"
    assert "images/train" in config["train"]

    # Verify positive label content (YOLO normalized format)
    label_file_1 = export_dir / "labels" / "train" / "crop_1.txt"
    assert label_file_1.exists()
    lines = label_file_1.read_text().strip().split("\n")
    assert len(lines) == 2

    # Check first box: class 0, cx=0.20, cy=0.30, w=0.20, h=0.40
    cls, cx, cy, w, h = map(float, lines[0].split())
    assert int(cls) == 0
    assert cx == pytest.approx(0.20, abs=1e-3)
    assert cy == pytest.approx(0.30, abs=1e-3)
    assert w == pytest.approx(0.20, abs=1e-3)
    assert h == pytest.approx(0.40, abs=1e-3)

    # Verify negative sample label exists and is empty
    label_file_2 = export_dir / "labels" / "train" / "crop_2.txt"
    assert label_file_2.exists()
    assert label_file_2.read_text().strip() == ""
