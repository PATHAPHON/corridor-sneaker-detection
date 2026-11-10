# Edit 05: Dark Sneaker Augmentation Strategy & ADR

**Status:** done

## Rationale & Impact
Following the `/grill-me` alignment session regarding capture methods and image processing for dark footwear in indoor corridors, the user decided to maintain single-frame capture at the tripwire and address low-contrast dark shoes via training-time data augmentation (Mosaic, Scale, Brightness/Contrast Jitter) with zero runtime latency impact. This decision represents a foundational architectural choice requiring a formal Architecture Decision Record (ADR-0007) and an addition to `GLOSSARY.md`.

## Target Files
- `docs/adr/0007-dark-sneaker-image-processing-and-training-augmentation.md`
- `GLOSSARY.md`
- `.scratch/storage-and-evidence/handoff.md`

## Planned Changes
- Verify ADR-0007 content and structure against template.
- Add Invariant 7 (Training-Time Augmentation over Runtime Preprocessing) to `GLOSSARY.md`.
- Produce the final handoff document in `.scratch/storage-and-evidence/handoff.md` capturing all grill-me decisions and Ticket 05 execution commands.

## Acceptance Criteria
- [x] ADR-0007 exists in `docs/adr/0007-dark-sneaker-image-processing-and-training-augmentation.md`.
- [x] `GLOSSARY.md` includes Invariant 7.
- [x] `.scratch/storage-and-evidence/handoff.md` details all architectural decisions, dataset paths, training parameters, benchmark gates, and verification steps.
- [x] `graphify update .` runs cleanly.
