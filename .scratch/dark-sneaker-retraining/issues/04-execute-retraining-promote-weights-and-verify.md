# 04: Execute Retraining, Promote Production Weights & Verify Live Stability

**What to build:** End-to-end execution of the merged dataset build, 30-epoch MPS fine-tuning run with ADR-0007 augmentations, dual-gate benchmark verification, safe promotion of `models/yolo-sneaker.pt`, and visual verification report across all 13 real hallway crops with full test suite green.

**Blocked by:** 03 (Dual-Gate Evaluation, Safe Backup & Before/After Visual Report)

**Status:** done

- [x] Generates `datasets/sneakers_merged/data.yaml` and oversampled manifests (`train.txt`, `val.txt`, `test.txt`)
- [x] Completes 30-epoch warm-start fine-tuning on `mps` and passes both Gate 1 (`mAP50 >= 0.80`) and Gate 2 (`hallway_recall >= 0.90`)
- [x] Promotes new weights to `models/yolo-sneaker.pt` with backup saved at `models/yolo-sneaker.backup.pt`
- [x] Produces complete Before/After visual comparison report for all 13 hallway crops and passes full `uv run pytest` suite
