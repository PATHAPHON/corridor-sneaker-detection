# Feedback 02: Tracker ID Stability and Reset

**Feature**: storage-and-evidence
**Linked edit**: edits/02-tracker-id-stability-and-reset.md
**Signal**: refine

## What the user said (verbatim)
> ได้ทำตามนี้

## Reason the user gave
Not stated

## What the user asked to change
- Prevent track ID churning and jumping when walking alone.
- Increase person detection confidence to eliminate false positive background object tracks.
- Increase tracker buffer to preserve track ID when temporarily out of camera frame.
- Reset ByteTrack track ID counter back to 1 on startup and support interactive reset via GUI keypress ('r').

## What was actually changed (fill in after the edit)
- `src/config/bytetrack.yaml`: Configured tuned ByteTrack tracking parameters (`track_buffer: 90` frames = 3.0s, `new_track_thresh: 0.50`, `track_high_thresh: 0.50`).
- `src/config/settings.py`: Updated default `person_confidence: 0.50` and added `tracker_config` pointing to tuned configuration.
- `src/tracking/person_tracker.py`: Implemented `reset()` to call `STrack.reset_id()` and clear model predictors on startup and reset.
- `src/tripwire/zone.py`: Added `reset()` to flush per-track cooldown timestamps.
- `src/pipeline/coordinator.py`: Added `reset_tracking()` and connected `'r'` interactive keypress handler in GUI loop.
- `src/pipeline/hud.py`: Added `'r': Reset IDs` hint to top HUD status bar.
- `tests/unit/test_tracking.py`: Added `test_person_tracker_reset_resets_track_id` unit test.
