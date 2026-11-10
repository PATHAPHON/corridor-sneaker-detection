# Feature Spec: Core Video and Tracking Pipeline

## Problem Statement

The system requires a robust, real-time computer vision monitoring pipeline that processes video input feeds at 30+ FPS, tracks pedestrians moving across a corridor, detects when an individual enters by crossing a virtual tripwire line, isolates the pedestrian's lower-body foot region, and inspects their footwear using a fine-tuned single-class sneaker detector.

Currently, the sneaker detector model is trained and exported, but no unified runtime video capture, multi-object tracking, tripwire geometric calculation, ROI extraction, or decoupled concurrent pipeline exists. Directly coupling heavy model inference and image/database I/O into the video acquisition loop would cause severe frame drops below the required 30 FPS, leading to lost tracks and missed crossings.

## Solution

Implement a two-stage decoupled video pipeline:
1. Stage 1 (Real-Time Acquisition & Tracking Thread): Captures frames from a uniform FrameSource abstraction, detects persons using YOLO11n COCO class 0, maintains stable tracking IDs using ByteTrack, extracts ground anchor points at the bottom-center of the person bounding boxes, evaluates directional entry crossings across a virtual tripwire using LineZone with anti-bounce cooldown, and non-blockingly enqueues crossing events into a bounded queue (`maxsize=20`).
2. Stage 2 (Background Event Inspection Worker): Dequeues crossing event tasks, extracts a lower-body ROI (bottom 30% of height with 10% horizontal padding), runs inference with the fine-tuned sneaker detector model (`models/yolo-sneaker.pt` at confidence $\ge 0.40$), and prepares annotated visual evidence and structured records for persistent storage.

## User Stories

1. As a security operator, I want the video capture system to accept live webcams, pre-recorded video files, and synthetic test streams through a single uniform interface, so that the pipeline can run identically in production and automated CI test environments.
2. As a security operator, I want the system to continuously detect persons in the camera frame using an efficient YOLO11 Nano model, so that pedestrian presence is recognized with minimal CPU and GPU latency.
3. As a monitoring system administrator, I want persistent multi-object tracking via ByteTrack across consecutive frames, so that each pedestrian retains a unique, stable tracking ID even during brief occlusions or direction changes.
4. As a facility manager, I want the ground-contact anchor point to be calculated strictly at the bottom-center of each person's bounding box, so that tripwire crossing accurately represents floor plane transit rather than upper body tilt or centroid shifting.
5. As an entry control supervisor, I want to define a virtual tripwire line between two coordinates across the corridor, so that the boundary between entry and exit zones is clearly demarcated.
6. As a facility manager, I want the system to trigger footwear inspection only when a pedestrian crosses in the entry direction ($A \to B$), so that computational resources and disk space are not wasted on departing individuals.
7. As an entry control supervisor, I want exit crossings ($B \to A$) to be silently ignored without triggering sneaker inference, so that the pipeline throughput remains dedicated to entries.
8. As a monitoring system administrator, I want exit crossings ($B \to A$) to reset the track's tripwire cooldown, so that an individual who leaves and re-enters later is properly inspected on their second arrival.
9. As a security operator, I want an anti-bounce debounce cooldown of 2.0 seconds per tracking ID for entry crossings, so that a person lingering, hesitating, or rocking on the line does not generate repeated duplicate trigger events.
10. As a footwear compliance auditor, I want the system to extract an event-triggered lower-body ROI corresponding to the bottom 30% of the bounding box height with 10% horizontal padding, so that the detector focuses precisely on shoes without clipping feet mid-stride.
11. As a footwear compliance auditor, I want the extracted lower-body ROI to be evaluated by the fine-tuned single-class sneaker detector (`models/yolo-sneaker.pt`) with a confidence threshold $\ge 0.40$, so that sneakers are reliably identified while non-sneakers or bare feet are marked as non-compliant.
12. As a system engineer, I want the real-time capture and tracking loop to execute on a dedicated thread that never blocks on sneaker inference, image compression, or disk writes, so that real-time video processing strictly maintains 30+ FPS.
13. As a system engineer, I want the inter-thread communication to utilize a bounded queue with a maximum capacity of 20 tasks, so that memory usage remains bounded and predictable even during extreme crowd entry bursts.
14. As an operator running automated testing, I want a synthetic frame source that generates deterministic geometric pedestrians crossing the tripwire, so that pipeline integration tests verify tracking, crossing, and inspection end-to-end without requiring physical cameras or video files.
15. As a system operator, I want a clean and graceful shutdown mechanism that terminates capture, waits for pending queue items to finish processing, and releases hardware resources cleanly upon receiving exit signals.

