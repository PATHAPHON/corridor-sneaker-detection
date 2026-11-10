# 03: Pipeline Worker Storage Integration

**What to build:** Asynchronous dispatch from the background worker in `PipelineCoordinator` to the SQLite repository and evidence writer, persisting all crossing events without blocking the 30+ FPS capture loop.

**Blocked by:** 01 (SQLite Repository), 02 (Evidence Writer)

**Status:** done

- [x] Background worker in `PipelineCoordinator` passes processed crossing events to the storage sink
- [x] Visual evidence files and SQLite records are committed concurrently without main thread stall
- [x] Integration tests verify deterministic persistence across synthetic and video frame sources
- [x] Capture FPS remains $\ge 30$ under high crossing load
