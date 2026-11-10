"""Main application entrypoint for the CV monitoring pipeline."""
import argparse
import logging
import sys
from typing import Optional

from src.capture.camera import CameraFrameSource
from src.capture.synthetic import SyntheticFrameSource
from src.capture.video_file import VideoFileFrameSource
from src.config.settings import PipelineConfig
from src.pipeline.coordinator import PipelineCoordinator, ProcessedCrossingEvent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("main")


def on_crossing_event(event: ProcessedCrossingEvent) -> None:
    """Callback triggered whenever background worker completes sneaker inspection."""
    status = "COMPLIANT (Sneakers)" if event.inspection.shoes_detected else "NON-COMPLIANT (No Sneakers)"
    saved_info = f" | DB ID: #{event.record_id} | Crop: {event.crop_image_path}" if event.record_id else ""
    logger.info(
        "Crossing Detected! Track ID: %d | Time: %.2fs | Sneaker Count: %d | Status: %s | Conf: %s%s",
        event.track_id,
        event.timestamp,
        event.inspection.sneaker_count,
        status,
        [round(c, 2) for c in event.inspection.confidences],
        saved_info,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Real-Time Pedestrian Footwear Inspection Pipeline")
    parser.add_argument("--video", type=str, default=None, help="Path to input video file")
    parser.add_argument("--camera", type=int, default=0, help="Webcam device index (default: 0)")
    parser.add_argument("--synthetic", action="store_true", help="Run with synthetic frame generator")
    parser.add_argument("--frames", type=int, default=100, help="Number of synthetic frames (default: 100)")
    parser.add_argument("--no-gui", action="store_true", help="Disable GUI preview window (headless mode)")
    parser.add_argument("--no-storage", action="store_true", help="Disable SQLite and image evidence persistence")
    parser.add_argument("--db-path", type=str, default="output/events.db", help="SQLite database path")
    parser.add_argument("--capture-dir", type=str, default="output/captures", help="Evidence images directory")

    args = parser.parse_args()
    config = PipelineConfig(
        enable_storage=not args.no_storage,
        db_path=args.db_path,
        capture_dir=args.capture_dir,
    )

    if args.synthetic:
        logger.info("Using SyntheticFrameSource (%d frames)...", args.frames)
        frame_source = SyntheticFrameSource(total_frames=args.frames, simulate_wall_clock=True)
    elif args.video:
        logger.info("Using VideoFileFrameSource from: %s", args.video)
        frame_source = VideoFileFrameSource(args.video)
    else:
        logger.info("Using CameraFrameSource device index: %d", args.camera)
        frame_source = CameraFrameSource(device_index=args.camera)

    show_preview = not args.no_gui
    coordinator = PipelineCoordinator(
        frame_source=frame_source,
        config=config,
        on_event_processed=on_crossing_event,
        show_preview=show_preview,
    )

    logger.info("Starting pipeline coordinator (GUI: %s)... Press 'q' or Ctrl+C to terminate.", show_preview)
    try:
        coordinator.run()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal. Shutting down gracefully...")
    finally:
        logger.info("Pipeline terminated. Dropped events count: %d", coordinator.dropped_events_count)


if __name__ == "__main__":
    main()
