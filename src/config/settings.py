"""Configuration models and system tunables."""
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class PipelineConfig:
    """Tunable parameters for the computer vision monitoring pipeline."""
    # Model paths
    person_model_path: str = "yolo11n.pt"
    sneaker_model_path: str = "models/yolo-sneaker.pt"

    # Thresholds
    person_confidence: float = 0.50
    sneaker_confidence: float = 0.40

    # Multi-Object Tracking Configuration
    tracker_config: str = "src/config/bytetrack.yaml"

    # Tripwire Line Coordinates (Lateral Side-View per ADR-0005: Vertical line dividing Left/Right)
    # If None, automatically centers vertically across the active frame: (w // 2, 0) -> (w // 2, h)
    tripwire_start: Optional[Tuple[int, int]] = None
    tripwire_end: Optional[Tuple[int, int]] = None
    tripwire_cooldown_seconds: float = 2.0

    # Concurrency and Queue Limits
    queue_maxsize: int = 20

    # Data Persistence & Evidence Storage per ADR-0004
    enable_storage: bool = True
    db_path: str = "output/events.db"
    capture_dir: str = "output/captures"

    # Hardware acceleration override ("mps", "cuda", "cpu" or None for auto)
    device: Optional[str] = None
