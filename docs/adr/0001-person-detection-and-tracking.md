# ADR-0001: Person Detection and Multi-Object Tracking Pipeline

**Date**: 2026-11-10
**Status**: accepted
**Deciders**: Pat (Developer), AI Assistant

## Context

The system must continuously process an RTSP/video camera feed in real-time (target 30+ FPS) to identify human beings walking through an entry point and track their movements persistently across consecutive frames. Without robust multi-object tracking, individuals crossing a tripwire cannot be uniquely identified or associated with their footwear analysis.

Core constraints:
- Real-time performance on edge or modest GPU/CPU hardware.
- High accuracy for bounding pedestrians under varying distances and slight crowd overlap.
- Ability to reliably extract the ground-contact point (feet level) for subsequent tripwire triggering.

## Decision

We will use **YOLO11 Nano (`yolo11n.pt`)** coupled with **ByteTrack** (via the `supervision` library):

1. **Detector (YOLO11 Nano - `yolo11n.pt`)**:
   - Single chosen model: `yolo11n.pt` filtered strictly to Class 0 (`person`).
   - **Architecture & Efficiency**: Has 2.6M parameters (22% fewer than YOLOv8n's 3.2M) and requires only 6.5B FLOPs (vs 8.7B FLOPs), resulting in lower CPU/GPU latency.
   - **Higher Accuracy**: Achieves 39.5 mAP on COCO (+2.2 mAP higher than YOLOv8n) thanks to C3k2 and C2PSA spatial attention blocks.
   - **Zero Retraining**: COCO dataset pretrained weights detect pedestrians out-of-the-box.
   - **Frame Budget**: Retains 30-60+ FPS real-time throughput with ample headroom for downstream footwear processing.
2. **Tracker**: `supervision.ByteTrack` assigns and maintains a stable `track_id` for each detected person across frames, matching high-confidence detections first and recovering tracks using low-confidence detections during occlusion.
3. **Ground Anchor Point**: The representative ground location of each tracked person is calculated as the bottom-center of their bounding box:
   $$P_{anchor} = \left(\frac{x_{min} + x_{max}}{2}, y_{max}\right)$$
   This point reflects the contact zone with the floor plane and feeds into the virtual line crossing calculator.

## Alternatives Considered

### Alternative 1: YOLOv8 Nano (`yolov8n.pt`)
- **Pros**: Mature, widely tested in production environments since 2023.
- **Cons**: 3.2M parameters and 8.7B FLOPs with lower mAP (37.3 vs 39.5) compared to YOLO11n.
- **Why not**: YOLO11n is strictly superior across all metrics (higher accuracy, fewer parameters, lower FLOPs) and uses the exact same `ultralytics` Python API.

### Alternative 1: YOLO Small / Medium (`YOLOv8s` / `YOLOv8m`)
- **Pros**: Marginally higher mAP on distant or partially occluded pedestrians.
- **Cons**: 3x to 8x higher parameter count (11M-25M parameters), halving frame rates on non-GPU setups.
- **Why not**: For indoor entry/hallway monitoring, persons occupy a significant portion of the frame; Nano provides sufficient recall (>95%) while saving compute.

### Alternative 2: YOLO-Pose (Human Pose Estimation)
- **Pros**: Directly detects ankle and foot keypoints (`left_ankle`, `right_ankle`), giving exact ground positions.
- **Cons**: Increases inference latency by ~30-35% compared to standard object detection.
- **Why not**: Bottom-center bounding box $(x_{center}, y_{max})$ provides sufficient precision for tripwire crossing at substantially higher throughput.

### Alternative 3: Background Subtraction + Optical Flow / Contour Tracking
- **Pros**: Extremely low compute footprint, runs on legacy CPUs without GPU acceleration.
- **Cons**: Fails severely with dynamic lighting changes, cast shadows, and people crossing close to each other.
- **Why not**: High false positive rate and lacks semantic understanding of pedestrians.

## Consequences

### Positive
- **High Throughput**: YOLOv8n/v11n easily sustains 30-60+ FPS on edge hardware.
- **Persistent Identification**: ByteTrack maintains ID consistency even during temporary occlusions or crossings.
- **Clear Decoupling**: Tracking outputs a clean stream of `(track_id, bbox, anchor_point)` tuples independent of downstream shoe detection.

### Negative
- **Anchor Approximation**: Bottom-center bounding box approximates feet position and may deviate slightly if a person is walking at an extreme tilt or jumping.

### Risks
- **ID Switching in Crowds**: Severe overlapping can occasionally flip track IDs.
  - *Mitigation*: Tune ByteTrack `track_thresh` and `match_thresh`, and implement a cooldown window on triggered events.

