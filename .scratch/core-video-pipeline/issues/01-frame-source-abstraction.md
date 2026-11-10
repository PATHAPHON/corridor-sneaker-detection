# 01: Uniform Frame Source Abstraction

**What to build:** A unified frame acquisition abstraction that feeds sequential video frames with timestamps and frame counters to the pipeline, capable of reading from camera devices, pre-recorded video files, and a deterministic synthetic frame generator for automated headless testing.

**Blocked by:** None (can start immediately)

**Status:** done

- [x] Uniform frame source interface yields sequential frame IDs, timestamps, and RGB/BGR frame arrays
- [x] Synthetic frame source generates deterministic frames of configurable dimensions and framerate for unit and integration testing without camera hardware
- [x] Video file frame source reads pre-recorded video media and terminates gracefully upon reaching EOF
- [x] Camera frame source connects to system video capture device with configurable resolution and framerate
- [x] Comprehensive unit tests verify frame source iteration, EOF handling, and synthetic frame generation
