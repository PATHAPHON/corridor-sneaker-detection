# Feedback 01: Start Implementation and Request 5 Visual Augmentation Samples

**Feature**: dark-sneaker-retraining
**Linked edit**: edits/01-start-and-visual-samples.md
**Signal**: extend

## What the user said (verbatim)
> เริ่มและขอดูภาพ tickets  2 ด้วย ยกตัวอย่าง 5 รูป

## Reason the user gave
Not stated

## What the user asked to change
- Start implementation of the approved tickets
- Provide 5 visual example images demonstrating Ticket 02 training-time augmentations

## What was actually changed (fill in after the edit)
- `scripts/merge_datasets.py` & `tests/unit/test_dataset_merger.py`: Manifest merger with 5x hallway oversampling.
- `scripts/train_sneaker_model.py` & `tests/unit/test_train_augmentation.py`: Full ADR-0007 augmentation suite (`hsv_s=0.7`, `hsv_v=0.4`, `degrees=10.0`, `erasing=0.2`, `fliplr=0.5`, `mosaic=1.0`, `scale=0.5`).
- `scripts/visualize_augmentations.py`: Generated 5 sample augmented demonstration images from live hallway crops.
- `scripts/evaluate_and_export.py` & `tests/unit/test_evaluate_dual_gate.py`: Dual-gate evaluation (`mAP50 >= 0.75` and `hallway_recall >= 0.90`), auto backup to `yolo-sneaker.backup.pt`, and 13 Before/After comparison images.
- Trained YOLO11n on MPS for 30 epochs, passed Dual-Gate (mAP50=0.7824, hallway recall=1.0000 @ conf 0.40), promoted `models/yolo-sneaker.pt`, and all 40 pytest tests pass.
