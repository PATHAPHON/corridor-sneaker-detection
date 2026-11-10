# 01: Manifest Dataset Merger with Hallway Oversampling

**What to build:** A manifest-based YOLO dataset merger and CLI utility that combines the baseline sneaker dataset with curated live hallway Lower-Body ROI crops into `train.txt`, `val.txt`, `test.txt`, and `data.yaml`, applying configurable oversampling (default 5x) to live hallway training images without duplicating image files on disk.

**Blocked by:** None (can start immediately)

**Status:** done

- [x] Generates `train.txt`, `val.txt`, `test.txt`, and `data.yaml` referencing single class `0: sneaker` without copying image files
- [x] Oversamples live hallway training crops by 5x default multiplier ($190 + 11 \times 5 = 245$ train entries) while keeping validation and test splits at 1x ($56 + 2 = 58$ val entries)
- [x] Verifies YOLO label availability and path resolution for both `images/train` and `train/images` directory layouts
- [x] Seam unit tests verify manifest counts, oversampling ratios, and `data.yaml` schema using temporary dataset fixtures
