# Feature Spec: Dark Sneaker Domain Adaptation, Retraining & Dual-Gate Verification

## Problem Statement

During live corridor deployments, the baseline single-class Sneaker Detector (`0: sneaker`) frequently misses dark or all-black sneakers or alternates inconsistently between 0, 1, and 2 detections per pedestrian crossing. This failure stems from a severe domain gap between the baseline dataset (190 studio and web photographs with bright, uniform illumination) and real indoor hallway Lower-Body ROI crops (11 training and 2 validation images), where auto-exposure calibrates to high-reflectance light tile floors and renders dark footwear as low-contrast silhouettes subject to stride motion blur, perspective tilt, and leg depth occlusion. Furthermore, simply combining the two datasets at a 1:1 ratio leaves real hallway crops at a 17:1 disadvantage, and evaluating solely on overall validation mAP50 allows models to pass using studio accuracy while still failing on dark hallway footwear. Finally, per System Invariant 7 and ADR-0007, no runtime image enhancement filters (such as CLAHE or unsharp masking) may be added to the real-time capture or background worker pipeline.

## Solution

Deliver an end-to-end offline domain-adaptation, training-time augmentation, and dual-gate evaluation pipeline for the Sneaker Detector:
1. **Oversampled Manifest Dataset Merger**: Combine the baseline sneaker dataset with curated live hallway Lower-Body ROI crops using lightweight manifest files (`train.txt`, `val.txt`, `test.txt`) and a unified YOLO configuration without duplicating image binaries on disk. Apply configurable oversampling (default 5x repetition of live hallway training crops, yielding 55 hallway samples against 190 baseline samples) so each training epoch heavily weights real indoor lighting and floor reflections while preserving general sneaker morphology.
2. **ADR-0007 Training-Time Augmentation Pipeline**: Extend the fine-tuning workflow to warm-start from the existing Sneaker Detector weights for 30 epochs on Apple Silicon Metal (`mps`) with CUDA/CPU fallback, applying targeted training-time augmentations: brightness/contrast jitter (`hsv_s=0.7`, `hsv_v=0.4`), perspective rotation (`degrees=10.0`), occlusion cutout (`erasing=0.2`), horizontal flip (`fliplr=0.5`), mosaic (`mosaic=1.0`), and scale (`scale=0.5`).
3. **Dual Benchmark Gate & Safe Rollback Backup**: Upgrade the evaluation and export workflow to require passing two non-negotiable gates before promoting candidate weights:
   - **Gate 1 (Generalization Gate)**: Overall merged validation `mAP50 >= 0.80` to prevent catastrophic forgetting of general sneaker shapes.
   - **Gate 2 (Hallway Domain Recall Gate)**: Ground-truth sneaker recall $\ge 0.90$ across all 13 curated real hallway crops at the production confidence threshold (`0.40`).
   Before promoting passing weights, automatically back up existing production weights to a `.backup.pt` artifact; if either gate fails, abort promotion and preserve existing production weights untouched.
4. **Automated Before/After Visual Verification Report**: Automatically run inference with both the previous backup weights (`Before`) and the newly trained candidate weights (`After`) across all 13 real hallway crops, rendering side-by-side annotated visual comparison panels (`before_vs_after_<crop>.jpg`) and persisting quantitative detection counts and confidence deltas into a structured evaluation summary.

## User Stories

