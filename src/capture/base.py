"""Base abstractions and data structures for frame capture."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterator, NamedTuple, Tuple
import numpy as np


class FrameData(NamedTuple):
    """Immutable frame payload yielded by a FrameSource."""
    frame_id: int
    timestamp: float
    frame: np.ndarray


class FrameSource(ABC):
    """Abstract base class defining the uniform frame acquisition interface."""

    @abstractmethod
    def stream(self) -> Iterator[Tuple[int, float, np.ndarray]]:
        """Yield sequential tuples of (frame_id, timestamp, frame_ndarray)."""
        pass

    @property
    @abstractmethod
    def width(self) -> int:
        """Frame width in pixels."""
        pass

    @property
    @abstractmethod
    def height(self) -> int:
        """Frame height in pixels."""
        pass

    @property
    @abstractmethod
    def fps(self) -> float:
        """Frames per second of the source stream."""
        pass

    def close(self) -> None:
        """Release underlying hardware or file resources."""
        pass

    def __iter__(self) -> Iterator[Tuple[int, float, np.ndarray]]:
        return self.stream()

    def __enter__(self) -> "FrameSource":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
