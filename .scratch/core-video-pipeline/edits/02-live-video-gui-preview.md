# Edit 02: Real-time Live Video GUI Preview Window with Visual HUD

**Status:** done

## Rationale & Impact
When running `uv run python -m src.main`, the pipeline processed frames and logged text to the terminal, but did not open a visual window (`ไม่แสดงเป็นvideo ให้ดู`).
Operators and users need to visually inspect the camera view to:
1. Verify camera framing and corridor coverage.
2. See the virtual tripwire line and understand where the crossing boundary lies.
3. Observe real-time bounding boxes, track IDs, ground anchor points, and sneaker compliance alerts.

## Target Files
- `src/pipeline/hud.py`
- `src/pipeline/coordinator.py`
- `src/main.py`
- `tests/integration/test_pipeline.py`

## Planned Changes
- Add an optional `show_preview: bool = True` option in `PipelineCoordinator` and `--no-gui` / `--gui` flags in `src/main.py`.
- Render real-time visual annotations on the display frame:
  - Directed virtual tripwire line with labeled endpoints ($A$ and $B$).
  - Pedestrian bounding boxes, track IDs, and bottom-center ground anchor dots ($P_{anchor}$).
  - Live HUD banner displaying crossing alerts, sneaker detection status, and FPS.
- Handle OpenCV GUI event loop (`cv2.imshow`, `cv2.waitKey(1)`) gracefully with 'q' or ESC key exit.

## Acceptance Criteria
- [x] Running `uv run python -m src.main` opens an interactive OpenCV window displaying the live video feed.
- [x] Visual overlays show the tripwire line, person bounding boxes, and detection status.
- [x] Pressing 'q' or closing the window terminates the application cleanly.
- [x] Headless mode (`--no-gui` / `show_preview=False`) remains fully supported for CI tests.
- [x] All unit and integration tests pass cleanly.
