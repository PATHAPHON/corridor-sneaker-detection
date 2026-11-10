# Edit 01: Implement Storage Persistence & Active Retraining Pipeline

**Status:** done

## Rationale & Impact
The user confirmed the diagnosis of intermittent sneaker detection caused by domain gap and lack of image persistence for model fine-tuning. The user gave direct approval ("เริ่ม") to implement the persistence foundation (SQLite WAL repository and visual evidence filesystem writer) and integrate them into the pipeline worker sink.

## Target Files
- `src/storage/__init__.py`
- `src/storage/repository.py`
- `src/storage/evidence_writer.py`
- `src/storage/dataset_exporter.py`
- `src/pipeline/coordinator.py`
- `src/config/settings.py`
- `src/main.py`
- `scripts/export_dataset.py`
- `tests/unit/test_storage.py`
- `tests/unit/test_evidence_writer.py`
- `tests/unit/test_dataset_exporter.py`
- `tests/integration/test_storage_pipeline.py`

## Planned Changes
- Create `src/storage/repository.py` implementing `EventRepository` and `CrossingRecord` dataclass with SQLite WAL mode.
- Create `src/storage/evidence_writer.py` implementing date-partitioned JPEG saving for full frame and annotated crop.
- Create `src/storage/dataset_exporter.py` implementing YOLO dataset exporter from SQLite.
- Connect storage components into `PipelineCoordinator` background worker loop.
- Validate via unit and integration tests under TDD.

## Acceptance Criteria
- [x] SQLite repository initializes schema with WAL mode enabled and indices on `timestamp` and `track_id`.
- [x] Evidence writer saves dual JPEGs under `output/captures/YYYY-MM-DD/`.
- [x] `PipelineCoordinator` dispatches crossing events to storage sink without blocking main capture thread.
- [x] All unit and integration tests pass cleanly (`pytest`).
