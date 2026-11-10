# 04: Active Dataset Curation & Export CLI

**What to build:** An active learning export utility that queries captured crossings from SQLite, retrieves cropped foot images, and generates a formatted YOLO dataset structure with bounding box annotation drafts and confidence filters for active retraining.

**Blocked by:** 03 (Pipeline Worker Storage Integration)

**Status:** done

- [x] CLI command queries `crossing_events` table and filters by confidence thresholds or compliance status
- [x] Exports cropped foot images into YOLO directory structure (`images/train`, `images/val`, `labels/train`, `labels/val`)
- [x] Auto-generates initial YOLO format text labels from detected sneaker coordinates for fast human review/pseudo-labeling
- [x] Generates valid `data.yaml` referencing class `0: sneaker`
- [x] Unit tests verify dataset structure generation and label coordinate normalizations
