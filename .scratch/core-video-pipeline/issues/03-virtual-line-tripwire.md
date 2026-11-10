# 03: Virtual Line Tripwire and Anti-Bounce Debounce Engine

**What to build:** Directional virtual line crossing tripwire using 2D vector mathematics that triggers when a tracked person moves from Zone A to Zone B (Entry), suppresses duplicate triggers via a per-track cooldown window, and silently drops reverse crossings from Zone B to Zone A (Exit) while immediately resetting the track's cooldown.

**Blocked by:** 02: Person Detection, ByteTrack Tracking, and Ground Anchor Formulation

**Status:** done

- [x] Line zone module defines virtual tripwire segment between two configurable Cartesian coordinates
- [x] Directional crossing evaluates ground anchor movement vectors and fires trigger events exclusively when moving from Zone A to Zone B (Entry)
- [x] Reverse crossing from Zone B to Zone A (Exit) is silently dropped without triggering inspection events
- [x] Reverse crossing acts as an immediate cooldown reset for that track ID, allowing subsequent re-entry detection
- [x] Per-track debounce cooldown suppresses duplicate triggers for a configurable duration (default 2.0s) when an individual lingers near the line
- [x] Unit tests verify vector cross-product geometry, directional discrimination, cooldown suppression, and exit reset behavior
