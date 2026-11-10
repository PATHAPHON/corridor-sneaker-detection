"""SQLite WAL event persistence repository."""
import json
import logging
import os
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CrossingRecord:
    """Immutable data record representing a crossing event stored in SQLite."""
    timestamp: str
    track_id: int
    direction: str = "A_TO_B"
    shoes_detected: bool = False
    shoe_count: int = 0
    max_confidence: Optional[float] = None
    bboxes_json: str = "[]"
    full_image_path: str = ""
    crop_image_path: str = ""
    id: Optional[int] = None


class EventRepository:
    """Thread-safe SQLite repository with WAL mode enabled for crossing events."""

    def __init__(self, db_path: str = "output/events.db"):
        self.db_path = db_path
        self._ensure_parent_directory()

    def _ensure_parent_directory(self) -> None:
        """Create parent directory for SQLite database if missing."""
        parent = Path(self.db_path).parent
        if parent and not parent.exists():
            parent.mkdir(parents=True, exist_ok=True)

    def _get_connection(self) -> sqlite3.Connection:
        """Create and configure a SQLite connection with WAL mode."""
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def initialize(self) -> None:
        """Initialize database schema and indices idempotently."""
        self._ensure_parent_directory()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
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
                """
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_events_timestamp ON crossing_events(timestamp);"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_events_track_id ON crossing_events(track_id);"
            )
            conn.commit()
            logger.info("SQLite EventRepository initialized in WAL mode at %s", self.db_path)

    def insert_event(self, record: CrossingRecord) -> int:
        """Insert crossing record into database.

        Returns:
            The newly inserted record ID.
        """
        query = """
            INSERT INTO crossing_events (
                timestamp, track_id, direction, shoes_detected, shoe_count,
                max_confidence, bboxes_json, full_image_path, crop_image_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    record.timestamp,
                    record.track_id,
                    record.direction,
                    1 if record.shoes_detected else 0,
                    record.shoe_count,
                    record.max_confidence,
                    record.bboxes_json,
                    record.full_image_path,
                    record.crop_image_path,
                ),
            )
            conn.commit()
            return cursor.lastrowid

    def get_events_by_track(self, track_id: int) -> List[CrossingRecord]:
        """Query crossing events for a specific track ID."""
        query = "SELECT * FROM crossing_events WHERE track_id = ? ORDER BY id ASC;"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (track_id,))
            rows = cursor.fetchall()
            return [self._row_to_record(row) for row in rows]

    def get_all_events(self, limit: int = 100) -> List[CrossingRecord]:
        """Query recent crossing events."""
        query = "SELECT * FROM crossing_events ORDER BY id DESC LIMIT ?;"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
            return [self._row_to_record(row) for row in rows]

    def count_events(self) -> int:
        """Return total number of recorded crossing events."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM crossing_events;")
            return cursor.fetchone()[0]

    @staticmethod
    def _row_to_record(row: sqlite3.Row) -> CrossingRecord:
        """Convert SQLite row to CrossingRecord dataclass."""
        return CrossingRecord(
            id=row["id"],
            timestamp=row["timestamp"],
            track_id=row["track_id"],
            direction=row["direction"],
            shoes_detected=bool(row["shoes_detected"]),
            shoe_count=row["shoe_count"],
            max_confidence=row["max_confidence"],
            bboxes_json=row["bboxes_json"],
            full_image_path=row["full_image_path"],
            crop_image_path=row["crop_image_path"],
        )
