# Edit 03: Accurate Two-Foot Annotation & Verification Pipeline

**Status:** done

## Rationale & Impact
The user identified that previous pseudo-labeled exports had misaligned or missing bounding boxes (only 0 or 1 box instead of both feet). Training on faulty pseudo-labels would cause confirmation bias and teach the detector to miss dark sneakers. The user confirmed that all 15 selected images depict sneakers on both feet and requested Method 1: AI-assisted precision annotation of both sneakers followed by visual verification output.

## Target Files
- `scripts/curate_and_annotate_all.py`
- `datasets/sneakers_live/labels/train/`
- `datasets/sneakers_live/images/train/`
- `datasets/sneakers_live/data.yaml`
- `output/verified_labels/`

## Planned Changes
- Create `scripts/curate_and_annotate_all.py` to extract clean lower-body crops from all 15 full frames without preexisting artifacts.
- Segment and annotate ground-truth bounding boxes for sneakers across all images.
- Write normalized YOLO format `.txt` label files for all clean images.
- Render verification preview images with distinct bounding boxes and labels to `output/verified_labels/`.
- Present verification results and file links to the user for visual inspection.

## Acceptance Criteria
- [x] All images have valid clean crops extracted from full frames.
- [x] All images have corresponding YOLO label files with ground-truth sneaker bounding boxes.
- [x] Rendered verification images saved to `output/verified_labels/`.