1. As a computer vision engineer, I want to merge the baseline sneaker dataset and the live hallway dataset using text manifests rather than copying image files, so that dataset preparation is instantaneous and avoids duplicating disk storage.
2. As a machine learning engineer, I want the dataset merger to oversample live hallway training images by a configurable multiplier (default 5x), so that the 11 hallway crops are not drowned out by the 190 studio images during mini-batch gradient updates.
3. As a machine learning engineer, I want validation and test manifests to remain un-duplicated (1x weight), so that evaluation metrics remain statistically unbiased.
4. As a machine learning engineer, I want the merged dataset configuration to enforce the single class `0: sneaker` invariant (Invariant 3), so that no multi-class label drift occurs.
5. As a system architect, I want all invariance to dark footwear, low contrast, and motion blur achieved strictly via training-time data augmentations rather than runtime preprocessing (Invariant 7 / ADR-0007), so that the real-time capture loop and background worker incur zero additional latency.
6. As a machine learning engineer, I want the training module to expose explicit hyperparameters for HSV saturation (`hsv_s=0.7`) and HSV value/brightness (`hsv_v=0.4`), so that the detector learns to recognize low-contrast black sneakers against bright tile floors.
7. As a machine learning engineer, I want the training module to apply rotation (`degrees=10.0`) and random erasing (`erasing=0.2`) alongside `mosaic=1.0`, `scale=0.5`, and `fliplr=0.5`, so that the detector remains accurate during foot swing tilt and partial leg-over-leg occlusion.
8. As a machine learning engineer, I want fine-tuning to warm-start from the existing Sneaker Detector weights for 30 epochs on `mps` (with CUDA/CPU fallback), so that training converges rapidly without losing pre-learned footwear features.
9. As a release engineer, I want the evaluation pipeline to enforce an overall merged validation gate of `mAP50 >= 0.80`, so that candidate models that suffer catastrophic forgetting on general sneakers are rejected.
10. As a release engineer, I want the evaluation pipeline to enforce a dedicated Hallway Domain Gate requiring $\ge 90\%$ ground-truth sneaker detection recall across all 13 real hallway crops at `conf=0.40`, so that a model cannot pass solely on studio images while failing on black hallway shoes.
11. As a reliability engineer, I want the export workflow to automatically back up the current production model weights before writing new weights, so that operators can roll back immediately if needed.
12. As a reliability engineer, I want the export workflow to abort without overwriting production weights if either the overall mAP50 gate or the hallway detection gate fails, so that degraded models never reach production.
13. As an audit operator, I want the evaluation script to generate side-by-side `Before vs After` annotated images for all 13 real hallway crops, so that I can visually inspect bounding box stability and confidence improvements on dark sneakers.
14. As an audit operator, I want the evaluation summary JSON to record per-crop and aggregate sneaker counts and mean confidence scores for both the baseline (`Before`) and retrained (`After`) models, so that improvements are quantitatively documented.
15. As a developer, I want deterministic unit tests covering manifest generation, oversampling ratios, augmentation argument forwarding, dual-gate pass/fail branching, backup creation, and side-by-side comparison rendering, so that the training and evaluation pipeline is verified without running slow full-epoch training during standard test runs.

## Implementation Decisions

### 1. Manifest-Based Dataset Merger with Domain Oversampling
- Introduce a dataset merge module and CLI utility that reads the baseline dataset splits and the curated live hallway dataset splits.
- Rather than copying image files, generate deterministic absolute-path manifest files (`train.txt`, `val.txt`, `test.txt`) and a `data.yaml` file inside the merged dataset directory.
- Verify that every image entry in the generated manifests has a corresponding YOLO `.txt` label file alongside it (or follows standard YOLO `images/` to `labels/` path resolution).
- Support a configurable `live_oversample_factor` (default `5`) applied strictly to the live hallway `train` split (producing $190 + 11 \times 5 = 245$ training entries per epoch), while keeping `val` ($56 + 2 = 58$ entries) and `test` splits at `1x`.

### 2. ADR-0007 Training-Time Augmentation Contract
- Enhance the sneaker model training interface and CLI to accept and forward ADR-0007 augmentation parameters directly to the YOLO trainer:
  - `hsv_h: float = 0.015`
  - `hsv_s: float = 0.7`
  - `hsv_v: float = 0.4`
  - `degrees: float = 10.0`
  - `fliplr: float = 0.5`
  - `erasing: float = 0.2`
  - `mosaic: float = 1.0`
  - `scale: float = 0.5`
