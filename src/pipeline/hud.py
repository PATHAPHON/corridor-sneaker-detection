"""Heads-Up Display (HUD) visual annotator for live video preview."""
import time
from typing import List, Optional, Tuple
import cv2
import numpy as np

from src.tracking.person_tracker import TrackedPerson


class PipelineHud:
    """Renders visual overlays, tracking boxes, tripwire, and status on preview frames."""

    def __init__(
        self,
        tripwire_start: Tuple[int, int] = (0, 360),
        tripwire_end: Tuple[int, int] = (1280, 360),
    ) -> None:
        self.tripwire_start = tripwire_start
        self.tripwire_end = tripwire_end
        self._last_alert_text: str = "Status: Monitoring Entry Corridor"
        self._last_alert_color: Tuple[int, int, int] = (200, 200, 200)
        self._alert_expiry: float = 0.0

    def trigger_alert(self, text: str, is_compliant: bool, duration: float = 3.0) -> None:
        """Display a compliance status alert banner for the given duration."""
        self._last_alert_text = text
        self._last_alert_color = (0, 220, 0) if is_compliant else (0, 0, 220)  # BGR: Green / Red
        self._alert_expiry = time.time() + duration

    def render(
        self,
        frame: np.ndarray,
        tracked_people: List[TrackedPerson],
        fps: float = 30.0,
        queue_size: int = 0,
    ) -> np.ndarray:
        """Draw bounding boxes, anchors, tripwire, and status HUD on a copy of the frame.

        Args:
            frame: Base BGR frame array.
            tracked_people: Currently tracked pedestrians.
            fps: Measured frame rate.
            queue_size: Current items in worker event queue.

        Returns:
            Annotated BGR frame ready for display.
        """
        canvas = frame.copy()
        h, w = canvas.shape[:2]

        # 1. Draw Virtual Tripwire Line (Neon Cyan/Yellow)
        pt1 = self.tripwire_start
        pt2 = self.tripwire_end
        cv2.line(canvas, pt1, pt2, (0, 255, 255), 2, cv2.LINE_AA)

        is_vertical = abs(pt2[1] - pt1[1]) >= abs(pt2[0] - pt1[0])
        if is_vertical:
            cx = pt1[0]
            mid_y = (pt1[1] + pt2[1]) // 2
            # Directional arrow pointing from Left (A) to Right (B)
            cv2.arrowedLine(canvas, (cx - 50, mid_y), (cx + 50, mid_y), (0, 255, 255), 3, tipLength=0.35)
            cv2.putText(canvas, "ZONE A (Entry)", (max(10, cx - 180), 65),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(canvas, "ZONE B (Exit)", (cx + 25, 65),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(canvas, "TRIPWIRE (Left -> Right: A -> B)", (cx + 15, mid_y - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
        else:
            cv2.circle(canvas, pt1, 5, (0, 165, 255), -1, cv2.LINE_AA)
            cv2.circle(canvas, pt2, 5, (0, 165, 255), -1, cv2.LINE_AA)
            cv2.putText(canvas, "TRIPWIRE (Entry: A -> B)", (pt1[0] + 10, pt1[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)

        # 2. Draw Tracked Pedestrians
        for person in tracked_people:
            x1, y1, x2, y2 = [int(v) for v in person.box]
            p_height = y2 - y1

            # Bounding box (Green)
            cv2.rectangle(canvas, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Lower-Body ROI (Bottom 30% height for feet inspection) in dashed/thin Cyan
            roi_top = max(y1, int(y2 - 0.30 * p_height))
            cv2.rectangle(canvas, (x1, roi_top), (x2, y2), (255, 255, 0), 1)

            # Ground Anchor Point (Magenta circle with white border at bottom-center)
            ax, ay = int(person.anchor_point[0]), int(person.anchor_point[1])
            cv2.circle(canvas, (ax, ay), 7, (255, 255, 255), -1, cv2.LINE_AA)
            cv2.circle(canvas, (ax, ay), 5, (255, 0, 255), -1, cv2.LINE_AA)

            # Label banner
            label = f"ID: {person.track_id} ({person.confidence:.2f})"
            (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
            cv2.rectangle(canvas, (x1, max(0, y1 - lh - 6)), (x1 + lw + 4, y1), (0, 255, 0), -1)
            cv2.putText(canvas, label, (x1 + 2, y1 - 4),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1, cv2.LINE_AA)

        # 3. Top Info Bar
        cv2.rectangle(canvas, (0, 0), (w, 36), (20, 20, 20), -1)
        info_text = f"FPS: {fps:.1f} | Tracks: {len(tracked_people)} | Queue: {queue_size}/20 | 'r': Reset IDs | 'q': Quit"
        cv2.putText(canvas, info_text, (12, 24),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 1, cv2.LINE_AA)

        # 4. Status / Compliance Alert Banner
        current_time = time.time()
        if current_time < self._alert_expiry:
            banner_text = self._last_alert_text
            banner_color = self._last_alert_color
        else:
            banner_text = "Status: Monitoring Corridor (A -> B)"
            banner_color = (200, 200, 200)

        cv2.rectangle(canvas, (0, h - 32), (w, h), (30, 30, 30), -1)
        cv2.putText(canvas, banner_text, (12, h - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, banner_color, 2 if current_time < self._alert_expiry else 1, cv2.LINE_AA)

        return canvas
