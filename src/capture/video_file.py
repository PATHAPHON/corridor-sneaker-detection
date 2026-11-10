"""Video file frame source for processing stored video recordings."""
from typing import Iterator, Tuple
import cv2
import numpy as np

from src.capture.base import FrameSource


class VideoFileFrameSource(FrameSource):
    """Reads sequential video frames from an on-disk video file."""

    def __init__(self, video_path: str) -> None:
        self.video_path = video_path
        self._cap = cv2.VideoCapture(video_path)
        if not self._cap.isOpened():
            raise FileNotFoundError(f"Failed to open video file: {video_path}")

        self._width = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._height = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._fps = float(self._cap.get(cv2.CAP_PROP_FPS)) or 30.0
        self._frame_count = 0

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
        """Yield frames from video until EOF."""
        frame_interval = 1.0 / self._fps if self._fps > 0 else 0.033

        while self._cap is not None and self._cap.isOpened():
            ret, frame = self._cap.read()
            if not ret or frame is None:
                break

            timestamp = self._frame_count * frame_interval
            yield (self._frame_count, timestamp, frame)
            self._frame_count += 1
        self.close()

    def close(self) -> None:
        if self._cap is not None:
            if self._cap.isOpened():
                self._cap.release()
            self._cap = None
