"""Unit tests for trained sneaker YOLO detector and exported model artifact."""

from pathlib import Path
import numpy as np
import pytest
from ultralytics import YOLO


@pytest.fixture(scope="module")
def model_path() -> Path:
    """Fixture providing path to exported sneaker model weights."""
    path = Path("models/yolo-sneaker.pt")
    assert path.is_file(), f"Trained weights not found at: {path}"
    return path


def test_sneaker_model_weights_exist(model_path: Path):
    """Verify that models/yolo-sneaker.pt exists and is a valid file size."""
    size_mb = model_path.stat().st_size / (1024 * 1024)
    assert size_mb > 1.0, f"Model file unexpectedly small: {size_mb:.2f} MB"


def test_sneaker_model_loads_and_single_class(model_path: Path):
    """Verify that model loads as YOLO and has exactly 1 class: 'sneaker'."""
    model = YOLO(str(model_path))
    assert model.names is not None
    assert len(model.names) == 1
    assert model.names[0] == "sneaker"


def test_sneaker_model_inference_contract(model_path: Path):
    """Verify that model inference on numpy array returns valid YOLO result objects."""
    model = YOLO(str(model_path))
    dummy_frame = np.zeros((640, 640, 3), dtype=np.uint8)
    results = model(dummy_frame, device="cpu", verbose=False)

    assert len(results) == 1
    result = results[0]
    assert hasattr(result, "boxes")
    assert hasattr(result.boxes, "xyxy")
    assert hasattr(result.boxes, "conf")
    assert hasattr(result.boxes, "cls")


def test_sneaker_model_detects_real_sample(model_path: Path):
    """Verify model detects sneakers on a real test image with confidence >= 0.40."""
    test_images = sorted(list(Path("datasets/sneakers/test/images").glob("*.*")))
    assert len(test_images) > 0, "No test images found in datasets/sneakers/test/images"

    model = YOLO(str(model_path))
    sample_image = str(test_images[0])
    results = model(sample_image, device="cpu", conf=0.40, verbose=False)

    assert len(results) == 1
    boxes = results[0].boxes
    assert len(boxes) > 0, f"Expected at least one sneaker detected in {sample_image}"
    assert float(boxes.conf[0]) >= 0.40
    assert int(boxes.cls[0]) == 0
