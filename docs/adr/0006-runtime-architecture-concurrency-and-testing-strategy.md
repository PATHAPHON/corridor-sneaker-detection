# ADR-0006: Runtime Architecture, Concurrency Model, and Testing Strategy

**Date**: 2026-11-10
**Status**: accepted
**Deciders**: Pat (Developer), AI Assistant

## Context

The system combines real-time video capture and object tracking (30+ FPS) with heavier downstream tasks (footwear inference, JPEG encoding, disk I/O, SQLite writes).

Running all operations synchronously inside the main capture loop creates frame drops, breaks ByteTrack association across skipped frames, and causes pipeline latency spikes during crossing events.

Additionally, to verify system behavior (crossing detection, directional logic, anti-bounce, database writes) reliably via automated CI/tests, the system requires an architecture decoupled from live hardware webcams.

## Decision

We establish a **Two-Stage Decoupled Pipeline (Producer-Consumer via Queue)** with strict testability patterns:

### 1. Runtime Tech Stack
- **Runtime**: Python 3.11+
- **Core Libraries**:
  - `ultralytics` (YOLO11 Nano `yolo11n.pt` for person + fine-tuned `models/yolo-sneaker.pt` for sneaker detection)
  - `supervision` (ByteTrack, LineZone, visual annotators)
  - `opencv-python` (video I/O, frame slicing, drawing)
  - `pyyaml` (configuration parsing)
  - `pytest` & `pytest-mock` (testing harness)
  - `sqlite3` (built-in standard library with WAL mode enabled)
- **Hardware Acceleration**: Auto-detect `mps` (Apple Silicon Metal Performance Shaders), fallback to `cpu` or `cuda`.
- **Dataset & Model Training Path**:
  - Exported YOLO sneaker dataset location: `datasets/sneakers/data.yaml` (single class `0: sneaker`).
  - Training script fine-tunes `yolo11n.pt` with `mosaic=1.0` and `scale=0.5` augmentations and outputs `models/yolo-sneaker.pt`.

### 2. Concurrency Architecture (Two-Stage Decoupled)

```text
[Camera / Video File]
       │ (30 FPS)
       ▼
┌─────────────────────────────────────────────────────────┐
│ Stage 1: Main Video Thread (Real-Time Tracker & HUD)    │
│  - VideoCapture read                                    │
│  - YOLO11n person detection + ByteTrack update          │
│  - Supervision LineZone evaluation                      │
│  - If A → B crossing detected:                          │
│      enqueue(CrossingEventTask) -> Event Queue          │
│  - Render debug HUD & cv2.imshow                        │
└──────────────────────────┬──────────────────────────────┘
                           │ Event Queue (bounded queue)
                           ▼
┌─────────────────────────────────────────────────────────┐
│ Stage 2: Background Event Worker Thread                 │
│  - Dequeue CrossingEventTask                            │
│  - Crop lower-body ROI (bottom 35%)                     │
│  - Run Footwear YOLO inference                          │
│  - Render bounding boxes on crop image                  │
│  - Save `{timestamp}_{track_id}_full.jpg` & `_crop.jpg` │
│  - Persist record to SQLite (`crossing_events`)         │
└─────────────────────────────────────────────────────────┘
```

- **Thread Isolation**: The main capture thread never waits on footwear inference or disk writes.
- **Queue Overflow Protection**: Bounded queue size (max 20 pending events) prevents memory spikes during rapid crowd bursts.

### 3. Testing Strategy & Testability Seams

- **Mockable Video Source**: Abstract video input behind a `FrameSource` interface:
  - `CameraFrameSource(device_index)` for live MacBook webcam.
  - `VideoFileFrameSource(file_path)` for recorded `.mp4` test fixtures.
  - `SyntheticFrameSource(generator)` for unit-testing tracking and line crossing without raw video decoding.
- **In-Memory Storage for Unit Tests**: Tests configure SQLite using `:memory:` or temporary directories (`tmp_path`).
- **Deterministic Coordinate Testing**: Line-crossing logic (`LineZone`, direction vector, and cooldown) must be testable using synthetic coordinate sequences without loading neural network weights.

## Alternatives Considered

### Alternative 1: Single-Threaded Synchronous Pipeline
- **Pros**: Simpler control flow, no threading or queues.
- **Cons**: Footwear model inference (~30-50ms) plus saving 2 JPEG images (~20-40ms) stalls video stream for 50-90ms per crossing event, causing video lag and lost tracking tracks.
- **Why not**: Real-time 30 FPS target cannot be maintained during person crossings.

### Alternative 2: Multiprocessing (`multiprocessing.Process`)
- **Pros**: Bypasses Python Global Interpreter Lock (GIL).
- **Cons**: High memory overhead duplicating model weights across process memory; IPC serialization of large frame arrays is slow.
- **Why not**: PyTorch/Ultralytics and OpenCV release GIL during C++/MPS inference. Standard threading is sufficient and shares model weights efficiently.

## Consequences

### Positive
- **Guaranteed 30+ FPS**: Main video tracking loop runs uninterrupted regardless of footwear processing time or disk write speed.
- **High Testability**: Decoupled frame sources allow 100% automated regression testing without a physical webcam.
- **Robustness**: Background errors in image saving or DB writes do not crash the primary tracking display.

### Negative
- **Asynchronous Latency**: Database records and saved crops appear a few milliseconds after the visual line crossing in the preview window.

### Risks
- **Sudden Shutdown During Processing**: If the user exits the app while events remain in the queue, some events might not finish writing.
  - *Mitigation*: Implement graceful shutdown with `queue.join(timeout=3.0)` to drain remaining events before process exit.

