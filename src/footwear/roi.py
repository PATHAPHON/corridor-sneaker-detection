"""Lower-body ROI extraction for footwear inspection."""
from dataclasses import dataclass
from typing import Tuple
import numpy as np


@dataclass(frozen=True)
class LowerBodyRoi:
    """Extracted lower-body region of interest."""
    roi_box: Tuple[int, int, int, int]  # (x1, y1, x2, y2) in frame pixel coordinates
    crop: np.ndarray                   # Sliced BGR image array


def extract_lower_body_roi(
    frame: np.ndarray,
    person_box: Tuple[float, float, float, float],
    height_ratio: float = 0.30,
    margin_ratio: float = 0.10,
) -> LowerBodyRoi:
    """Crop the lower-body region (bottom 30% of height with 10% horizontal padding).

    Formula per Invariant 3 & ADR-0003:
        y_top = y_max - 0.30 * (y_max - y_min)
        x_left = max(0, x_min - 0.10 * width)
        x_right = min(frame_width, x_max + 0.10 * width)

    Args:
        frame: Full BGR frame ndarray.
        person_box: Person bounding box (x_min, y_min, x_max, y_max).
        height_ratio: Fraction of person height for feet ROI (default 0.30).
        margin_ratio: Horizontal margin fraction on each side (default 0.10).

    Returns:
        LowerBodyRoi containing clamped box coordinates and image crop.
    """
    frame_h, frame_w = frame.shape[:2]
    x_min, y_min, x_max, y_max = person_box

    width = x_max - x_min
    height = y_max - y_min

    roi_y_top = int(round(y_max - height_ratio * height))
    roi_y_bottom = int(round(y_max))
    roi_x_left = int(round(x_min - margin_ratio * width))
    roi_x_right = int(round(x_max + margin_ratio * width))

    # Clamp coordinates to frame boundaries
    clamped_x_left = max(0, min(frame_w, roi_x_left))
    clamped_y_top = max(0, min(frame_h, roi_y_top))
    clamped_x_right = max(0, min(frame_w, roi_x_right))
    clamped_y_bottom = max(0, min(frame_h, roi_y_bottom))

    # Handle degenerated crop
    if clamped_x_right <= clamped_x_left or clamped_y_bottom <= clamped_y_top:
        empty_crop = np.zeros((0, 0, 3), dtype=frame.dtype)
        return LowerBodyRoi(
            roi_box=(clamped_x_left, clamped_y_top, clamped_x_right, clamped_y_bottom),
            crop=empty_crop,
        )

    crop = frame[clamped_y_top:clamped_y_bottom, clamped_x_left:clamped_x_right].copy()

    return LowerBodyRoi(
        roi_box=(clamped_x_left, clamped_y_top, clamped_x_right, clamped_y_bottom),
        crop=crop,
    )
