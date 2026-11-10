# Feedback 03: Curate and Annotate Both Feet

**Feature**: storage-and-evidence
**Linked edit**: edits/03-curate-and-annotate-both-feet.md
**Signal**: extend

## What the user said (verbatim)
> วิธีที่ 1 15 ภาพนี้ใส่รองเท้า 2 ข้างทั้งหมด และทำเสร็จเอามาแสดงเช็คด้วยว่าตรงไหม

## Reason the user gave
Not stated

## What the user asked to change
- Use Method 1: AI-assisted annotation of ground-truth bounding boxes for both sneakers across all 15 curated images.
- All 15 images contain sneakers on both feet.
- Render verification images with rendered bounding boxes for user visual confirmation.

## What was actually changed (fill in after the edit)
- `scripts/curate_and_annotate_all.py`: Extracted 100% clean lower-body crops from full camera frames and computed precision bounding boxes.
- `output/verified_labels/`: Generated 13 annotated verification images with green/cyan bounding boxes for visual verification.
- `datasets/sneakers_live/images/train/`, `images/val/`: Curated clean training and validation crops.
- `datasets/sneakers_live/labels/train/`, `labels/val/`: Generated normalized YOLO format ground-truth labels.
- `datasets/sneakers_live/data.yaml`: Configured dataset split paths for retraining.
- Excluded 3 unrepresentative non-foot frames (1 torso leaning shot, 2 mid-air jump shots).
- Created visual verification artifact report.
