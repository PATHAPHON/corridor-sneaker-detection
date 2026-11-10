# 01: SQLite WAL Event Persistence Repository

**What to build:** An embedded SQLite persistence layer with Write-Ahead Logging (WAL) enabled that stores crossing event metadata (track ID, timestamp, direction, sneaker detection status, sneaker count, confidence scores, and evidence image paths) with query and indexing support.

**Blocked by:** None (can start immediately)

**Status:** done

- [x] SQLite connection helper enables `PRAGMA journal_mode=WAL;` and `PRAGMA synchronous=NORMAL;`
- [x] Table schema for `crossing_events` created idempotently with indices on `timestamp` and `track_id`
- [x] Repository interface inserts crossing event records and retrieves them by date range or track ID
- [x] Seam unit tests verify WAL mode, insertion, and query contracts using an in-memory or temporary database
