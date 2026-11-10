# Edit 04: Annotate Occluded and Blurred Second Shoes

**Status:** done

## Rationale & Impact
Upon visual review of the verification report, the user pointed out three specific images where the automated segmentation missed the second shoe due to depth occlusion, tilt, or motion blur:
1. `07-00-37_6`: Second shoe is overlapping in depth right behind shoe #1.
2. `07-01-39_1`: Second shoe is tilted in the upper-left corner.
3. `07-01-13_1`: Second shoe is motion blurred in the upper-right corner.

Accurately boxing these challenging edge cases teaches YOLO11n to handle heavy motion blur, perspective tilt, and stride overlap, preventing false negatives in live production.

## Target Files
- `datasets/sneakers_live/labels/train/`
- `output/verified_labels/`
- `<conversation-artifact>/verified_labels_report.md`

## Planned Changes
- Inspect the exact pixel regions for `07-00-37_6`, `07-01-39_1`, and `07-01-13_1`.
- Add the second bounding box for each of these three images with exact normalized YOLO coordinates in `datasets/sneakers_live/labels/`.
- Re-render the annotated verification images with cyan boxes (`sneaker #2`) in `output/verified_labels/`.
- Update the visual verification report artifact.

## Acceptance Criteria
- [x] `07-00-37_6` has 2 bounding boxes annotated.
- [x] `07-01-39_1` has 2 bounding boxes annotated.
- [x] `07-01-13_1` has 2 bounding boxes annotated.
- [x] Verification images visually confirm accurate framing for all three.
