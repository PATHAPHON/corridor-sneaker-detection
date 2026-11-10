# Edit 01: Implement Retraining Pipeline and Generate 5 Visual Augmentation Samples

**Status**: done

## Rationale & Impact
The user explicitly confirmed approval to proceed ("เริ่ม") and requested 5 visual example images illustrating Ticket 02 training-time data augmentations applied to hallway crops ("ขอดูภาพ tickets 2 ด้วย ยกตัวอย่าง 5 รูป"). This edit delivers:
1. Manifest dataset merger script `scripts/merge_datasets.py` and unit test `tests/unit/test_dataset_merger.py` (Ticket 01).
2. Augmentation upgrades in `scripts/train_sneaker_model.py` and an augmentation visualizer script `scripts/visualize_augmentations.py` producing 5 side-by-side augmented sample images saved to disk and presented to the user (Ticket 02).
3. Dual-gate benchmark evaluator and backup workflow in `scripts/evaluate_and_export.py` (Ticket 03).
4. Retraining execution on Metal (`mps`) and production model promotion (Ticket 04).

## Target Files
- `scripts/merge_datasets.py`
- `tests/unit/test_dataset_merger.py`
- `scripts/visualize_augmentations.py`
- `scripts/train_sneaker_model.py`
- `tests/unit/test_train_augmentation.py`
- `scripts/evaluate_and_export.py`
- `tests/unit/test_evaluate_dual_gate.py`

## Planned Changes
- Implement `scripts/merge_datasets.py` to create `train.txt`, `val.txt`, `test.txt`, and `data.yaml` with 5x hallway oversampling.
- Implement `scripts/visualize_augmentations.py` applying ADR-0007 transforms (`hsv_s=0.7`, `hsv_v=0.4`, `degrees=10.0`, `erasing=0.2`, `mosaic`, `scale=0.5`) to generate 5 real hallway crop demonstration images.
- Upgrade `scripts/train_sneaker_model.py` to forward full ADR-0007 augmentation arguments.
- Upgrade `scripts/evaluate_and_export.py` to enforce dual benchmark gates (`mAP50 >= 0.80` and `hallway_recall >= 0.90`), auto-backup existing weights, and generate Before/After comparisons.
- Run tests and update knowledge graph.

## Acceptance Criteria
- [x] Manifest dataset merger generates valid manifests and passes unit tests.
- [x] 5 visual example images demonstrating Ticket 02 augmentations are generated and presented.
- [x] `train_sneaker_model.py` supports all ADR-0007 parameters and passes unit tests.
- [x] `evaluate_and_export.py` enforces dual gates, auto-backup, and Before/After reporting.
- [x] Full pytest test suite passes cleanly.
