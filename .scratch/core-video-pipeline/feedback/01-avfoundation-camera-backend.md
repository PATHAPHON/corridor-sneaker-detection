# Feedback 01: macOS AVFoundation Camera Backend

**Feature**: core-video-pipeline
**Linked edit**: edits/01-avfoundation-camera-backend.md
**Signal**: bug

## What the user said (verbatim)
> uv run python -m src.main
> 2026-11-10 17:47:58,703 [INFO] main: Using CameraFrameSource device index: 0
> OpenCV: not authorized to capture video (status 0), requesting...
> OpenCV: camera failed to properly initialize!
> [ WARN:0@2.470] global cap_ffmpeg_impl.hpp:1240 open VIDEOIO/FFMPEG: Failed list devices for backend avfoundation
> Traceback (most recent call last):
> RuntimeError: Failed to open camera device index 0

## Reason the user gave
Not stated

## What the user asked to change
- Fix camera initialization on macOS so `CameraFrameSource` successfully accesses the MacBook camera without `VideoCapture` runtime errors.

## What was actually changed (fill in after the edit)
- Updated `src/capture/camera.py` to explicitly use `cv2.CAP_AVFOUNDATION` on macOS (`sys.platform == "darwin"`), preventing OpenCV from failing on FFMPEG camera probe. Verified 24 tests passing.
