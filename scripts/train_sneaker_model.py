"""Train fine-tuned single-class YOLO11 Nano model for sneaker detection with ADR-0007 augmentations."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
import torch
from ultralytics import YOLO


def resolve_device(requested_device: str | None = None) -> str:
    """Resolve the optimal compute device (MPS -> CUDA -> CPU)."""
    if requested_device:
        return requested_device

    if torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def train_sneaker_model(
    data_yaml: str | Path = "datasets/sneakers_merged/data.yaml",
    base_model: str = "models/yolo-sneaker.pt",
    epochs: int = 30,
    batch_size: int = 16,
    imgsz: int = 640,
    patience: int = 0,
    mosaic: float = 1.0,
    scale: float = 0.5,
    hsv_h: float = 0.015,
    hsv_s: float = 0.7,
    hsv_v: float = 0.4,
    degrees: float = 10.0,
    fliplr: float = 0.5,
    erasing: float = 0.2,
    close_mosaic: int = 10,
    device: str | None = None,
    project: str = "runs/detect",
    name: str = "sneaker_yolo11n_merged",
) -> Path:
    """
    Fine-tune YOLO11 Nano detector on single-class sneaker dataset with ADR-0007 augmentations.

    Returns:
        Path: Path to the best checkpoint weights file.
    """
    data_path = Path(data_yaml).resolve()
    if not data_path.is_file():
        raise FileNotFoundError(f"Dataset config not found at: {data_path}")

    selected_device = resolve_device(device)
    project_dir = str(Path(project).resolve())
    print(f"Initializing YOLO model '{base_model}' on device: {selected_device}")

    model = YOLO(base_model)

    print(
        f"Starting training on {data_path} for {epochs} epochs (batch={batch_size}, imgsz={imgsz})...\n"
        f"  Augmentations: mosaic={mosaic}, scale={scale}, hsv_s={hsv_s}, hsv_v={hsv_v}, "
        f"degrees={degrees}, fliplr={fliplr}, erasing={erasing}, close_mosaic={close_mosaic}"
    )

    results = model.train(
        data=str(data_path),
        epochs=epochs,
        batch=batch_size,
        imgsz=imgsz,
        patience=patience,
        mosaic=mosaic,
        scale=scale,
        hsv_h=hsv_h,
        hsv_s=hsv_s,
        hsv_v=hsv_v,
        degrees=degrees,
        fliplr=fliplr,
        erasing=erasing,
        close_mosaic=close_mosaic,
        device=selected_device,
        project=project_dir,
        name=name,
        exist_ok=True,
        save=True,
        verbose=True,
    )

    best_weight = Path(results.save_dir) / "weights" / "best.pt"
    if not best_weight.is_file():
        raise RuntimeError(f"Expected best weight file not found at: {best_weight}")

    print(f"\nTraining completed successfully.")
    print(f"Best weight saved at: {best_weight}")
    return best_weight


def main() -> None:
    """CLI entry point for training sneaker model."""
    parser = argparse.ArgumentParser(description="Fine-tune YOLO11 Nano model with ADR-0007 augmentations")
    parser.add_argument("--data", type=str, default="datasets/sneakers_merged/data.yaml", help="Path to data.yaml")
    parser.add_argument("--base-model", type=str, default="models/yolo-sneaker.pt", help="Pretrained base YOLO weights")
    parser.add_argument("--epochs", type=int, default=30, help="Maximum training epochs")
    parser.add_argument("--batch", type=int, default=16, help="Training batch size")
    parser.add_argument("--imgsz", type=int, default=640, help="Input image dimension")
    parser.add_argument("--patience", type=int, default=0, help="Early stopping patience (0 to disable)")
    parser.add_argument("--mosaic", type=float, default=1.0, help="Mosaic augmentation probability")
    parser.add_argument("--scale", type=float, default=0.5, help="Scale augmentation gain")
    parser.add_argument("--hsv-s", type=float, default=0.7, help="HSV saturation fraction")
    parser.add_argument("--hsv-v", type=float, default=0.4, help="HSV value/brightness fraction")
    parser.add_argument("--degrees", type=float, default=10.0, help="Rotation degrees")
    parser.add_argument("--fliplr", type=float, default=0.5, help="Horizontal flip probability")
    parser.add_argument("--erasing", type=float, default=0.2, help="Random erasing cutout probability")
    parser.add_argument("--close-mosaic", type=int, default=10, help="Disable mosaic in last N epochs")
    parser.add_argument("--device", type=str, default=None, help="Hardware device ('mps', 'cuda', 'cpu')")
    parser.add_argument("--project", type=str, default="runs/detect", help="Results save directory")
    parser.add_argument("--name", type=str, default="sneaker_yolo11n_merged", help="Run identifier name")

    args = parser.parse_args()

    try:
        best_pt = train_sneaker_model(
            data_yaml=args.data,
            base_model=args.base_model,
            epochs=args.epochs,
            batch_size=args.batch,
            imgsz=args.imgsz,
            patience=args.patience,
            mosaic=args.mosaic,
            scale=args.scale,
            hsv_s=args.hsv_s,
            hsv_v=args.hsv_v,
            degrees=args.degrees,
            fliplr=args.fliplr,
            erasing=args.erasing,
            close_mosaic=args.close_mosaic,
            device=args.device,
            project=args.project,
            name=args.name,
        )
        print(f"Training run finished: {best_pt}")
    except Exception as e:
        print(f"Error during training: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
