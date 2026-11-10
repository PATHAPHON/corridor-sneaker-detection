# Edit 01: Enable AVFoundation Camera Backend for macOS

**Status:** done

## Rationale & Impact
The user attempted to run `uv run python -m src.main` using the MacBook built-in FaceTime HD camera, but OpenCV failed with:
`[ WARN:0@2.470] global cap_ffmpeg_impl.hpp:1240 open VIDEOIO/FFMPEG: Failed list devices for backend avfoundation`
`RuntimeError: Failed to open camera device index 0`

OpenCV on macOS defaults to `CAP_ANY` which invokes FFMPEG device probing first. On macOS (Darwin), native camera access requires the `cv2.CAP_AVFOUNDATION` backend explicitly. When tested with `cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)`, the FaceTime HD camera opened immediately and yielded 1080p frames (`(1080, 1920, 3)`).
Therefore, `CameraFrameSource` must explicitly attempt `cv2.CAP_AVFOUNDATION` on macOS, falling back to standard `cv2.VideoCapture` on Linux/Windows.

## Target Files
- `src/capture/camera.py`
- `tests/unit/test_capture.py`

## Planned Changes
- Update `CameraFrameSource.__init__` to explicitly use `cv2.CAP_AVFOUNDATION` on Darwin platforms, falling back gracefully if needed.
- Update tests in `test_capture.py` to ensure compatibility with backend parameters.

## Acceptance Criteria
- [x] `CameraFrameSource` uses `cv2.CAP_AVFOUNDATION` when running on macOS.
- [x] All unit and integration tests pass cleanly.
