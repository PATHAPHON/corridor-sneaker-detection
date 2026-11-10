import numpy as np
import pytest
from unittest.mock import MagicMock
from src.tracking.person_tracker import TrackedPerson
from src.tripwire.zone import TripwireZone, TripwireCrossing


def test_tripwire_crossing_entry_and_exit_discrimination():
    """Verify that moving A -> B triggers Entry crossing, while B -> A is dropped."""
    # Line across corridor: horizontal line at y=200 from x=0 to x=600
    # Vector points from (0, 200) to (600, 200)
    # Zone A (left of vector): y < 200
    # Zone B (right of vector): y > 200
    tripwire = TripwireZone(
        start=(0, 200),
        end=(600, 200),
        cooldown_seconds=2.0,
    )

    # Person 1 starts in Zone A (y=150)
    p1_f1 = TrackedPerson(track_id=1, box=(90, 50, 110, 150), confidence=0.9, anchor_point=(100, 150))
    crossings_f1 = tripwire.update([p1_f1], timestamp=0.0)
    assert len(crossings_f1) == 0

    # Person 1 moves to Zone B (y=250) -> Crossing A -> B (Entry)
    p1_f2 = TrackedPerson(track_id=1, box=(90, 150, 110, 250), confidence=0.9, anchor_point=(100, 250))
    crossings_f2 = tripwire.update([p1_f2], timestamp=0.033)
    assert len(crossings_f2) == 1
    assert crossings_f2[0].track_id == 1
    assert crossings_f2[0].direction == "ENTRY"
    assert crossings_f2[0].anchor_point == (100, 250)

    # Person 1 steps back to Zone A (y=150) -> Exit (B -> A)
    # Must be silently dropped (no crossing event returned)
    p1_f3 = TrackedPerson(track_id=1, box=(90, 50, 110, 150), confidence=0.9, anchor_point=(100, 150))
    crossings_f3 = tripwire.update([p1_f3], timestamp=0.066)
    assert len(crossings_f3) == 0


def test_tripwire_cooldown_debounce_suppression():
    """Duplicate A -> B triggers within cooldown window must be suppressed without exit reset."""
    tripwire = TripwireZone(
        start=(0, 200),
        end=(600, 200),
        cooldown_seconds=2.0,
    )

    # Initial crossing at t=0.1
    p1_a = TrackedPerson(track_id=1, box=(90, 50, 110, 150), confidence=0.9, anchor_point=(100, 150))
    p1_b = TrackedPerson(track_id=1, box=(90, 150, 110, 250), confidence=0.9, anchor_point=(100, 250))
    tripwire.update([p1_a], timestamp=0.0)
    c1 = tripwire.update([p1_b], timestamp=0.1)
    assert len(c1) == 1

    # Simulate another trigger for same track_id at t=1.0 (< 2.0s cooldown) without exit reset
    # Mocking line_zone trigger to report crossed_out=True again
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(tripwire.line_zone, "trigger", lambda dets: (np.array([False]), np.array([True])))
        c2 = tripwire.update([p1_b], timestamp=1.0)
        assert len(c2) == 0  # Suppressed by cooldown

        # Crossing again after cooldown expires at t=3.5s (> 2.0s)
        c3 = tripwire.update([p1_b], timestamp=3.5)
        assert len(c3) == 1
        assert c3[0].track_id == 1


def test_tripwire_exit_resets_cooldown_immediately():
    """Exit (B -> A) must immediately reset cooldown for that track_id."""
    tripwire = TripwireZone(
        start=(0, 200),
        end=(600, 200),
        cooldown_seconds=5.0,  # long cooldown
    )

    # Entry at t=0.1
    p1_a = TrackedPerson(track_id=1, box=(90, 50, 110, 150), confidence=0.9, anchor_point=(100, 150))
    p1_b = TrackedPerson(track_id=1, box=(90, 150, 110, 250), confidence=0.9, anchor_point=(100, 250))
    tripwire.update([p1_a], timestamp=0.0)
    c1 = tripwire.update([p1_b], timestamp=0.1)
    assert len(c1) == 1

    # Person exits at t=0.5 (B -> A)
    tripwire.update([p1_a], timestamp=0.5)

    # Person immediately re-enters at t=0.8 (before 5.0s would have expired)
    c2 = tripwire.update([p1_b], timestamp=0.8)
    assert len(c2) == 1
    assert c2[0].track_id == 1


def test_tripwire_vertical_lateral_side_view_crossing():
    """Verify ADR-0005 lateral side view: vertical tripwire at x=960 triggers on left-to-right transit."""
    tripwire = TripwireZone(
        start=(960, 0),
        end=(960, 1080),
        cooldown_seconds=2.0,
    )

    # Person walking left to right: starts at x=800 (Zone A)
    p_left = TrackedPerson(track_id=1, box=(750, 700, 850, 1000), confidence=0.92, anchor_point=(800, 1000))
    # Moves to x=1100 (Zone B)
    p_right = TrackedPerson(track_id=1, box=(1050, 700, 1150, 1000), confidence=0.92, anchor_point=(1100, 1000))

    # Frame 1: on left side
    c1 = tripwire.update([p_left], timestamp=0.0)
    assert len(c1) == 0

    # Frame 2: crosses to right side -> Entry!
    c2 = tripwire.update([p_right], timestamp=0.033)
    assert len(c2) == 1
    assert c2[0].track_id == 1
    assert c2[0].direction == "ENTRY"

    # Frame 3: walking back right to left -> Exit (silent drop)
    c3 = tripwire.update([p_left], timestamp=0.066)
    assert len(c3) == 0
