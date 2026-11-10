# AGENTS.md — Engineering Guidelines & Operational Standards

## 1. Project Overview & Tech Stack

This project is a real-time computer vision monitoring system that tracks pedestrians crossing a virtual tripwire (corridor entry), extracts a lower-body ROI, detects sneakers using a fine-tuned single-class YOLO11 detector, saves annotated visual evidence, and logs events into SQLite.

- **Language / Runtime**: Python 3.12 (managed via `uv`)
- **Computer Vision & Tracking**:
  - `ultralytics` (YOLO11 Nano: `yolo11n.pt` for person detection, `models/yolo-sneaker.pt` for single-class sneaker detection)
  - `supervision` (ByteTrack multi-object tracking, LineZone directional tripwire crossing)
  - `opencv-python-headless` (frame acquisition, transformations, visual annotation)
- **Data Persistence**: `sqlite3` with WAL (`Write-Ahead Logging`) mode enabled, local file system for evidence images
- **Hardware Acceleration**: Apple Silicon Metal (`mps`) auto-detected, fallback to CUDA or CPU
- **Testing & Quality Tooling**: `pytest`, `pytest-mock`
- **Architecture Pattern**: Two-stage decoupled concurrency (real-time video capture/tracking thread + bounded background worker thread)

---

## 2. Build, Run & Test Commands

Always use `uv run` to guarantee isolated execution with pinned dependencies.

```bash
# Install / Sync dependencies
uv sync

# Run main application (default webcam)
uv run python -m src.main

# Run with test video file
uv run python -m src.main --video path/to/sample.mp4

# Run test suite
uv run pytest

# Run single test file
uv run pytest tests/test_tripwire.py -v

# Graphify Knowledge Graph (Mandatory before coding or answering architecture questions)
graphify .
graphify query "<target>"
graphify explain "<target>"
graphify path "<A>" "<B>"
graphify update .
```

---

## 3. Code Style & Architecture Conventions

### Clean 10-Line Pattern (Decoupled Stage Architecture)
- The main capture thread must remain lightweight and non-blocking, executing ONLY frame reading, person detection, ByteTrack tracking, and LineZone evaluation.
- All heavy operations (sneaker inference, disk writes, SQLite inserts) MUST be enqueued to the bounded background worker.

```python
# IDEAL PATTERN: Main loop enqueues event without blocking
for frame in frame_source.stream():
    detections = person_detector.detect(frame)
    tracked = tracker.update_with_detections(detections)
    crossings = tripwire.trigger(tracked)
    for crossing in crossings:
        event_queue.put_nowait(CrossingEventTask(frame=frame.copy(), crossing=crossing))
    hud.render(frame, tracked)
    hud.display(frame)
```

### Forbidden Anti-Patterns
- **DO NOT** perform sneaker YOLO inference or disk I/O in the main video loop (causes frame drop below 30 FPS).
- **DO NOT** use unconstrained queues (e.g., `queue.Queue()`) without `maxsize=20` (prevents memory spikes during crowd bursts).
- **DO NOT** hardcode absolute file paths, camera device indices, confidence thresholds, or line coordinates in business logic. All tunables belong in configuration models (`src/config/`).
- **DO NOT** write code without type hints and docstrings.

---

## 4. Architecture & Module Boundaries

```text
src/
├── capture/      # FrameSource abstractions (CameraFrameSource, VideoFileFrameSource, SyntheticFrameSource)
├── tracking/     # YOLO11 person detector, ByteTrack tracker, bottom-center ground anchor point
├── tripwire/     # Virtual line crossing, 2D vector cross product, per-track cooldown
├── footwear/     # Bottom 30% ROI extractor, fine-tuned YOLO11 sneaker detector
├── storage/      # SQLite repository (WAL mode), evidence JPEG writer
├── pipeline/     # Concurrency manager (Main thread + Bounded Queue + Worker thread), graceful shutdown
└── config/       # Tunable parameters, line coordinates, thresholds, paths

tests/
├── unit/         # Deterministic coordinate tests, mock frame sources, in-memory SQLite
└── integration/  # Decoupled pipeline end-to-end simulation with fixture videos
```

### Encapsulation Rules:
- `src/capture/` must expose a uniform `FrameSource` interface yielding `(frame_id, timestamp, ndarray)`.
- `src/tripwire/` must only operate on anchor coordinates `(x, y)` and `track_id`, completely decoupled from image pixels or model weights.
- `src/storage/` must receive immutable dataclass event payloads and handle its own file system and database transactions.

---

## 5. Boundaries (Never-Touch Rules)

1. **Zero Secrets in Code**: Roboflow API keys, tokens, or credentials must strictly be loaded from `.env` or system environment variables. Never commit credentials to git.
2. **Mandatory Graphify Invariant**: Always query `graphify` before exploring files or refactoring dependencies. Keep `graphify-out/graph.json` synchronized via `graphify update .`.
3. **Zero Code Without Spec & Tickets**: Never implement features without approved specs in `.scratch/<feature-slug>/spec.md` and approved tracer-bullet tickets in `.scratch/<feature-slug>/issues/`.
4. **Zero Main-Thread Blocking**: The 30+ FPS capture loop is inviolable. Long operations belong in worker threads.
5. **No Speculative Complexity**: Implement strictly what ADRs specify. Do not introduce multi-class shoe detectors, complex message brokers, or external cloud services where SQLite and local files suffice.

---

## 6. Standard Delivery Workflow

Follow the lifecycle flow strictly:
```text
Search-First (graphify) ──> to-spec ──> to-tickets ──> User Approval ──> implement-spec & tdd ──> to-edit on changes ──> code-review ──> PR
```
