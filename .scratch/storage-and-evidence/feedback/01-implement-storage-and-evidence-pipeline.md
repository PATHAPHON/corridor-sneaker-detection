# Feedback 01: Implement Storage Persistence & Active Retraining Pipeline

**Feature**: storage-and-evidence
**Linked edit**: edits/01-implement-storage-and-evidence-pipeline.md
**Signal**: extend

## What the user said (verbatim)
> เริ่ม

## Reason the user gave
Not stated

## What the user asked to change
- Proceed with implementing the storage persistence layer and active retraining pipeline according to approved spec and tracer-bullet tickets.

## What was actually changed (fill in after the edit)
- `src/storage/repository.py`: Implemented SQLite WAL repository (`EventRepository`) and `CrossingRecord` schema.
- `src/storage/evidence_writer.py`: Implemented date-partitioned JPEG saving for full scene and annotated cropped feet ROI.
- `src/storage/dataset_exporter.py`: Implemented YOLO format export utility extracting foot crops and normalized bounding box labels from SQLite.
- `src/config/settings.py`: Added `enable_storage`, `db_path`, `capture_dir` to `PipelineConfig`.
- `src/pipeline/coordinator.py`: Integrated background worker with storage repository and evidence writer.
- `src/main.py`: Added `--no-storage`, `--db-path`, `--capture-dir` CLI options and formatted persistence log output.
- `scripts/export_dataset.py`: Added CLI entrypoint for dataset export.
- `tests/unit/test_storage.py`, `tests/unit/test_evidence_writer.py`, `tests/unit/test_dataset_exporter.py`, `tests/integration/test_storage_pipeline.py`: Comprehensive unit and integration test coverage.
