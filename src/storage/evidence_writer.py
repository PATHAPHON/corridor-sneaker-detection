"""Date-partitioned visual evidence filesystem writer."""
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Sequence
import cv2
import numpy as np

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SavedEvidencePaths:
    """Paths to saved evidence images."""
    full_image_path: str
    crop_image_path: str


class EvidenceWriter:
    """Saves full scene and annotated cropped feet ROI images into date-partitioned folders."""

    def __init__(self, base_dir: str = "output/captures"):
        self.base_dir = Path(base_dir)

    def save_evidence(
        self,
        timestamp: str,
        track_id: int,
        full_frame: np.ndarray,
        roi_crop: np.ndarray,
        boxes: Optional[np.ndarray] = None,
        confidences: Optional[Sequence[float]] = None,
        event_id: Optional[int] = None,
    ) -> SavedEvidencePaths:
        """Save full frame and annotated lower-body crop.

        Args:
            timestamp: Timestamp string (e.g. ISO format or float seconds).
            track_id: Multi-object tracking ID.
            full_frame: Full camera context frame (H, W, 3).
            roi_crop: Cropped lower-body ROI (H_crop, W_crop, 3).
            boxes: Optional sneaker bounding boxes relative to crop [N, 4].
            confidences: Optional list of confidence values.
            event_id: Optional sequential event sequence number for filename ordering.

        Returns:
            SavedEvidencePaths containing absolute or configured string paths.
        """
        # Determine date folder (YYYY-MM-DD)
        date_str = self._extract_date_str(timestamp)
        date_dir = self.base_dir / date_str
        date_dir.mkdir(parents=True, exist_ok=True)

        # Sanitize timestamp for safe filesystem usage
        safe_timestamp = timestamp.replace(":", "-").replace(" ", "T")
        prefix = f"{event_id:05d}_" if event_id is not None else ""
        full_path = date_dir / f"{prefix}{safe_timestamp}_{track_id}_full.jpg"
        crop_path = date_dir / f"{prefix}{safe_timestamp}_{track_id}_crop.jpg"

        # 1. Save full frame
        cv2.imwrite(str(full_path), full_frame)

        # 2. Render bounding boxes and confidence overlays on lower-body crop
        annotated_crop = roi_crop.copy()
        if boxes is not None and len(boxes) > 0:
            for idx, box in enumerate(boxes):
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(annotated_crop, (x1, y1), (x2, y2), (0, 255, 0), 2)
                conf_text = (
                    f"sneaker: {confidences[idx]:.2f}"
                    if confidences and idx < len(confidences)
                    else "sneaker"
                )
                cv2.putText(
                    annotated_crop,
                    conf_text,
                    (x1, max(12, y1 - 4)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    (0, 255, 0),
                    1,
                    cv2.LINE_AA,
                )

        cv2.imwrite(str(crop_path), annotated_crop)
        logger.debug("Evidence saved: %s, %s", full_path, crop_path)

        return SavedEvidencePaths(
            full_image_path=str(full_path),
            crop_image_path=str(crop_path),
        )

    @staticmethod
    def _extract_date_str(timestamp: str) -> str:
        """Extract YYYY-MM-DD from timestamp string or fallback to today's date."""
        if (
            len(timestamp) >= 10
            and timestamp[4] == "-"
            and timestamp[7] == "-"
            and not timestamp.startswith("1970-01-01")
        ):
            return timestamp[:10]
        return datetime.now().strftime("%Y-%m-%d")