- Default fine-tuning run parameters for domain adaptation: warm start from existing production sneaker weights, `epochs=30`, `batch_size=16`, `imgsz=640`, `close_mosaic=10`.
- Zero changes to runtime `FootwearInspector` image preprocessing (strictly honoring Invariant 7).

### 3. Dual-Gate Evaluation, Safe Backup & Promotion
- Extend the evaluation and export module with a two-stage verification gate:
  1. **Merged Validation Gate**: Evaluates `mAP50` on the specified validation split and checks `map50 >= min_map50` (default `0.80`).
  2. **Hallway Domain Recall Gate**: Runs inference at `conf=0.40` across all curated hallway images and compares predicted boxes against ground-truth YOLO label files using IoU $\ge 0.50$ matching. Computes `hallway_recall = matched_gt_boxes / total_gt_boxes` and checks `hallway_recall >= min_hallway_recall` (default `0.90`).
- **Safe Promotion Contract**:
  - If `gate_passed` is `True` (both gates pass): if the target production model file already exists, copy it to a `.backup.pt` sibling file before copying the new best checkpoint to the production path.
  - If `gate_passed` is `False`: do NOT overwrite the target production model file; raise a descriptive gate failure error (or exit non-zero in CLI) after writing the diagnostic evaluation summary and visual report.

### 4. Automated Before/After Hallway Visual Comparison
- During evaluation, load both the previous production model (from the production path or backup path) as the `Before` reference and the newly trained checkpoint as the `After` candidate.
- For each of the 13 curated hallway crop images, render a side-by-side composite JPEG (`Left: Before (count, confs)` vs `Right: After (count, confs)`) into the evaluation output directory.
- Record structured `before_vs_after` metrics in `eval_summary.json`, including total ground-truth boxes, total detected boxes before/after, hallway recall before/after, mean confidence before/after, and paths to the generated comparison images.

## Testing Decisions

- **Agreed Public Seams**:
  1. **Dataset Merger Seam**: Given temporary baseline and live hallway dataset directories, call the dataset merger and assert that `train.txt`, `val.txt`, and `data.yaml` are generated with exact oversampling counts (5x on live train, 1x on val) and valid YOLO label resolution.
  2. **Training Augmentation Seam**: Call the training entrypoint with mocked YOLO trainer and assert that all ADR-0007 augmentation arguments (`hsv_s=0.7`, `hsv_v=0.4`, `degrees=10.0`, `erasing=0.2`, `fliplr=0.5`, `mosaic=1.0`, `scale=0.5`) are forwarded accurately.
  3. **Dual-Gate Evaluation & Backup Seam**: Call `evaluate_and_export` under three scenarios:
     - Both gates pass (`mAP50 >= 0.80` and `hallway_recall >= 0.90`) -> backs up existing `.pt` to `.backup.pt`, promotes new weights, writes side-by-side comparison images and `eval_summary.json`.
     - Overall `mAP50 < 0.80` -> aborts promotion, preserves original production weights untouched.
     - Overall `mAP50 >= 0.80` but `hallway_recall < 0.90` -> aborts promotion, preserves original production weights untouched.
  4. **Production Weight Integration Seam**: Run the existing sneaker model and footwear unit/integration test suites against the newly promoted production weights to confirm zero regressions and stable dark-sneaker detection on real hallway crops.

## Out of Scope

- Runtime image enhancement filters (CLAHE, gamma correction, unsharp masking, histogram equalization) in the capture or worker threads (prohibited by Invariant 7 and ADR-0007).
- Multi-frame circular burst capture buffers at tripwire crossing (prohibited by ADR-0007).
- Multi-class footwear classification (boots, sandals, dress shoes, slippers) — strictly single class `0: sneaker` (Invariant 3).
- Automated background retraining loops triggered inside the live video process.

## Further Notes

- Complies strictly with ADR-0006 (Fine-Tuned Single-Class YOLO11n Sneaker Detector) and ADR-0007 (Dark Footwear Robustness via Training-Time Augmentation vs Real-Time Preprocessing).
