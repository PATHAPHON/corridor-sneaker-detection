"""Fine-tuned single-class sneaker detector module."""
from dataclasses import dataclass
from typing import List, Optional, Tuple
import numpy as np
import torch
from ultralytics import YOLO

from src.tracking.person_tracker import get_default_device


@dataclass(frozen=True)
class FootwearInspectionResult:
    """Immutable result of footwear inference on lower-body crop."""
    shoes_detected: bool
    sneaker_count: int
    boxes: List[Tuple[float, float, float, float]]
    confidences: List[float]


class FootwearInspector:
    """Executes sneaker inference on lower-body crops using fine-tuned YOLO11n."""

    def __init__(
        self,
        model_path: str = "models/yolo-sneaker.pt",
        confidence_threshold: float = 0.40,
        device: Optional[str] = None,
    ) -> None:
        self.device = device if device is not None else get_default_device()
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.model = YOLO(model_path)

    def inspect(self, roi_crop: np.ndarray) -> FootwearInspectionResult:
        """Run sneaker detection on lower-body crop.

        Args:
            roi_crop: BGR lower-body image crop.

        Returns:
            FootwearInspectionResult containing detection status, counts, boxes, confidences.
        """
        if roi_crop.size == 0 or roi_crop.shape[0] < 5 or roi_crop.shape[1] < 5:
            return FootwearInspectionResult(
                shoes_detected=False,
                sneaker_count=0,
                boxes=[],
                confidences=[],
            )

        results = self.model(
            roi_crop,
            classes=[0],
            conf=self.confidence_threshold,
            device=self.device,
            verbose=False,
        )

        boxes: List[Tuple[float, float, float, float]] = []
        confidences: List[float] = []

        if results and results[0].boxes is not None:
            for b in results[0].boxes:
                conf = float(b.conf[0].item() if hasattr(b.conf[0], "item") else b.conf[0])
                if conf >= self.confidence_threshold:
                    coords = b.xyxy[0].tolist() if hasattr(b.xyxy[0], "tolist") else list(b.xyxy[0])
                    boxes.append((float(coords[0]), float(coords[1]), float(coords[2]), float(coords[3])))
                    confidences.append(conf)

        sneaker_count = len(boxes)
        shoes_detected = sneaker_count > 0

        return FootwearInspectionResult(
            shoes_detected=shoes_detected,
            sneaker_count=sneaker_count,
            boxes=boxes,
            confidences=confidences,
        )
