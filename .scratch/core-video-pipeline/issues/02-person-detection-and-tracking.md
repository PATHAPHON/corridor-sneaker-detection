# 02: Person Detection, ByteTrack Tracking, and Ground Anchor Formulation

**What to build:** Real-time pedestrian detection filtered strictly to COCO Class 0 (person) utilizing pretrained YOLO11 Nano weights, integrated with ByteTrack multi-object tracking to maintain stable track IDs across consecutive frames, and computing the floor-plane Ground Anchor Point at the bottom-center of each tracked bounding box.

**Blocked by:** 01: Uniform Frame Source Abstraction

**Status:** done

- [x] Person detector runs YOLO11 Nano inference and filters output exclusively to person class detections with configurable confidence threshold
- [x] Multi-object tracking integrates ByteTrack to assign and preserve persistent track IDs across frames
- [x] Ground anchor point calculation accurately derives the bottom-center floor contact coordinate for every active track
- [x] Hardware acceleration automatically detects Apple Silicon Metal (MPS), falling back to CUDA or CPU
- [x] Unit tests verify anchor point mathematics, confidence filtering, and tracking persistence across simulated detections
