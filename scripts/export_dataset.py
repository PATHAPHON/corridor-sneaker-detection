"""CLI utility to export captured foot crops from SQLite to YOLO dataset format."""
import argparse
import logging
from src.storage.dataset_exporter import DatasetExporter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("export_dataset")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export SQLite foot crops to YOLO dataset format")
    parser.add_argument("--db-path", type=str, default="output/events.db", help="SQLite database path")
    parser.add_argument("--output-dir", type=str, default="datasets/sneakers_live", help="YOLO export directory")
    parser.add_argument("--train-ratio", type=float, default=0.8, help="Train split ratio (default: 0.8)")
    parser.add_argument("--min-confidence", type=float, default=None, help="Filter out detections below confidence")

    args = parser.parse_args()

    exporter = DatasetExporter(db_path=args.db_path, output_dir=args.output_dir)
    summary = exporter.export(train_ratio=args.train_ratio, min_confidence=args.min_confidence)
    logger.info(
        "Export finished successfully: Total=%d (Train=%d, Val=%d, Negatives=%d) -> %s",
        summary.total_exported,
        summary.train_count,
        summary.val_count,
        summary.negative_count,
        args.output_dir,
    )


if __name__ == "__main__":
    main()
