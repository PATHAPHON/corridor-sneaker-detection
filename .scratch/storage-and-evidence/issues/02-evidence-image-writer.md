# 02: Evidence Image Filesystem Writer

**What to build:** A date-partitioned visual evidence filesystem writer saving dual high-resolution JPEG files (full context frame and cropped feet ROI with rendered bounding boxes) per crossing event.

**Blocked by:** None (can start immediately)

**Status:** done

- [x] Directory layout partitioned by date (`output/captures/YYYY-MM-DD/`) created automatically
- [x] Saves full scene frame to `{timestamp}_{track_id}_full.jpg`
- [x] Saves lower-body feet crop with rendered sneaker bounding boxes to `{timestamp}_{track_id}_crop.jpg`
- [x] Seam unit tests verify file creation, directory permissions, and valid JPEG encoding
