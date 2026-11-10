import numpy as np
import pytest
import torch
from unittest.mock import MagicMock, patch

from src.footwear.roi import extract_lower_body_roi, LowerBodyRoi
from src.footwear.inspector import FootwearInspector, FootwearInspectionResult


def test_extract_lower_body_roi_exact_formula():
    """Verify ROI formula: bottom 30% height, 10% horizontal padding on each side."""
    frame = np.zeros((1000, 1000, 3), dtype=np.uint8)
    # Box: x_min=200, y_min=100, x_max=400, y_max=600
    # width = 200, height = 500
    # 30% height = 150 -> y_roi_top = 600 - 150 = 450, y_roi_bottom = 600
    # 10% width = 20 -> x_roi_left = 200 - 20 = 180, x_roi_right = 400 + 20 = 420
    box = (200.0, 100.0, 400.0, 600.0)

    roi = extract_lower_body_roi(frame, box)
    assert roi.roi_box == (180, 450, 420, 600)
    assert roi.crop.shape == (150, 240, 3)


def test_extract_lower_body_roi_boundary_clamping():
    """Verify ROI coordinates clamp strictly to frame dimensions (0 to W/H)."""
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    # Box touching left and bottom boundaries: x_min=5, y_min=200, x_max=100, y_max=480
    box = (5.0, 200.0, 100.0, 480.0)

    roi = extract_lower_body_roi(frame, box)
    # x_roi_left = max(0, 5 - 9.5) = 0
    # y_roi_bottom = min(480, 480) = 480
    assert roi.roi_box[0] == 0
    assert roi.roi_box[3] == 480
    assert roi.crop.shape[0] > 0
    assert roi.crop.shape[1] > 0


def test_footwear_inspector_positive_detection():
    """FootwearInspector should report shoes_detected=True when sneaker >= threshold."""
    with patch("src.footwear.inspector.YOLO") as mock_yolo_cls:
        mock_model = MagicMock()
        mock_yolo_cls.return_value = mock_model

        inspector = FootwearInspector(
            model_path="models/yolo-sneaker.pt",
            confidence_threshold=0.40,
            device="cpu",
        )

        crop = np.zeros((150, 240, 3), dtype=np.uint8)

        mock_box1 = MagicMock()
        mock_box1.cls = [torch.tensor(0.0)]
        mock_box1.conf = [torch.tensor(0.88)]
        mock_box1.xyxy = [torch.tensor([20.0, 50.0, 100.0, 120.0])]

        mock_box2 = MagicMock()
        mock_box2.cls = [torch.tensor(0.0)]
        mock_box2.conf = [torch.tensor(0.75)]
        mock_box2.xyxy = [torch.tensor([120.0, 55.0, 210.0, 125.0])]

        mock_results = MagicMock()
        mock_results.boxes = [mock_box1, mock_box2]
        mock_model.return_value = [mock_results]

        result = inspector.inspect(crop)

        assert result.shoes_detected is True
        assert result.sneaker_count == 2
        assert len(result.boxes) == 2
        assert result.confidences == pytest.approx([0.88, 0.75])


def test_footwear_inspector_negative_detection():
    """FootwearInspector should report shoes_detected=False when no sneaker meets threshold."""
    with patch("src.footwear.inspector.YOLO") as mock_yolo_cls:
        mock_model = MagicMock()
        mock_yolo_cls.return_value = mock_model

        inspector = FootwearInspector(
            model_path="models/yolo-sneaker.pt",
            confidence_threshold=0.40,
            device="cpu",
        )

        crop = np.zeros((150, 240, 3), dtype=np.uint8)

        # Low confidence box below 0.40
        mock_box = MagicMock()
        mock_box.cls = [torch.tensor(0.0)]
        mock_box.conf = [torch.tensor(0.25)]
        mock_box.xyxy = [torch.tensor([10.0, 20.0, 50.0, 60.0])]

        mock_results = MagicMock()
        mock_results.boxes = [mock_box]
        mock_model.return_value = [mock_results]

        result = inspector.inspect(crop)

        assert result.shoes_detected is False
        assert result.sneaker_count == 0
        assert len(result.boxes) == 0
