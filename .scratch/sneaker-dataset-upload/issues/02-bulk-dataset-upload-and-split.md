# 02: Bulk Dataset Upload and Split

**What to build:** Ingestion script that uploads the remaining 298 sneaker images to the Roboflow `sneaker-detection` project, automatically distributing images across a 70% Train / 20% Valid / 10% Test split with progress reporting and retry logic.

**Blocked by:** 01: Preflight and Single-Image Verification

**Status:** done

- [x] Ingest remaining 298 images from `training/sneakers` and `validation/sneakers`.
- [x] Distribute images with 70% train (~210), 20% valid (~60), 10% test (~29) tags/splits (actual: 209 train, 60 valid, 30 test).
- [x] Log progress, upload status, and handle any network transient errors.
- [x] Confirm total 299 images processed in Roboflow project (275 unique images uploaded, 24 duplicate source images filtered by Roboflow).
