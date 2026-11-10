# Feedback 05: Dark Sneaker Augmentation Strategy & ADR

**Feature**: storage-and-evidence
**Linked edit**: edits/05-dark-sneaker-augmentation-and-adr.md
**Signal**: extend

## What the user said (verbatim)
> เอาแบบ 1 และ เพื่ม adr เกี่ยวกับเรื่องนี้ด้วยยังไม่มีถึงเรื่องนี้เลย

## Reason the user gave
In response to the grill-me design questions on how to improve dark sneaker detection under indoor lighting and motion blur: the user chose Option 1 (training-time data augmentation with zero runtime overhead) over runtime CLAHE image enhancement or multi-frame burst capture, and requested creating an Architecture Decision Record (ADR) documenting this architectural invariant.

## What the user asked to change
- Keep single-frame snapshot capture at tripwire crossing (no burst buffering complexity).
- Adopt training-time data augmentation (Mosaic, Scale, Brightness/Contrast Jitter, Motion Blur) in YOLO fine-tuning without runtime preprocessing.
- Author ADR-0007 in `docs/adr/0007-dark-sneaker-image-processing-and-training-augmentation.md`.
- Update `GLOSSARY.md` with Invariant 7 reflecting this architecture decision.
- Prepare a comprehensive `/handoff` document for executing Ticket 05 retraining and verification.

## What was actually changed (fill in after the edit)
- Authored `docs/adr/0007-dark-sneaker-image-processing-and-training-augmentation.md`.
- Added Invariant 7 (Training-Time Augmentation over Runtime Preprocessing) to `GLOSSARY.md`.
- Created `.scratch/storage-and-evidence/handoff.md` summarising the grill-me alignment decisions and execution playbook.
