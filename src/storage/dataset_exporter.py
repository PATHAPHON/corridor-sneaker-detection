"""Active dataset curation and YOLO export utility."""
import json
import logging
import random
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple
import cv2
import yaml

from src.storage.repository import CrossingRecord, EventRepository

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ExportSummary:
    """Summary metrics of exported dataset."""
    total_exported: int
    train_count: int
    val_count: int
    negative_count: int


class DatasetExporter:
    """Exports captured lower-body crops from SQLite into standard YOLO dataset format."""

    def __init__(self, db_path: str = "output/events.db", output_dir: str = "datasets/sneakers_live"):
        self.db_path = db_path
        self.output_dir = Path(output_dir)

    def export(
        self,
        train_ratio: float = 0.8,
        min_confidence: Optional[float] = None,
        seed: int = 42,
    ) -> ExportSummary:
        """Export images and normalized bounding boxes for YOLO training.

        Args:
            train_ratio: Proportion of images assigned to train split (remainder to val).
            min_confidence: Optional minimum confidence filter for positive detections.
            seed: Random seed for reproducible dataset splits.

        Returns:
            ExportSummary containing split instance counts.
        """
        random.seed(seed)
        repo = EventRepository(db_path=self.db_path)
        records = repo.get_all_events(limit=10000)

        # Setup destination directories
        train_img_dir = self.output_dir / "images" / "train"
        val_img_dir = self.output_dir / "images" / "val"
        train_lbl_dir = self.output_dir / "labels" / "train"
        val_lbl_dir = self.output_dir / "labels" / "val"

        for d in [train_img_dir, val_img_dir, train_lbl_dir, val_lbl_dir]:
            d.mkdir(parents=True, exist_ok=True)

        total_exported = 0
        train_count = 0
        val_count = 0
        negative_count = 0

        for record in records:
            crop_path = Path(record.crop_image_path)
            if not crop_path.exists():
                logger.warning("Referenced crop path not found: %s", crop_path)
                continue

            img = cv2.imread(str(crop_path))
            if img is None:
                logger.warning("Failed to decode crop image: %s", crop_path)
                continue

            h, w = img.shape[:2]
            if h <= 0 or w <= 0:
                continue

            # Determine split
            is_train = random.random() < train_ratio
            dest_img_dir = train_img_dir if is_train else val_img_dir
            dest_lbl_dir = train_lbl_dir if is_train else val_lbl_dir

            dest_img_path = dest_img_dir / crop_path.name
            dest_lbl_path = dest_lbl_dir / f"{crop_path.stem}.txt"

            # Copy image
            shutil.copy2(str(crop_path), str(dest_img_path))

            # Parse bounding boxes
            yolo_lines: List[str] = []
            try:
                bboxes_data = json.loads(record.bboxes_json) if record.bboxes_json else []
            except Exception:
                bboxes_data = []

            for item in bboxes_data:
                conf = item.get("confidence", 1.0)
                if min_confidence is not None and conf < min_confidence:
                    continue

                box = item.get("box", [])
                if len(box) == 4:
                    x1, y1, x2, y2 = box
                    # Clamp coordinates to image boundaries
                    x1 = max(0.0, min(float(w), float(x1)))
                    x2 = max(0.0, min(float(w), float(x2)))
                    y1 = max(0.0, min(float(h), float(y1)))
                    y2 = max(0.0, min(float(h), float(y2)))

                    box_w = x2 - x1
                    box_h = y2 - y1
                    if box_w > 0 and box_h > 0:
                        cx = (x1 + x2) / (2.0 * w)
                        cy = (y1 + y2) / (2.0 * h)
                        norm_w = box_w / w
                        norm_h = box_h / h
                        yolo_lines.append(f"0 {cx:.6f} {cy:.6f} {norm_w:.6f} {norm_h:.6f}")

            # Write label file (empty file for negative background crops)
            with open(dest_lbl_path, "w") as f:
                if yolo_lines:
                    f.write("\n".join(yolo_lines) + "\n")
                else:
                    f.write("")

            total_exported += 1
            if is_train:
                train_count += 1
            else:
                val_count += 1

            if not yolo_lines:
                negative_count += 1

        # Write data.yaml
        data_yaml_content = {
            "path": str(self.output_dir.resolve()),
            "train": "images/train",
            "val": "images/val",
            "names": {0: "sneaker"},
        }
        with open(self.output_dir / "data.yaml", "w") as f:
            yaml.dump(data_yaml_content, f, sort_keys=False)

        logger.info(
            "YOLO dataset export complete: %d total (%d train, %d val, %d negative)",
            total_exported,
            train_count,
            val_count,
            negative_count,
        )

        return ExportSummary(
            total_exported=total_exported,
            train_count=train_count,
            val_count=val_count,
            negative_count=negative_count,
        )
