"""Unit tests for dual-gate evaluation, auto-backup, and Before/After reporting."""

from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from scripts.evaluate_and_export import evaluate_and_export, evaluate_hallway_crops


def test_evaluate_hallway_crops_computes_recall(tmp_path: Path):
    """Verify hallway crop evaluation calculates ground-truth recall correctly."""
    live_dir = tmp_path / "live"
    img_dir = live_dir / "images" / "train"
    lbl_dir = live_dir / "labels" / "train"
    img_dir.mkdir(parents=True)
    lbl_dir.mkdir(parents=True)

    # 1 image with 2 sneakers
    img = img_dir / "hallway_1.jpg"
    import cv2
    import numpy as np
    cv2.imwrite(str(img), np.zeros((100, 100, 3), dtype=np.uint8))
    lbl = lbl_dir / "hallway_1.txt"
    lbl.write_text("0 0.4 0.8 0.2 0.2\n0 0.6 0.8 0.2 0.2\n")

    mock_model = MagicMock()
    # Mock detection returning 2 matching boxes
    mock_box1 = MagicMock()
    mock_box1.xyxy = [[30, 70, 50, 90]]
    mock_box1.conf = [0.85]
    mock_box1.cls = [0]

    mock_box2 = MagicMock()
    mock_box2.xyxy = [[50, 70, 70, 90]]
    mock_box2.conf = [0.82]
    mock_box2.cls = [0]

    mock_res = MagicMock()
    mock_res.boxes = [mock_box1, mock_box2]
    mock_res.orig_shape = (100, 100)
    mock_model.return_value = [mock_res]

    stats = evaluate_hallway_crops(mock_model, hallway_dir=live_dir, device="cpu", conf=0.40)
    assert stats["total_gt_boxes"] == 2
    assert stats["detected_boxes"] == 2
    assert stats["recall"] == 1.0


def test_evaluate_and_export_aborts_when_gate_fails(tmp_path: Path):
    """Verify that export aborts and does not overwrite model when gate fails."""
    weights = tmp_path / "best.pt"
    weights.write_bytes(b"candidate-weights")

    data_yaml = tmp_path / "data.yaml"
    data_yaml.write_text("train: train.txt\nval: val.txt\nnames: {0: sneaker}\n")

    export_target = tmp_path / "models" / "yolo-sneaker.pt"
    export_target.parent.mkdir(parents=True)
    export_target.write_bytes(b"original-production-weights")

    with patch("scripts.evaluate_and_export.YOLO") as mock_yolo:
        mock_instance = MagicMock()
        # Mock mAP50 = 0.65 (< 0.80)
        mock_val = MagicMock()
        mock_val.box.map50 = 0.65
        mock_val.box.map = 0.45
        mock_val.box.p = [0.70]
        mock_val.box.r = [0.60]
        mock_instance.val.return_value = mock_val
        mock_yolo.return_value = mock_instance

        with pytest.raises(RuntimeError, match="Dual-gate benchmark check failed"):
            evaluate_and_export(
                weights_path=weights,
                data_yaml=data_yaml,
                export_dest=export_target,
                min_map50=0.80,
                device="cpu",
                output_evidence_dir=tmp_path / "eval",
            )

        # Original weights MUST be preserved untouched
        assert export_target.read_bytes() == b"original-production-weights"
        backup_file = export_target.with_name("yolo-sneaker.backup.pt")
        assert not backup_file.exists()


def test_evaluate_and_export_promotes_and_backs_up_on_success(tmp_path: Path):
    """Verify that export creates backup and promotes weights when both gates pass."""
    weights = tmp_path / "best.pt"
    weights.write_bytes(b"candidate-weights")

    data_yaml = tmp_path / "data.yaml"
    data_yaml.write_text("train: train.txt\nval: val.txt\nnames: {0: sneaker}\n")

    export_target = tmp_path / "models" / "yolo-sneaker.pt"
    export_target.parent.mkdir(parents=True)
    export_target.write_bytes(b"original-production-weights")

    with patch("scripts.evaluate_and_export.YOLO") as mock_yolo, \
         patch("scripts.evaluate_and_export.evaluate_hallway_crops") as mock_hallway, \
         patch("scripts.evaluate_and_export.render_before_after_comparisons") as mock_render:

        mock_instance = MagicMock()
        mock_val = MagicMock()
        mock_val.box.map50 = 0.88
        mock_val.box.map = 0.65
        mock_val.box.p = [0.91]
        mock_val.box.r = [0.89]
        mock_instance.val.return_value = mock_val
        mock_yolo.return_value = mock_instance

        mock_hallway.return_value = {
            "total_images": 13,
            "total_gt_boxes": 26,
            "detected_boxes": 25,
            "recall": 0.96,
            "mean_conf": 0.82,
        }
        mock_render.return_value = ["fake_comparison.jpg"]

        summary = evaluate_and_export(
            weights_path=weights,
            data_yaml=data_yaml,
            export_dest=export_target,
            min_map50=0.80,
            min_hallway_recall=0.90,
            device="cpu",
            output_evidence_dir=tmp_path / "eval",
        )

        assert summary["gates"]["passed"] is True
        # Backup created
        backup_file = export_target.with_name("yolo-sneaker.backup.pt")
        assert backup_file.is_file()
        assert backup_file.read_bytes() == b"original-production-weights"
        # Export promoted
        assert export_target.read_bytes() == b"candidate-weights"
