# 01: Project Dependencies and Hardware Acceleration Preflight

**What to build:** Configure project dependency specifications using uv, pin core computer vision libraries, and verify that Apple Silicon Metal (MPS) hardware acceleration is operational.

**Blocked by:** None (can start immediately)

**Status:** done

- [x] Declare project dependencies in configuration managed via uv with Python 3.12 compatibility.
- [x] Ensure all required core libraries (ultralytics, PyTorch, torchvision, supervision, opencv-python-headless) install cleanly without conflicts.
- [x] Provide an automated preflight verification confirming that PyTorch detects and utilizes the MPS device accelerator.
