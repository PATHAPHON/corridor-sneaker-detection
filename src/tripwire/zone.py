"""Virtual line tripwire and directional anti-bounce debounce engine."""
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
import supervision as sv

from src.tracking.person_tracker import TrackedPerson


@dataclass(frozen=True)
class TripwireCrossing:
    """Immutable record of a detected directional line crossing event."""
    track_id: int
    timestamp: float
    direction: str  # e.g., "ENTRY"
    box: Tuple[float, float, float, float]
    anchor_point: Tuple[float, float]


class TripwireZone:
    """Evaluates virtual line crossings using 2D geometry and per-track cooldowns."""

    def __init__(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
        cooldown_seconds: float = 2.0,
        trigger_on_in: Optional[bool] = None,
    ) -> None:
        self.start = start
        self.end = end
        self.cooldown_seconds = cooldown_seconds

        # For vertical line from top to bottom, moving left to right (A -> B) is 'crossed_in'.
        # For horizontal line from left to right, moving top to bottom (A -> B) is 'crossed_out'.
        is_vertical = abs(end[1] - start[1]) >= abs(end[0] - start[0])
        self.trigger_on_in = is_vertical if trigger_on_in is None else trigger_on_in

        self.line_zone = sv.LineZone(
            start=sv.Point(x=start[0], y=start[1]),
            end=sv.Point(x=end[0], y=end[1]),
            triggering_anchors=[sv.Position.BOTTOM_CENTER],
        )
        self._last_trigger_time: Dict[int, float] = {}

    def update(
        self,
        tracked_people: List[TrackedPerson],
        timestamp: float,
    ) -> List[TripwireCrossing]:
        """Update tracker positions against the virtual line.

        Args:
            tracked_people: Current frame's tracked pedestrians.
            timestamp: Frame timestamp in seconds.

        Returns:
            List of confirmed Entry crossing events that pass debounce cooldown.
        """
        if not tracked_people:
            # Still call LineZone with empty detections to evict absent tracks
            self.line_zone.trigger(sv.Detections.empty())
            return []

        # Convert TrackedPerson instances into supervision Detections
        xyxy = np.array([p.box for p in tracked_people], dtype=np.float32)
        tracker_ids = np.array([p.track_id for p in tracked_people], dtype=np.int32)
        confidences = np.array([p.confidence for p in tracked_people], dtype=np.float32)

        detections = sv.Detections(
            xyxy=xyxy,
            confidence=confidences,
            tracker_id=tracker_ids,
        )

        crossed_in, crossed_out = self.line_zone.trigger(detections)

        # Per ADR-0002: Vector directed from start -> end bisects plane into:
        # - Zone A: Left-hand side relative to directed vector
        # - Zone B: Right-hand side relative to directed vector
        # In supervision.LineZone, transitioning from Left (A) to Right (B) yields crossed_out=True.
        # Transitioning from Right (B) to Left (A) yields crossed_in=True.
        confirmed_crossings: List[TripwireCrossing] = []

        for i, person in enumerate(tracked_people):
            if self.trigger_on_in:
                is_entry = bool(crossed_in[i])
                is_exit = bool(crossed_out[i])
            else:
                is_entry = bool(crossed_out[i])
                is_exit = bool(crossed_in[i])

            # Check Exit crossing (B -> A)
            if is_exit:
                # Silent drop + immediate cooldown reset for this track_id
                self._last_trigger_time.pop(person.track_id, None)

            # Check Entry crossing (A -> B)
            elif is_entry:
                last_time = self._last_trigger_time.get(person.track_id, -float("inf"))
                if (timestamp - last_time) >= self.cooldown_seconds:
                    self._last_trigger_time[person.track_id] = timestamp
                    confirmed_crossings.append(
                        TripwireCrossing(
                            track_id=person.track_id,
                            timestamp=timestamp,
                            direction="ENTRY",
                            box=person.box,
                            anchor_point=person.anchor_point,
                        )
                    )

        return confirmed_crossings

    def reset(self) -> None:
        """Clear all active per-track cooldowns and line zone history."""
        self._last_trigger_time.clear()
