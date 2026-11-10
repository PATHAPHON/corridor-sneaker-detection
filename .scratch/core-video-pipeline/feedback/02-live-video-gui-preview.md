# Feedback 02: Real-time Live Video GUI Preview

**Feature**: core-video-pipeline
**Linked edit**: edits/02-live-video-gui-preview.md
**Signal**: extend

## What the user said (verbatim)
> ไม่แสดงเป็นvideo ให้ดู

## Reason the user gave
Not stated

## What the user asked to change
- Display a live GUI window rendering the video stream in real-time with visual overlays (tripwire line, tracked pedestrian bounding boxes, anchor points, and detection status HUD) instead of terminal-only text output.

## What was actually changed (fill in after the edit)
- Created `src/pipeline/hud.py` with `PipelineHud` rendering visual overlays (Tripwire line, pedestrian bounding boxes, anchor points, active alerts, and FPS).
- Updated `src/pipeline/coordinator.py` to support `show_preview=True`, displaying a real-time OpenCV window with `cv2.imshow` and keyboard exit handling ('q' or ESC).
- Updated `src/main.py` to enable GUI preview by default, with `--no-gui` flag available for headless runs. All 24 tests passing.
