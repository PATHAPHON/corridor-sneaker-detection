# Feature Spec: Storage Persistence & Active Retraining Pipeline

## Problem Statement

The pedestrian monitoring system currently experiences inconsistent sneaker detection during live camera execution (repeatedly alternating between 0, 1, or 2 sneakers with erratic confidence scores). Crucially, the system does not persist visual evidence or crossing event records to disk. As a result:
1. No permanent audit trail exists for facility compliance tracking.
2. No operational dataset of real-world corridor/hallway foot crops is collected under actual camera lighting, angle, and floor reflections.
3. The fine-tuned sneaker detector cannot be re-trained or adapted on real camera domain data, leaving the domain gap between training data and live operational video unresolved.

## Solution

Implement a complete closed-loop data persistence and active learning pipeline executed in strict sequential phases:
1. **Phase 1: Real-Time Event & Evidence Storage (Foundation)**
   - Persist every crossing event into a local SQLite database configured with Write-Ahead Logging (WAL) for high-performance concurrent writes.
   - Save dual high-resolution evidence images (full context frame and lower-body foot crop) into date-partitioned local storage.
   - Wire storage operations into the decoupled background worker thread so the 30+ FPS capture loop remains completely non-blocking.
2. **Phase 2: Active Dataset Curation & Export**
   - Provide an export utility that queries SQLite for captured crossing events, retrieves the corresponding foot ROI crops, and structures them into standard YOLO format.
   - Filter and catalog crops across compliance classes (sneakers detected vs. no sneakers detected) for semi-automated labeling or pseudo-labeling.
3. **Phase 3: Sneaker Model Retraining & Evaluation Gate**
   - Retrain the single-class YOLO11n sneaker detector combining original baseline data with newly harvested real-world hallway foot crops.
   - Enforce rigorous evaluation gates (mAP50, precision, recall) before exporting updated model weights to the production runtime.
4. **Phase 4: Live Verification & Model Hot-Swap**
   - Deploy the retrained model weights into the pipeline coordinator and verify stable, consistent sneaker counts on live camera feed.

## User Stories

1. As a facility compliance officer, I want every virtual tripwire crossing event recorded in SQLite, so that I have a reliable and searchable audit log of entries.
2. As a facility compliance officer, I want crossing records to store track ID, timestamp, transit direction, shoe detection flag, sneaker count, and confidence scores, so that I can inspect compliance metrics.
3. As an audit operator, I want each crossing record to link to physical full-scene and cropped-foot JPEG evidence files, so that I can visually verify compliance decisions.
4. As a system engineer, I want the SQLite database to run in WAL (`Write-Ahead Logging`) mode, so that background worker writes never cause database lock errors or block concurrent reads.
5. As a system engineer, I want evidence images saved into date-partitioned folders (`YYYY-MM-DD`), so that filesystem directories remain organized and performant over long runtimes.
6. As a real-time capture loop, I want all disk I/O and database operations handled strictly in the background worker thread, so that video processing maintains a consistent 30+ FPS rate.
7. As a computer vision engineer, I want to collect real lower-body crops from live webcam footage, so that I have domain-specific training samples reflecting actual floor glare, camera angles, and walking strides.
8. As a computer vision engineer, I want a dataset exporter tool to extract captured crops from SQLite into YOLO dataset format, so that I can easily feed them into the model retraining pipeline.
9. As a computer vision engineer, I want the exporter to support confidence-based filtering (e.g. low-confidence detections or false negatives), so that active learning focuses on the most ambiguous cases.
10. As a ML engineer, I want to fine-tune YOLO11n on the merged dataset using mosaic and scale augmentations, so that the detector overcomes the domain gap and learns real-world shoe appearances.
11. As a ML engineer, I want the retraining script to validate against a held-out test split and enforce an mAP50 benchmark gate, so that regression or degraded models are prevented from deploying.
12. As a system operator, I want the pipeline to seamlessly load the retrained model weights without architectural changes, so that live detection accuracy immediately improves.
13. As an operator running synthetic or video file tests, I want persistence to function deterministically across all frame sources, so that automated testing can verify storage without physical cameras.
14. As a developer, I want unit and integration tests using temporary in-memory databases and mock directories, so that the storage layer is thoroughly validated without cluttering project files.

