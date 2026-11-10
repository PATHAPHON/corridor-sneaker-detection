"""Preflight unit tests for dependencies and hardware acceleration."""

import torch


def test_core_dependencies_importable():
    """Verify that all critical computer vision libraries are importable."""
    import cv2
    import supervision as sv
    import ultralytics

    assert cv2.__version__ is not None
    assert sv.__version__ is not None
    assert ultralytics.__version__ is not None


def test_mps_acceleration_available():
    """Verify that Apple Silicon Metal (MPS) device is supported and built."""
    assert torch.backends.mps.is_built(), "PyTorch was not built with MPS enabled"
    assert torch.backends.mps.is_available(), "MPS device is not available on this system"


def test_mps_tensor_operation():
    """Verify that tensors can be created and operated on the MPS device."""
    device = torch.device("mps")
    x = torch.ones((2, 2), device=device)
    y = x * 2
    assert torch.equal(y, torch.full((2, 2), 2.0, device=device))
