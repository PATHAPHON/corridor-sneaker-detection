# ADR-0007: Dark Footwear Robustness via Training-Time Augmentation vs Real-Time Preprocessing

**Date**: 2026-11-10
**Status**: accepted
**Deciders**: Engineering Team, System Architect

## Context

In production hallway and corridor deployments, pedestrians frequently wear dark or all-black sneakers while walking across high-reflectance, light-colored tile floors under standard indoor lighting. Cameras with auto-exposure calibrate for the dominant room illumination, causing dark footwear to render as low-contrast, underexposed silhouettes lacking fine edge, seam, or lace textures. Additionally, the human gait cycle introduces significant motion blur during the swing phase (when a foot accelerates forward).

Initial testing revealed that base sneaker models fine-tuned purely on well-lit studio photographs frequently miss dark sneakers or alternate erratically between 0 and 1 detections on live video. We evaluated two potential architectural interventions:
1. Real-time image preprocessing (e.g. CLAHE, unsharp masking, gamma stretching) applied to foot crops in the live capture/inference pipeline.
2. Training-time data augmentation (e.g. Mosaic, HSV-V/HSV-S brightness and contrast jitter, scale variations, and simulated motion blur) combined with fine-tuning on real corridor samples.

## Decision

We decide to:
1. **Rely entirely on training-time data augmentation and dataset curation** to make the YOLO11n sneaker detector invariant to low contrast, indoor shadows, and motion blur.
2. **Keep the real-time inference pipeline clean and free of runtime image enhancement filters**, maintaining zero additional latency overhead on the video capture and worker threads.
3. **Maintain a single-frame crossing snapshot trigger** at the tripwire crossing rather than implementing multi-frame burst capture buffers.

## Alternatives Considered

### Alternative 1: Real-Time CLAHE (Contrast Limited Adaptive Histogram Equalization)
- **Pros**: Directly amplifies local contrast in dark shoe regions before feeding the image into YOLO inference.
- **Cons**: Adds CPU/GPU compute latency (~5–12 ms per crop) in the worker thread, amplifies sensor noise in dim conditions, and can introduce high-frequency pixel artifacts that degrade neural network confidence.
- **Why not**: The detection network can achieve equal or superior invariance if trained on augmented data, avoiding unnecessary runtime computation.

### Alternative 2: Multi-Frame Burst Capture with Laplacian Sharpness Selection
- **Pros**: Captures 3–5 frames during a crossing event and selects the frame with highest edge sharpness (lowest motion blur).
- **Cons**: Requires circular frame buffering, multi-frame storage overhead, and asynchronous peak-sharpness evaluation logic that complicates the decoupled capture pipeline.
- **Why not**: The user and system prioritize pipeline simplicity and zero capture latency. Training the detector to recognize slightly blurred or stride-occluded sneakers removes the need for burst buffering.

## Consequences

### Positive
- **Zero Runtime Overhead**: No image preprocessing transforms are injected into the 30+ FPS capture loop or background worker thread.
- **Robust Model Invariance**: The detector learns generalized feature representations robust to varying lighting, dark footwear, and stride motion.
- **Architecture Simplicity**: Keeps `FootwearDetector` and `PipelineCoordinator` focused solely on ROI extraction and model forward passes.

### Negative
- **Training Complexity**: Requires careful tuning of YOLO augmentation hyperparameters (`mosaic=1.0`, `scale=0.5`, `hsv_v=0.4`, `hsv_s=0.7`) to prevent training instability.
- **Annotation Diligence**: Ground-truth training labels must include challenging edge cases (motion blur, perspective tilt, overlapping depth) as verified in dataset curation.

### Risks & Mitigations
- **Risk**: Extreme motion blur during rapid running might still challenge single-frame detection.
- **Mitigation**: The background worker saves full-resolution evidence crops for continuous active learning; subsequent model iterations can incorporate any persistent failure cases.
