"""Unit tests for SQLite WAL event persistence repository."""
import os
import sqlite3
import tempfile
from dataclasses import asdict
from pathlib import Path
import pytest

from src.storage.repository import EventRepository, CrossingRecord


@pytest.fixture
def temp_db_path(tmp_path: Path) -> Path:
    """Fixture providing a temporary SQLite database file path."""
    return tmp_path / "test_events.db"


def test_sqlite_repository_initialization_enables_wal_and_creates_schema(temp_db_path: Path):
    """Test repository creates table, indices, and enables WAL mode."""
    repo = EventRepository(db_path=str(temp_db_path))
    repo.initialize()

    conn = sqlite3.connect(str(temp_db_path))
    cursor = conn.cursor()

    # Verify WAL journal mode
    cursor.execute("PRAGMA journal_mode;")
    mode = cursor.fetchone()[0]
    assert mode.lower() == "wal"

    # Verify table existence
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='crossing_events';")
    assert cursor.fetchone() is not None

    # Verify indices
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_events_timestamp';")
    assert cursor.fetchone() is not None
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_events_track_id';")
    assert cursor.fetchone() is not None
    conn.close()


def test_sqlite_repository_insert_and_query_by_track_id(temp_db_path: Path):
    """Test inserting crossing records and querying them by track_id."""
    repo = EventRepository(db_path=str(temp_db_path))
    repo.initialize()

    record1 = CrossingRecord(
        timestamp="2026-11-10T18:57:17.773",
        track_id=3,
        direction="A_TO_B",
        shoes_detected=False,
        shoe_count=0,
        max_confidence=None,
        bboxes_json="[]",
        full_image_path="/path/to/3_full.jpg",
        crop_image_path="/path/to/3_crop.jpg",
    )
    record2 = CrossingRecord(
        timestamp="2026-11-10T18:58:16.718",
        track_id=17,
        direction="A_TO_B",
        shoes_detected=True,
        shoe_count=2,
        max_confidence=0.79,
        bboxes_json='[{"box": [10, 20, 50, 60], "confidence": 0.79}, {"box": [60, 20, 100, 60], "confidence": 0.48}]',
        full_image_path="/path/to/17_full.jpg",
        crop_image_path="/path/to/17_crop.jpg",
    )

    record_id_1 = repo.insert_event(record1)
    record_id_2 = repo.insert_event(record2)

    assert record_id_1 == 1
    assert record_id_2 == 2

    # Query by track_id
    results_track_17 = repo.get_events_by_track(track_id=17)
    assert len(results_track_17) == 1
    retrieved = results_track_17[0]
    assert retrieved.track_id == 17
    assert retrieved.shoes_detected is True
    assert retrieved.shoe_count == 2
    assert retrieved.max_confidence == pytest.approx(0.79)
    assert retrieved.full_image_path == "/path/to/17_full.jpg"
    assert retrieved.crop_image_path == "/path/to/17_crop.jpg"


def test_sqlite_repository_query_all_and_count(temp_db_path: Path):
    """Test counting records and querying recent records."""
    repo = EventRepository(db_path=str(temp_db_path))
    repo.initialize()

    for i in range(5):
        record = CrossingRecord(
            timestamp=f"2026-11-10T18:5{i}:00.000",
            track_id=i,
            direction="A_TO_B",
            shoes_detected=(i % 2 == 0),
            shoe_count=2 if (i % 2 == 0) else 0,
            max_confidence=0.85 if (i % 2 == 0) else None,
            bboxes_json="[]",
            full_image_path=f"/captures/{i}_full.jpg",
            crop_image_path=f"/captures/{i}_crop.jpg",
        )
        repo.insert_event(record)

    assert repo.count_events() == 5
    records = repo.get_all_events(limit=10)
    assert len(records) == 5
