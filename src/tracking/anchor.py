"""Calculation of floor-plane ground contact anchor point."""
from typing import Tuple


def calculate_ground_anchor_point(box: Tuple[float, float, float, float]) -> Tuple[float, float]:
    """Calculate the bottom-center Ground Anchor Point from a bounding box.

    Formula per Invariant 4 & GLOSSARY.md:
        P_anchor = ((x_min + x_max) / 2.0, y_max)

    Args:
        box: Bounding box tuple (x_min, y_min, x_max, y_max).

    Returns:
        Tuple of (anchor_x, anchor_y).
    """
    x_min, y_min, x_max, y_max = box
    anchor_x = (x_min + x_max) / 2.0
    anchor_y = float(y_max)
    return (anchor_x, anchor_y)
