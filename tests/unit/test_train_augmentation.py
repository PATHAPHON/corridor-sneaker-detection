"""Unit test for ADR-0007 training-time augmentation parameters."""

from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from scripts.train_sneaker_model import train_sneaker_model


def test_train_sneaker_model_forwards_adr0007_parameters(tmp_path: Path):
    """Verify that all ADR-0007 augmentations are forwarded to YOLO.train."""
    dummy_yaml = tmp_path / "data.yaml"
    dummy_yaml.write_text("names: {0: sneaker}\n")

    fake_save_dir = tmp_path / "runs" / "exp"
    weights_dir = fake_save_dir / "weights"
    weights_dir.mkdir(parents=True)
    best_weight = weights_dir / "best.pt"
    best_weight.write_bytes(b"model-data")

    mock_results = MagicMock()
    mock_results.save_dir = str(fake_save_dir)

    with patch("scripts.train_sneaker_model.YOLO") as mock_yolo:
        mock_instance = MagicMock()
        mock_instance.train.return_value = mock_results
        mock_yolo.return_value = mock_instance

        returned_path = train_sneaker_model(
            data_yaml=dummy_yaml,
            base_model="models/yolo-sneaker.pt",
            epochs=30,
            batch_size=8,
            imgsz=640,
            mosaic=1.0,
            scale=0.5,
            hsv_s=0.7,
            hsv_v=0.4,
            degrees=10.0,
            fliplr=0.5,
            erasing=0.2,
            close_mosaic=10,
            device="cpu",
        )

        assert returned_path == best_weight
        mock_yolo.assert_called_once_with("models/yolo-sneaker.pt")
        mock_instance.train.assert_called_once()
        _, train_kwargs = mock_instance.train.call_args

        assert train_kwargs["epochs"] == 30
        assert train_kwargs["batch"] == 8
        assert train_kwargs["mosaic"] == 1.0
        assert train_kwargs["scale"] == 0.5
        assert train_kwargs["hsv_s"] == 0.7
        assert train_kwargs["hsv_v"] == 0.4
        assert train_kwargs["degrees"] == 10.0
        assert train_kwargs["fliplr"] == 0.5
        assert train_kwargs["erasing"] == 0.2
        assert train_kwargs["close_mosaic"] == 10
        assert train_kwargs["device"] == "cpu"