## Implementation Decisions

- **Frame Source Abstraction**: Define a uniform frame source interface yielding sequential frame IDs, timestamps, and pixel arrays. Provide implementations for camera devices, video files, and deterministic synthetic frame generators for headless testing.
- **Pedestrian Tracking & Ground Anchor Formulation**: Person detector filters YOLO11 Nano strictly to COCO Class 0 (`person`). ByteTrack associates detections into persistent tracks. The ground anchor point is formulated as bottom-center $P_{anchor} = ((x_{min} + x_{max}) / 2, y_{max})$, representing floor plane contact.
- **Directional Tripwire & Cooldown Engine**: Use supervision LineZone for 2D vector cross-product boundary evaluation. Line crossing from vector left ($Zone\ A$) to vector right ($Zone\ B$) constitutes an entry event. Implement an in-memory timestamped debounce map per track ID with a default 2.0-second cooldown window. Reverse transit ($B \to A$) resets the cooldown without queuing inspection tasks.
- **Footwear ROI Extraction & Sneaker Inference**: When an entry crossing triggers, compute the lower-body ROI coordinates: top coordinate set at $y_{max} - 0.30 \times (y_{max} - y_{min})$, left and right coordinates padded by $10\%$ width clamped to frame boundaries. Pass the cropped ROI to the fine-tuned sneaker YOLO11n detector (`models/yolo-sneaker.pt`). Sneaker detections with confidence $\ge 0.40$ are recorded with their bounding box and confidence score.
- **Decoupled Concurrency & Queue Policy**: Decouple the pipeline into a producer thread (capture, detection, tracking, tripwire evaluation) and a consumer worker thread (ROI crop, sneaker inference, visual evidence generation). Tasks are passed via a bounded in-memory queue with `maxsize=20`. If the queue is saturated, incoming events are dropped with a warning log, guaranteeing the capture thread never blocks.

## Testing Decisions

- **Public Seam 1 (High-Level End-to-End Pipeline)**: Test the full pipeline coordinator using a synthetic frame generator that simulates a person walking across the virtual line from Zone A to Zone B. Verify that the pipeline produces exactly one crossing event task, processes the footwear ROI, runs sneaker inference, and drains the bounded queue cleanly.
- **Public Seam 2 (Deterministic Tripwire Geometry)**: Unit test the tripwire engine with synthetic coordinate trajectories passing $A \to B$ (triggers crossing), $B \to A$ (silently dropped, resets cooldown), lingering coordinates within the cooldown window (suppressed), and post-cooldown crossings (triggers again).
- **Public Seam 3 (ROI Extraction Mathematics)**: Unit test the lower-body ROI extractor across edge cases including boundary clamping (person near frame edges), zero-sized boxes, and verifying exact bottom 30% height and 10% horizontal padding calculations.
- **Public Seam 4 (Bounded Queue & Backpressure Invariant)**: Concurrency unit tests verifying that worker queue instantiation enforces `maxsize=20`, drops or warns gracefully on full queue without blocking caller thread, and terminates cleanly on shutdown signals.

## Out of Scope

- Multi-class footwear classification (boots, sandals, high heels, dress shoes).
- Cloud messaging brokers, Kafka, or distributed queues (in-process Python threading and SQLite WAL suffice).
- Web dashboard or streaming HTTP server for live preview (GUI HUD or headless processing only).
- Database persistence implementation (covered in subsequent storage feature).

## Further Notes

- Model weight paths and default line coordinates are externalized in configuration models to prevent hardcoding.
- Apple Silicon Metal (`mps`) acceleration is auto-detected for both person detection and sneaker detection with automatic fallback to CPU.
