# Edit 02: Real Wall-Clock Date and Sequence Prefix for Captured Evidence

**Status**: done

## Rationale & Impact
The user reported confusion distinguishing between older and newer captured images ("จะรู้ได้ไงอันไหนเก่าใหม่", "แก้ให้หน่อย"). Investigation revealed two root causes:
1. When video files are streamed, `task.timestamp` provides relative video seconds (e.g. 109.34s). Calling `datetime.fromtimestamp(task.timestamp)` maps this to the Unix epoch date (`1970-01-01`), producing misleading folder paths like `output/captures/1970-01-01/`.
2. Evidence file names omit an incrementing event counter, forcing users to parse microsecond timestamp strings to determine event order.

Per user selection, this edit changes evidence capture to:
- Partition folders and timestamps using the real current wall-clock date (`YYYY-MM-DD`) and timestamp (`YYYY-MM-DDTHH-MM-SS`), while preserving video playback seconds in log metadata.
- Prepend a zero-padded sequential event identifier (e.g. `event_00071_...`) to evidence image filenames so that standard filesystem sorting (Finder, `ls`) naturally and unambiguously orders files from oldest to newest.

## Target Files
- `src/pipeline/coordinator.py`
- `src/storage/evidence_writer.py`
- `tests/unit/test_evidence_writer.py`
- `tests/integration/test_storage_pipeline.py`

## Planned Changes
- Enhance `EvidenceWriter.save_evidence()` to accept `event_id: Optional[int] = None`.
- If `event_id` is provided, name files `{event_id:05d}_{safe_timestamp}_{track_id}_full.jpg` and `{event_id:05d}_{safe_timestamp}_{track_id}_crop.jpg`.
- In `PipelineCoordinator`, track sequential crossing count `crossing_counter` and use real current wall-clock `datetime.now()` when `task.timestamp` is a relative offset (< 1e9).
- Update unit tests in `test_evidence_writer.py` and integration tests in `test_storage_pipeline.py`.
- Run full pytest test suite and update knowledge graph.

## Acceptance Criteria
- [x] Relative video timestamps map to real current wall-clock date (`YYYY-MM-DD`), preventing `1970-01-01` folders.
- [x] Evidence filenames include zero-padded event sequence prefix (e.g. `00071_...`) when provided.
- [x] Alphabetical sorting of capture directories orders files from oldest to newest.
- [x] All unit and integration tests pass cleanly.