## Implementation Decisions

### Phase 1: Storage Layer & Pipeline Integration
- **SQLite Database Architecture**:
  - Embedded single-file database initialized with `PRAGMA journal_mode=WAL;` and `PRAGMA synchronous=NORMAL;`.
  - Schema:
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
- **Evidence Filesystem Writer**:
  - Date-partitioned directory layout: `output/captures/YYYY-MM-DD/`.
  - Deterministic file naming: `{timestamp}_{track_id}_full.jpg` (full frame) and `{timestamp}_{track_id}_crop.jpg` (feet ROI with annotated boxes).
  - Atomic directory creation and safe JPEG encoding.
- **Pipeline Sink Integration**:
  - The background worker consumes `CrossingTask` from the bounded queue, runs sneaker inspection, persists records and images via the storage manager, updates the HUD alert, and executes the optional callback.
  - Zero filesystem or database operations are executed on the main video thread.

### Phase 2: Active Dataset Export & Curation
- **Dataset Export Utility**:
  - CLI command/script querying `crossing_events` for recent captures.
  - Generates YOLO-compliant dataset structure (`images/train`, `images/val`, `labels/train`, `labels/val`, and `data.yaml`).
  - Pre-populates YOLO label txt files based on inspector bounding box coordinates, allowing rapid human review or pseudo-labeling.
  - Flags uncertain detections (confidence between 0.20 and 0.50, or count = 0 with high person presence) for targeted labeling.

### Phase 3: Model Retraining & Deployment
- **Fine-Tuning Execution**:
  - Python training script executing YOLO11n fine-tuning on Metal (`mps`) or CPU/CUDA.
  - Training configuration: 50 epochs, learning rate schedule, `mosaic=1.0`, `scale=0.5`.
  - Checkpoint verification: mAP50 evaluation gate ($\ge 0.80$ on real-world test split).
- **Model Promotion**:
  - Script replaces or versions `models/yolo-sneaker.pt`.
  - Config points to active model weights.

### Execution Roadmap (Order of Operations)
1. **First (Phase 1)**: Build SQLite repository & Evidence image writer + hook into background worker. Verify via unit & integration tests.
2. **Second (Collection)**: Run the live pipeline with camera to capture 50–100 real crossing events (collecting real foot crops).
3. **Third (Phase 2)**: Run dataset export tool to prepare the YOLO retraining dataset.
4. **Fourth (Phase 3)**: Retrain YOLO11n sneaker model on the augmented dataset and pass evaluation gate.
5. **Fifth (Phase 4)**: Verify live inference in camera GUI preview, confirming stable multi-shoe detection.

## Testing Decisions

- **Public Seams**:
  - **Storage Repository Seam**: Input an immutable event dataclass; assert SQLite table insertion, field values, and query filtering by track ID / date range.
  - **Evidence Writer Seam**: Input frame and crop numpy arrays; assert files created on disk at expected paths with valid dimensions.
  - **Pipeline Worker Seam**: Send crossing tasks through the bounded queue; assert background worker persists database records and writes image files without delaying the capture loop.
  - **Dataset Exporter Seam**: Populate mock SQLite records; assert generated YOLO folder structure, images, and label format.
- **Invariants to Verify**:
  - SQLite WAL mode is active.
  - Main capture loop maintains 30+ FPS during consecutive crossings.
  - Database schema migrations or table creation are idempotent (`IF NOT EXISTS`).
  - Graceful handling of disk write failures or directory permissions.

## Out of Scope

- Multi-camera centralized database clustering (PostgreSQL/Cloud SQL).
- Automatic online model learning during inference (all training is offline/batch fine-tuning).
- Multi-class footwear taxonomy (flip-flops, boots, sandals) — strictly limited to single class `0: sneaker`.
- Cloud auto-sync (S3/GCS bucket uploads) — edge local storage only.

## Further Notes

- In compliance with ADR-0004 and ADR-0005, all configuration parameters (paths, thresholds, directory names) reside in `src/config/settings.py` and are overridable via CLI.
