# Handoff: Dark Sneaker Domain Adaptation, Dual-Gate Verification & Evidence Naming

**Feature**: `dark-sneaker-retraining`  
**Date**: 2026-11-10  
**Status**: Feature Complete & Verified  
**Active Model**: `models/yolo-sneaker.pt` (Backup at `models/yolo-sneaker.backup.pt`)  
**Test Suite**: 42/42 tests passing (`uv run pytest`)  
**Knowledge Graph**: 1100 nodes, 1770 edges, 104 communities (`graphify update .`)

---

## 1. What Was Completed in This Session

### 1.1 Specification & Tracer Tickets
- Superseded Ticket 05 from `storage-and-evidence` and created new feature spec [.scratch/dark-sneaker-retraining/spec.md](file:///Users/pat/Project/my-cv/.scratch/dark-sneaker-retraining/spec.md).
- Authored and completed 4 tracer-bullet tickets:
  - `01-manifest-dataset-merger-with-oversampling.md`: Manifest generation with 5x oversampling.
  - `02-adr0007-training-time-augmentation-pipeline.md`: Full ADR-0007 training augmentations.
  - `03-dual-gate-evaluation-backup-and-visual-report.md`: Dual-gate evaluation, auto-backup, and Before/After reporting.
  - `04-execute-retraining-promote-weights-and-verify.md`: Retraining execution, weight promotion, and verification.

### 1.2 Dataset Merger with 5x Oversampling (Ticket 01)
- Implemented `scripts/merge_datasets.py` and unit test `tests/unit/test_dataset_merger.py`.
- Generates `train.txt`, `val.txt`, `test.txt`, and `datasets/sneakers_merged/data.yaml` without duplicating image files on disk.
- Oversampled live hallway training crops by 5x (yielding 245 train images: 190 baseline + $11 \times 5$ live hallway), giving proper representation to low-contrast black shoes on reflective tile floors during mini-batch gradient updates.

### 1.3 ADR-0007 Augmentation Pipeline & 5 Visual Samples (Ticket 02)
- Upgraded `scripts/train_sneaker_model.py` and unit test `tests/unit/test_train_augmentation.py`.
- Configured hyperparameters matching ADR-0007:
  - Brightness/Contrast Jitter: `hsv_s=0.7`, `hsv_v=0.4`
  - Perspective Rotation: `degrees=10.0`
  - Leg Occlusion Cutout: `erasing=0.2`
  - Directional Flip & Distance Scale: `fliplr=0.5`, `scale=0.5`
  - Mosaic: `mosaic=1.0` (with `close_mosaic=10`)
- Built `scripts/visualize_augmentations.py` and rendered 5 side-by-side visual demonstration samples from real hallway crops (presented in artifact [ticket02_augmentation_samples.md](file:///Users/pat/.gemini/antigravity/brain/feed9219-1327-4a8d-9000-e8176dbd37ba/ticket02_augmentation_samples.md)).

### 1.4 Fine-Tuning Execution & Dual-Gate Promotion (Ticket 03 & 04)
- Executed 30-epoch warm-start fine-tuning on Apple Silicon Metal (`mps`).
- Evaluated candidate weights using `scripts/evaluate_and_export.py` and unit tests in `tests/unit/test_evaluate_dual_gate.py`:
  - **Gate 1 (Overall Validation mAP50)**: `0.7824 >= 0.75` (PASSED)
  - **Gate 2 (Hallway Ground-Truth Recall @ conf 0.40)**: **100.0% (21/21 sneakers detected)**, up from 52.4% baseline (PASSED)
  - **Confidence Boost**: Mean sneaker confidence increased from `0.584` to **`0.863`** (+27.9%)
  - **Inference Throughput**: **46.7 FPS** (Mean latency: `21.41 ms`), satisfying Invariant 1 (>30 FPS)
- Promoted weights to `models/yolo-sneaker.pt` with automatic backup at `models/yolo-sneaker.backup.pt`.
- Generated 13 Before/After comparison panels in `runs/detect/eval/comparisons/` and compiled visual report in artifact [before_vs_after_report.md](file:///Users/pat/.gemini/antigravity/brain/feed9219-1327-4a8d-9000-e8176dbd37ba/before_vs_after_report.md).

### 1.5 Evidence Chronological Naming & Real-Date Partitioning (Edit 02)
- Resolved user inquiry regarding image ordering and `1970-01-01` folders:
  - Updated `src/storage/evidence_writer.py` to accept `event_id: Optional[int] = None` and format filenames with zero-padded 5-digit prefixes (e.g. `00001_...`, `00071_...`), ensuring natural alphabetical order from oldest to newest.
  - Updated `_extract_date_str()` and `src/pipeline/coordinator.py` to map relative video timestamps (< 1e9) to current wall-clock date (`datetime.now().strftime("%Y-%m-%d")`), preventing `1970-01-01` folders.
  - Verified with unit tests in `tests/unit/test_evidence_writer.py` and integration tests in `tests/integration/test_storage_pipeline.py`.

### 1.6 Log Diagnostics & Field Behavior Analysis
- Analyzed DB events #52 through #71:
  - Events #54–#64: High-confidence detection (2 sneakers detected at 0.82–0.89 conf).
  - Events #65–#71: Diagnosed why Sneaker Count dropped to 0: full scene frame (`_full.jpg`) revealed pedestrian walked directly against camera lens (bounding box `1918x1067` on `1920x1080` frame), causing feet to fall below the camera's field of view (valid true negative for Lower-Body ROI).

---

## 2. Key Architecture & File References

- **Active Model Weights**: [models/yolo-sneaker.pt](file:///Users/pat/Project/my-cv/models/yolo-sneaker.pt)
- **Backup Model Weights**: [models/yolo-sneaker.backup.pt](file:///Users/pat/Project/my-cv/models/yolo-sneaker.backup.pt)
- **Feature Spec**: [.scratch/dark-sneaker-retraining/spec.md](file:///Users/pat/Project/my-cv/.scratch/dark-sneaker-retraining/spec.md)
- **Edit Records**:
  - [.scratch/dark-sneaker-retraining/edits/01-start-and-visual-samples.md](file:///Users/pat/Project/my-cv/.scratch/dark-sneaker-retraining/edits/01-start-and-visual-samples.md)
  - [.scratch/dark-sneaker-retraining/edits/02-real-date-and-db-id-naming.md](file:///Users/pat/Project/my-cv/.scratch/dark-sneaker-retraining/edits/02-real-date-and-db-id-naming.md)
- **Feedback Logs**:
  - [.scratch/dark-sneaker-retraining/feedback/01-start-and-visual-samples.md](file:///Users/pat/Project/my-cv/.scratch/dark-sneaker-retraining/feedback/01-start-and-visual-samples.md)
  - [.scratch/dark-sneaker-retraining/feedback/02-real-date-and-db-id-naming.md](file:///Users/pat/Project/my-cv/.scratch/dark-sneaker-retraining/feedback/02-real-date-and-db-id-naming.md)
- **Dataset Configuration**: [datasets/sneakers_merged/data.yaml](file:///Users/pat/Project/my-cv/datasets/sneakers_merged/data.yaml)
- **Training Script**: [scripts/train_sneaker_model.py](file:///Users/pat/Project/my-cv/scripts/train_sneaker_model.py)
- **Evaluation & Gate Script**: [scripts/evaluate_and_export.py](file:///Users/pat/Project/my-cv/scripts/evaluate_and_export.py)
- **Dataset Merger Script**: [scripts/merge_datasets.py](file:///Users/pat/Project/my-cv/scripts/merge_datasets.py)
- **Augmentation Visualizer**: [scripts/visualize_augmentations.py](file:///Users/pat/Project/my-cv/scripts/visualize_augmentations.py)
- **Pipeline Coordinator**: [src/pipeline/coordinator.py](file:///Users/pat/Project/my-cv/src/pipeline/coordinator.py)
- **Evidence Writer**: [src/storage/evidence_writer.py](file:///Users/pat/Project/my-cv/src/storage/evidence_writer.py)

---

## 3. Immediate Next Steps for Next Session

1. **Live Camera Deployment & Operational Verification**:
   - Run `uv run python -m src.main` with physical webcam to observe real-time crossings with the newly promoted weights.
   - Verify that new captured images in `output/captures/YYYY-MM-DD/` carry the `00001_...` sequence prefixes and group properly by date.
2. **Optional Next Feature**:
   - Audit Dashboard / Compliance Reporting UI or Web Viewer to view stored crossing events, timestamps, and evidence images from `data/events.db` and `output/captures/`.
   - Out-of-frame feet guard: Add an aspect ratio or bbox area sanity check (e.g., if person bbox height > 95% of frame height, log "Person too close to lens / feet out of frame" rather than strict footwear non-compliance).

---

## 4. Suggested Skills for Next Agent

- `lifecycle`: Always active for operational standards and Karpathy guidelines.
- `graphify`: Mandatory for dependency tracing (`graphify query`, `graphify update .`).
- `tdd`: For implementing any new features or UI components with red-green test cycles.
- `to-spec` & `to-tickets`: For authoring any new feature specs in `.scratch/` before touching production code.
