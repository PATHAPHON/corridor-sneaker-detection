"""Synthetic frame source for headless CI testing and deterministic simulations."""
import time
from typing import Iterator, Optional, Tuple
import numpy as np

from src.capture.base import FrameSource


class SyntheticFrameSource(FrameSource):
    """Generates synthetic video frames for deterministic automated testing."""

    def __init__(
        self,
        width: int = 640,
        height: int = 480,
        fps: float = 30.0,
        total_frames: Optional[int] = 30,
        simulate_wall_clock: bool = False,
    ) -> None:
        self._width = width
        self._height = height
        self._fps = fps
        self._total_frames = total_frames
        self._simulate_wall_clock = simulate_wall_clock
        self._frame_count = 0
        self._is_closed = False

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
        """Yield sequential synthetic frames."""
        self._frame_count = 0
        frame_interval = 1.0 / self._fps

        while not self._is_closed:
            if self._total_frames is not None and self._frame_count >= self._total_frames:
                break

            timestamp = self._frame_count * frame_interval

            # Generate synthetic frame with a dark background and frame counter imprint
            frame = np.zeros((self._height, self._width, 3), dtype=np.uint8)

            # Optional wall-clock pacing
            if self._simulate_wall_clock:
                time.sleep(frame_interval)

            yield (self._frame_count, timestamp, frame)
            self._frame_count += 1

    def close(self) -> None:
        self._is_closed = True
