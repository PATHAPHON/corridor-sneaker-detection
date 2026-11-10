# Feedback 04: Annotate Occluded and Blurred Second Shoes

**Feature**: storage-and-evidence
**Linked edit**: edits/04-annotate-occluded-blurred-second-shoes.md
**Signal**: refine

## What the user said (verbatim)
> ภาพแรกแค่อยู่ใกล้ๆกับภาพหนึ่ง มันซ้อนกันอยู่ มันอยู่ละหน้า ต่อมาภาพที่สอง มันจะอยู่ด้านซ้ายบน มันจะเอียงๆนิดนึง เกือบ เกือบมองไม่เห็น ต่อมาภาพที่สามก็จะอยู่ขวาบน มันเบลอๆนิดนึง

## Reason the user gave
Not stated

## What the user asked to change
- In image `07-00-37_6`: Add the second shoe overlapping/stacked closely behind shoe #1.
- In image `07-01-39_1`: Add the second shoe located at the upper-left, tilted, almost occluded.
- In image `07-01-13_1`: Add the second shoe located at the upper-right, motion blurred.
- Update YOLO ground-truth label files and regenerate verification images for user visual confirmation.

## What was actually changed (fill in after the edit)
- Added precision bounding box for second shoe in `07-00-37_6` (depth-overlapping heel directly behind front shoe).
- Added precision bounding box for second shoe in `07-01-39_1` (tilted upper-left shoe resting on cardboard box).
- Added precision bounding box for second shoe in `07-01-13_1` (motion-blurred upper-right shoe stepping forward).
- Updated YOLO `.txt` label files in `datasets/sneakers_live/labels/train/`.
- Regenerated verification preview images in `output/verified_labels/` and updated `verified_labels_report.md` artifact.
