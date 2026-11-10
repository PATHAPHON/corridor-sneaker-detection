# 03: Dual-Gate Evaluation, Safe Backup & Before/After Visual Report

**What to build:** A dual-gate evaluation, automatic backup, and side-by-side visual comparison workflow that enforces both overall merged validation `mAP50 >= 0.80` and real hallway sneaker recall $\ge 0.90$ at `conf=0.40` before backing up existing production weights and promoting new weights, while generating side-by-side Before vs After comparison images and quantitative summaries across all 13 hallway crops.

**Blocked by:** 01 (Manifest Dataset Merger with Hallway Oversampling), 02 (ADR-0007 Training-Time Augmentation Pipeline)

**Status:** done

- [x] Enforces Gate 1 (Merged validation `mAP50 >= 0.80`) and Gate 2 (Hallway ground-truth recall $\ge 0.90$ at `conf=0.40`)
- [x] Automatically backs up existing production model weights to `.backup.pt` prior to promotion, and aborts promotion without overwriting if either gate fails
- [x] Renders side-by-side `Before vs After` annotated comparison JPEGs for all 13 real hallway crops showing bounding boxes, counts, and confidence scores
- [x] Writes comprehensive `eval_summary.json` including dual-gate status, before/after hallway recall, before/after mean confidence, and comparison image paths
- [x] Seam unit tests verify dual-gate pass/fail branching, backup creation, abort safety, and Before/After report generation
