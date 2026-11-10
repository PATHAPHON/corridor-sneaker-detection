"""Frame source abstractions and implementations."""
from src.capture.base import FrameData, FrameSource
from src.capture.camera import CameraFrameSource
from src.capture.synthetic import SyntheticFrameSource
from src.capture.video_file import VideoFileFrameSource

__all__ = [
    "FrameSource",
    "FrameData",
    "CameraFrameSource",
    "SyntheticFrameSource",
    "VideoFileFrameSource",
]
