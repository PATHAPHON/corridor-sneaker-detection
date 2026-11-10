# ADR-0004: Event Logging, Image Evidence Storage, and Database Architecture

**Date**: 2026-11-10
**Status**: accepted
**Deciders**: Pat (Developer), AI Assistant

## Context

When a line-crossing shoe detection event occurs, the system must persist both structured event metadata and visual evidence for verification, auditing, and subsequent reporting. 

The storage architecture must:
1. Handle write concurrency without external database server overhead.
2. Store dual image evidence: the full camera scene (showing the person context) and the high-resolution cropped foot region (showing the detected shoes).
3. Centralize system parameters (line coordinates, camera URL, thresholds) in a clean configuration structure.

## Decision

We will implement a **SQLite Database + Dual-Image Local Storage** architecture configured via **YAML**:

1. **Storage Engine (SQLite)**:
   - A single-file SQLite database located at `output/events.db`.
   - Table `crossing_events`:
     ```sql
     CREATE TABLE IF NOT EXISTS crossing_events (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         timestamp TEXT NOT NULL,
         track_id INTEGER NOT NULL,
         direction TEXT NOT NULL DEFAULT 'A_TO_B',
         shoes_detected BOOLEAN NOT NULL,
         shoe_count INTEGER NOT NULL DEFAULT 0,
         max_confidence REAL,
         bboxes_json TEXT,
         full_image_path TEXT NOT NULL,
         crop_image_path TEXT NOT NULL
     );
     CREATE INDEX IF NOT EXISTS idx_events_timestamp ON crossing_events(timestamp);
     CREATE INDEX IF NOT EXISTS idx_events_track_id ON crossing_events(track_id);
     ```

2. **Visual Evidence Filesystem**:
   - Save images under date-partitioned directories: `output/captures/YYYY-MM-DD/`.
   - File naming convention:
     - Full scene frame: `{timestamp}_{track_id}_full.jpg`
     - Cropped foot ROI: `{timestamp}_{track_id}_crop.jpg`

3. **Configuration Architecture (`config.yaml`)**:
   - Centralize all environment and pipeline tunables into `config.yaml`:
     ```yaml
     video_source: 0 # MacBook FaceTime Camera (device 0), RTSP URL, or video file
     virtual_line:
       start: [960, 0]
       end: [960, 1080]
       trigger_direction: "A_TO_B" # Left-to-Right crossing (A=Left, B=Right)
     models:
       person_model: "yolo11n.pt"
       shoe_model: "models/yolo-sneaker.pt"
       person_confidence: 0.50
       shoe_confidence: 0.40
     tracking:
       track_thresh: 0.25
       match_thresh: 0.80
       cooldown_seconds: 3.0
     storage:
       db_path: "output/events.db"
       capture_dir: "output/captures"
     ```
   - CLI arguments can override `config.yaml` values when launched.

## Alternatives Considered

### Alternative 1: Flat JSON Lines (`events.jsonl`) Only
- **Pros**: Minimal dependencies, zero SQL schema required.
- **Cons**: Querying by date range, track ID, or shoe detection status requires full sequential file scans; difficult to do analytical reporting.
- **Why not**: SQLite is built into Python standard library, requires zero external services, and provides indexed fast queries.

### Alternative 2: Remote PostgreSQL / Cloud Database
- **Pros**: Centralized multi-camera aggregation.
- **Cons**: Fails if local network drops; adds infrastructure complexity for local edge processing.
- **Why not**: Edge-first local SQLite provides full offline resilience. An optional background exporter can sync SQLite rows to cloud asynchronously later.

## Consequences

### Positive
- **Complete Audit Trail**: Each record links exact timestamp, track ID, and decision metadata to physical JPEG evidence on disk.
- **Zero Server Setup**: Works out of the box using Python's native `sqlite3` module.
- **Safe from Network Drops**: Local storage guarantees zero lost events even if WAN/LAN connectivity disconnects.

### Negative
- **Disk Space Management**: Continuous capture images will accumulate over time.
  - *Mitigation*: Implement an automated retention/cleanup policy (e.g. purge images older than 30 days).

### Risks
- **SQLite Write Locks under High Concurrency**: If multiple camera threads write simultaneously, `sqlite3.OperationalError: database is locked` could occur.
  - *Mitigation*: Enable WAL mode (`PRAGMA journal_mode=WAL;`) on connection initialization and use a thread-safe write queue.

