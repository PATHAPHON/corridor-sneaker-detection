# 01: Preflight and Single-Image Verification

**What to build:** An automated preflight validation check and single-image upload runner that loads `.env` credentials, creates the `sneaker-detection` object detection project in Roboflow, and uploads 1 test image from the dataset to confirm the connection and project initialization end-to-end.

**Blocked by:** None (can start immediately).

**Status:** done

- [x] Verify 299 image files in `/Users/pat/Downloads/shoeTypeClassifierDataset/` are valid and accessible.
- [x] Verify `ROBOFLOW_API_KEY` and `ROBOFLOW_WORKSPACE` authenticate with Roboflow API.
- [x] Create `sneaker-detection` project on Roboflow if not existing (created `sneaker-detection-fggnt`).
- [x] Upload 1 test image successfully and confirm project shows 1 uploaded image (tested with `image1.jpg`).
