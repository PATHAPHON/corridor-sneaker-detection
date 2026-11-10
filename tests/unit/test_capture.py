import numpy as np
import pytest
from unittest.mock import MagicMock, patch

from src.capture.base import FrameSource, FrameData
from src.capture.synthetic import SyntheticFrameSource
from src.capture.video_file import VideoFileFrameSource
from src.capture.camera import CameraFrameSource


def test_synthetic_frame_source_yields_expected_stream():
    """SyntheticFrameSource must yield (frame_id, timestamp, ndarray) with correct shapes."""
    width, height, fps, total_frames = 640, 480, 30.0, 10
    source = SyntheticFrameSource(
        width=width,
        height=height,
        fps=fps,
        total_frames=total_frames,
    )

    frames = list(source.stream())
    assert len(frames) == total_frames

    for idx, (frame_id, timestamp, frame) in enumerate(frames):
        assert frame_id == idx
        assert isinstance(timestamp, float)
        assert timestamp >= 0.0
        assert isinstance(frame, np.ndarray)
        assert frame.shape == (height, width, 3)
        assert frame.dtype == np.uint8


def test_synthetic_frame_source_context_manager():
    """SyntheticFrameSource should support context manager protocol."""
    with SyntheticFrameSource(width=320, height=240, fps=10.0, total_frames=3) as src:
        frames = list(src)
        assert len(frames) == 3


def test_video_file_frame_source_eof_and_close(tmp_path):
    """VideoFileFrameSource should read frames sequentially and stop at EOF."""
    fake_video_path = str(tmp_path / "test.mp4")

    # Mock cv2.VideoCapture to simulate 3 frames then EOF
    with patch("cv2.VideoCapture") as mock_cap_cls:
        mock_cap = MagicMock()
        mock_cap_cls.return_value = mock_cap
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda prop: {
            3: 1280.0,  # CAP_PROP_FRAME_WIDTH
            4: 720.0,   # CAP_PROP_FRAME_HEIGHT
            5: 30.0,    # CAP_PROP_FPS
        }.get(prop, 0.0)

        fake_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
        # Yield 3 valid frames then False (EOF)
        mock_cap.read.side_effect = [
            (True, fake_frame),
            (True, fake_frame),
            (True, fake_frame),
            (False, None),
        ]

        source = VideoFileFrameSource(fake_video_path)
        frames = list(source.stream())

        assert len(frames) == 3
        assert frames[0][0] == 0
        assert frames[1][0] == 1
        assert frames[2][0] == 2
        mock_cap.release.assert_called_once()


def test_camera_frame_source_initialization():
    """CameraFrameSource should configure camera index and capture properties."""
    with patch("cv2.VideoCapture") as mock_cap_cls:
        mock_cap = MagicMock()
        mock_cap_cls.return_value = mock_cap
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda prop: {
            3: 1920.0,
            4: 1080.0,
            5: 30.0,
        }.get(prop, 0.0)

        fake_frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
        mock_cap.read.return_value = (True, fake_frame)

        with CameraFrameSource(device_index=0, width=1920, height=1080, fps=30.0) as cam:
            frame_id, timestamp, frame = next(iter(cam.stream()))
            assert frame_id == 0
            assert frame.shape == (1080, 1920, 3)

        mock_cap.release.assert_called_once()
