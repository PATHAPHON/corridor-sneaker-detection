# Handoff: Sneaker Model Retraining & Production Verification (Ticket 05)

**Feature**: `storage-and-evidence`  
**Date**: 2026-11-10  
**Status**: Ready for Retraining & Verification  
**Next Objective**: Execute fine-tuning on the merged sneaker dataset, validate against the mAP50 $\ge 0.80$ benchmark gate, update `models/yolo-sneaker.pt`, and verify live detection stability.

---

## 1. Executive Summary & Active State

In the preceding sessions, we completed:
1. **SQLite & Evidence Storage**: Implemented `EventRepository` (WAL mode), `EvidenceWriter`, and `DatasetExporter`.
2. **Tracker Stability & Reset**: Reconfigured ByteTrack (`track_buffer: 90`, `new_track_thresh: 0.50`, `person_confidence: 0.50`) and added `'r'` key reset.
3. **Hallway Dataset Curation**: Curated 13 real hallway crop images in `datasets/sneakers_live/` (11 train, 2 val) and verified 100% accurate ground-truth bounding boxes including edge cases (depth overlap in `07-00-37`, perspective tilt in `07-01-39`, motion blur in `07-01-13`).
4. **Architectural Invariant (ADR-0007)**: Documented ADR-0007 and Invariant 7 in `GLOSSARY.md`, establishing training-time data augmentation over runtime image enhancement filters.

All 34 tests pass (`uv run pytest`).

---

## 2. Grill-Me Consensus & Architectural Decisions

Following the interactive interview, the user established six non-negotiable decisions:

| Decision Area | Selected Strategy | Rationale & Impact |
| :--- | :--- | :--- |
| **1. Dataset Strategy** | **Merged Dataset** (Baseline 246 + Live Hallway 13) | Prevents catastrophic forgetting of universal sneaker shapes while adapting weights to black shoes on light tile floors. |
| **2. Base Weights & Epochs** | **Warm Start from `models/yolo-sneaker.pt` (30 Epochs)** | Fast convergence (~1 min on MPS), builds directly upon footwear features without starting from COCO scratch. |
| **3. Benchmark & Safety Gate** | **Enforce mAP50 $\ge 0.80$ Gate + Auto Backup** | Back up current model to `models/yolo-sneaker.backup.pt`. If mAP50 $\ge 0.80$, promote new weights; if not, keep original. |
| **4. Crossing Capture Trigger** | **Single-Frame Snapshot** | Preserve clean decoupled architecture at line crossing; avoid complex circular burst buffers. |
| **5. Low-Contrast / Blur Handling** | **Training-Time Data Augmentation (ADR-0007)** | Inject Mosaic (`1.0`), Scale (`0.5`), Brightness/Contrast Jitter (`hsv_v=0.4`, `hsv_s=0.7`) in training for zero runtime latency. |
| **6. Verification Mode** | **Before/After Visual Report + Live Video Test** | Show side-by-side detection improvements on real hallway crops, verify full test suite, and launch `src.main`. |

---

## 3. Step-by-Step Execution Playbook for Next Agent

### Step 1: Prepare Merged Dataset Configuration
Create `datasets/sneakers_merged/data.yaml` referencing both baseline and live images:
- Combine images or configure YOLO dataset path pointing to merged train/val sets.
- Ensure class remains strictly `0: sneaker`.

### Step 2: Execute Retraining with Tuned Augmentations
Run fine-tuning using Apple Silicon Metal (`mps`):
```bash
uv run python -m scripts.train_sneaker_model \
  --data datasets/sneakers_merged/data.yaml \
  --base-model models/yolo-sneaker.pt \
  --epochs 30 \
  --batch 16 \
  --mosaic 1.0 \
  --scale 0.5 \
  --project runs/detect \
  --name sneaker_yolo11n_merged
```

### Step 3: Run Benchmark Gate & Weight Export
```bash
uv run python -m scripts.evaluate_and_export \
  --weights runs/detect/sneaker_yolo11n_merged/weights/best.pt \
  --data datasets/sneakers_merged/data.yaml \
  --export models/yolo-sneaker.pt \
  --split val
```
- Verify `mAP50 >= 0.80`.
- Backup previous weights: `cp models/yolo-sneaker.pt models/yolo-sneaker.backup.pt` before overwriting.

### Step 4: Render Before/After Visual Verification Report
- Run inference with both old and new weights across the 13 hallway crops in `datasets/sneakers_live/images/train/`.
- Produce visual verification artifact showing detection boxes and confidence scores before vs after.
- Confirm both black sneakers are consistently detected without dropping to 0.

### Step 5: Mark Ticket 05 Complete & Update Graph
- Update `.scratch/storage-and-evidence/issues/05-sneaker-model-retraining-and-benchmark.md` status to `done`.
- Run `graphify update .`.
- Run `uv run pytest` to ensure zero regressions across all 34 tests.

---

## 4. Key File & Directory References
- **Feature Specification**: [.scratch/storage-and-evidence/spec.md](file:///Users/pat/Project/my-cv/.scratch/storage-and-evidence/spec.md)
- **Active Issue**: [.scratch/storage-and-evidence/issues/05-sneaker-model-retraining-and-benchmark.md](file:///Users/pat/Project/my-cv/.scratch/storage-and-evidence/issues/05-sneaker-model-retraining-and-benchmark.md)
- **Ground-Truth Labels**: [datasets/sneakers_live/](file:///Users/pat/Project/my-cv/datasets/sneakers_live/)
- **Baseline Dataset**: [datasets/sneakers/](file:///Users/pat/Project/my-cv/datasets/sneakers/)
- **Current Model**: [models/yolo-sneaker.pt](file:///Users/pat/Project/my-cv/models/yolo-sneaker.pt)
- **Architecture Record**: [docs/adr/0007-dark-sneaker-image-processing-and-training-augmentation.md](file:///Users/pat/Project/my-cv/docs/adr/0007-dark-sneaker-image-processing-and-training-augmentation.md)
- **Visual Label Report**: [verified_labels_report.md](file:///Users/pat/.gemini/antigravity/brain/db7d3848-d67b-46b0-b926-54a74e26c776/verified_labels_report.md)

---

## 5. Suggested Skills
- `tdd`: For running automated test suites and validation gate checks.
- `diagnosing-bugs`: If mAP50 fails the benchmark gate or training encounters gradient anomalies.
- `graphify`: To keep knowledge graph topology synchronized with `graphify update .`.
