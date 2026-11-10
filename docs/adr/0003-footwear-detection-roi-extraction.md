# ADR-0003: Lower-Body ROI Extraction and Sneaker Detection

**Date**: 2026-11-10
**Status**: accepted
**Deciders**: Pat (Developer), AI Assistant

## Context

Running full-frame shoe detection continuously at 30 FPS causes unnecessary GPU/CPU saturation and false positives from floor patterns or background clutter, as shoes occupy a small pixel area in a 1080p wide scene.

Furthermore, supporting every possible footwear morphology (flip-flops, knee-high boots, loafers, heels) introduces inter-class ambiguity and burdensome manual dataset labeling. Restricting the inspection scope strictly to **Sneakers (`sneaker`)** allows leveraging the `Sneakers` subset from the Kaggle Shoe Dataset (`noobyogi0100/shoe-dataset`) combined with Web Few-Shot Auto-Box tools (Roboflow Auto-Label / T-Rex Label), eliminating manual bounding box annotation while achieving high precision.

The system requires:
1. An event-triggered, high-resolution lower-body inspection step when the tripwire fires (A → B).
2. A single-class YOLO11 Nano detector (`0: sneaker`, saved at `models/yolo-sneaker.pt`) trained via auto-labeled YOLO dataset in `datasets/sneakers/`.
3. Visual evidence saving an annotated crop of the feet with bounding boxes and detection confidence overlays.

## Decision

We will use an **Event-Triggered Lower-Body ROI Extraction** followed by a **Fine-Tuned Sneaker YOLO11n Detector (`models/yolo-sneaker.pt`) with Annotated Evidence Storage**:

1. **ROI Extraction (Spatial Crop for Sneaker Zone)**:
   - When Track ID $k$ triggers a line crossing event (A → B) at frame $t$, take the person's bounding box $[x_{min}, y_{min}, x_{max}, y_{max}]$.
   - Calculate the lower foot and ankle zone (bottom 30% of person height):
     $$y_{roi\_top} = y_{max} - 0.30 \times (y_{max} - y_{min})$$
     $$ROI = \text{frame}[y_{roi\_top}:y_{max}, \max(0, x_{min} - 0.10 \cdot W):\min(W_{frame}, x_{max} + 0.10 \cdot W)]$$
   - **Why 30% height**: Tightly frames the ankle-and-foot region where sneakers sit without excess upper-leg background.
   - **Why 10% horizontal margin**: Prevents clipping sneakers extended mid-stride.

2. **Single-Class Sneaker Detector (`0: sneaker`) & Auto-Box Training Pipeline**:
   - **Dataset Preparation**: Use the `Sneakers` subset from Kaggle (`noobyogi0100/shoe-dataset`) alongside sample webcam foot crops. Generate bounding boxes via Web Few-Shot Auto-Box (Roboflow Auto-Label or T-Rex Label by drawing 2–3 example boxes and auto-labeling the rest) and export in YOLO format to `datasets/sneakers/`.
   - **Model Fine-Tuning**: Fine-tune `yolo11n.pt` on `datasets/sneakers/data.yaml` with `mosaic=1.0` and `scale=0.5` augmentations enabled so close-up sneaker photos generalize to smaller sneaker scales inside the ROI crop. Export trained weights to `models/yolo-sneaker.pt`.
   - **Inference Output**: Detects sneakers under single class `0: sneaker`, outputting bounding boxes, detected count (0, 1, or 2), and confidence scores.
   - **Threshold**: Default confidence threshold at `0.40`. If no sneakers are detected above threshold (e.g. barefoot, socks, or non-sneaker footwear), flag as `shoes_detected = FALSE`.

3. **Annotated Image Evidence**:
   - The saved cropped image evidence (`{timestamp}_{track_id}_crop.jpg`) will be rendered with drawn bounding boxes, label, and confidence score (e.g. `[sneaker: 0.93]`).
   - Enables operators to instantly verify whether sneakers were detected on both feet without inspecting raw coordinates.

## Alternatives Considered

### Alternative 1: Multi-Style Footwear Detection (Boots, Flip-flops, Sandals, Loafers)
- **Pros**: Detects any type of shoe.
- **Cons**: Requires annotating 6x more data and struggles with thin flip-flops or tall boots.
- **Why not**: Focusing exclusively on `sneaker` cuts dataset preparation by >80% and yields much higher auto-labeling and detection accuracy.

### Alternative 2: Manual Bounding Box Labeling from Scratch
- **Pros**: Full manual control over every box coordinate.
- **Cons**: Time-consuming, tedious manual labor across hundreds of images.
- **Why not**: Few-shot web auto-labeling (drawing 2–3 boxes in Roboflow / T-Rex Label) produces clean bounding boxes for sneakers automatically in minutes.

### Alternative 3: Full-Frame Continuous Sneaker Detection
- **Pros**: Detects sneakers at every frame without waiting for line crossing.
- **Cons**: Severe frame-rate drop; high false positives from background clutter.
- **Why not**: Waste of compute; sneaker inspection is only required at the decision boundary (the virtual line).

## Consequences

### Positive
- **Zero Tedious Labeling**: Web auto-box tools annotate the `Sneakers` dataset after 2–3 visual examples.
- **Compute Optimization**: Sneaker detector only executes once per person crossing in the background worker thread, keeping the main video pipeline at 30+ FPS.
- **Higher Resolution & Accuracy**: Cropping focuses pixels directly on the ankles/feet, and Mosaic/Scale augmentation bridges the gap between close-up dataset images and ROI crops.

### Negative
- **Domain Gap from Studio Photos**: Pure studio sneaker photos have clean backgrounds compared to hallway floors.
  - *Mitigation*: Enable YOLO `mosaic=1.0` and `scale=0.5` augmentations during training, and optionally mix 20–30 real ROI crops captured from the MacBook webcam into the auto-label batch.

### Risks
- **Floor Glare / Dark Sneakers**: Low contrast on dark flooring can suppress detection confidence.
  - *Mitigation*: Maintain adequate corridor lighting ($\ge 200\text{ lux}$) or apply CLAHE contrast normalization on the cropped ROI if needed.
