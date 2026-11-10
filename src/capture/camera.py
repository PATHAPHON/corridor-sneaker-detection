"""Camera frame source for live real-time video capture."""
import sys
import time
from typing import Iterator, Optional, Tuple
import cv2
import numpy as np

from src.capture.base import FrameSource


class CameraFrameSource(FrameSource):
    """Captures real-time frames from a connected camera device."""

    def __init__(
        self,
        device_index: int = 0,
        width: Optional[int] = None,
        height: Optional[int] = None,
        fps: Optional[float] = None,
    ) -> None:
        self.device_index = device_index

        # On macOS (Darwin), prioritize AVFoundation backend for FaceTime and USB webcams
        if sys.platform == "darwin":
            self._cap = cv2.VideoCapture(device_index, cv2.CAP_AVFOUNDATION)
        else:
            self._cap = cv2.VideoCapture(device_index)

        if not self._cap.isOpened():
            self._cap = cv2.VideoCapture(device_index)

        if not self._cap.isOpened():
            raise RuntimeError(f"Failed to open camera device index {device_index}")

        if width is not None:
            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, float(width))
        if height is not None:
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, float(height))
        if fps is not None:
            self._cap.set(cv2.CAP_PROP_FPS, float(fps))

        self._width = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._height = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._fps = float(self._cap.get(cv2.CAP_PROP_FPS)) or 30.0
        self._frame_count = 0
        self._start_time: Optional[float] = None

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def fps(self) -> float:
        return self._fps

    def stream(self) -> Iterator[Tuple[int, float, np.ndarray]]:
        """Continuously stream live frames from camera."""
        self._start_time = time.time()
        while self._cap is not None and self._cap.isOpened():
            ret, frame = self._cap.read()
            if not ret or frame is None:
                break

            timestamp = time.time() - self._start_time
            yield (self._frame_count, timestamp, frame)
            self._frame_count += 1

    def close(self) -> None:
        if self._cap is not None:
            if self._cap.isOpened():
                self._cap.release()
            self._cap = None
