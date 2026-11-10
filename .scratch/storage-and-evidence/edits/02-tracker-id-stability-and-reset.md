# Edit 02: Tracker ID Stability and Reset Mechanism

**Status:** done

## Rationale & Impact
During single-person testing, track IDs churned rapidly (skipping from 3 to 17, 35, 54) due to two factors:
1. Low person confidence threshold (0.40) caused transient background items to register as persons, consuming IDs before disappearing.
2. Short default ByteTrack buffer (30 frames ~ 1.0s) immediately purged the person identity when they stepped out of the camera's field of view, assigning a new ID on return.
3. ByteTrack's internal class-level counter `STrack._count` was never reset upon pipeline launch.

Increasing `person_confidence` to 0.50, increasing `track_buffer` to 90 frames (3 seconds), resetting `STrack._count` on tracker initialization, and adding an interactive 'r' key in the GUI preview resolves ID jumping and maintains consistent pedestrian identity.

## Target Files
- `src/config/bytetrack.yaml`
- `src/config/settings.py`
- `src/tracking/person_tracker.py`
- `src/tripwire/zone.py`
- `src/pipeline/coordinator.py`
- `src/pipeline/hud.py`
- `tests/unit/test_tracking.py`

## Planned Changes
- Update `PipelineConfig` default `person_confidence` to `0.50` and add `tracker_config` pointing to tuned configuration.
- Add `src/config/bytetrack.yaml` with `track_buffer=90` (3.0s) and `new_track_thresh=0.50`.
- Call `STrack.reset_id()` in `PersonTracker.__init__` and implement `PersonTracker.reset()`.
- Add interactive 'r' keypress handler in `PipelineCoordinator.run()` to trigger `reset_tracking()`.
- Update tests in `tests/unit/test_tracking.py` to verify reset mechanism.

## Acceptance Criteria
- [x] `PersonTracker` resets `STrack` ID counter on initialization so first detected track starts at 1.
- [x] `PersonTracker.reset()` clears tracker state and resets ID counter.
- [x] `PipelineCoordinator` responds to 'r' key by resetting tracker and tripwire cooldowns.
- [x] All unit and integration tests pass cleanly (`pytest`).
