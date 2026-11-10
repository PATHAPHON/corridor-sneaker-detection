"""Merge baseline and live YOLO datasets using manifests with domain oversampling."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any
import yaml


def resolve_split_images(data_yaml_path: Path, split_key: str) -> list[Path]:
    """Resolve image file paths for a dataset split from data.yaml."""
    data_yaml_path = data_yaml_path.resolve()
    with open(data_yaml_path, "r", encoding="utf-8") as f:
        config: dict[str, Any] = yaml.safe_load(f)

    if split_key not in config or not config[split_key]:
        return []

    split_val = config[split_key]
    base_dir = data_yaml_path.parent
    if "path" in config and config["path"]:
        declared_path = Path(config["path"])
        if declared_path.is_absolute():
            base_dir = declared_path
        else:
            base_dir = (data_yaml_path.parent / declared_path).resolve()

    target_path = Path(split_val)
    if not target_path.is_absolute():
        target_path = (base_dir / target_path).resolve()

    if not target_path.exists():
        fallback = (data_yaml_path.parent / split_val).resolve()
        fallback2 = (data_yaml_path.parent / split_val.replace("../", "")).resolve()
        if fallback.exists():
            target_path = fallback
        elif fallback2.exists():
            target_path = fallback2

    if target_path.is_file() and target_path.suffix in (".txt", ".text"):
        with open(target_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        return [Path(line).resolve() for line in lines]

    if target_path.is_dir():
        image_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
        images = [p.resolve() for p in target_path.rglob("*") if p.suffix.lower() in image_exts]
        images.sort()
        return images

    return []


def find_label_for_image(image_path: Path) -> Path | None:
    """Find corresponding YOLO label .txt file for an image path."""
    image_path = image_path.resolve()
    stem = image_path.stem
    str_path = str(image_path)

    if "/images/" in str_path:
        candidate = Path(str_path.replace("/images/", "/labels/")).with_suffix(".txt")
        if candidate.is_file():
            return candidate

    candidate = image_path.parent.parent / "labels" / f"{stem}.txt"
    if candidate.is_file():
        return candidate

    candidate = image_path.with_suffix(".txt")
    if candidate.is_file():
        return candidate

    return None


def verify_labels_exist(images: list[Path]) -> list[tuple[Path, Path]]:
    """Verify that every image has an existing label file."""
    matched = []
    for img in images:
        lbl = find_label_for_image(img)
        if lbl is None or not lbl.is_file():
            raise FileNotFoundError(f"Missing label file for image: {img}")
        matched.append((img, lbl))
    return matched


def merge_datasets(
    baseline_yaml: str | Path = "datasets/sneakers/data.yaml",
    live_yaml: str | Path = "datasets/sneakers_live/data.yaml",
    output_dir: str | Path = "datasets/sneakers_merged",
    live_oversample_factor: int = 5,
) -> dict[str, Any]:
    """
    Merge baseline and live datasets via absolute-path manifest txt files.

    Args:
        baseline_yaml: Path to baseline dataset data.yaml
        live_yaml: Path to live hallway dataset data.yaml
        output_dir: Directory to write manifests and data.yaml
        live_oversample_factor: Repetition factor for live hallway training set

    Returns:
        dict: Summary containing image counts per split.
    """
    base_yaml_path = Path(baseline_yaml).resolve()
    live_yaml_path = Path(live_yaml).resolve()
    out_path = Path(output_dir).resolve()
    out_path.mkdir(parents=True, exist_ok=True)

    base_train = resolve_split_images(base_yaml_path, "train")
    base_val = resolve_split_images(base_yaml_path, "val")
    base_test = resolve_split_images(base_yaml_path, "test")

    live_train = resolve_split_images(live_yaml_path, "train")
    live_val = resolve_split_images(live_yaml_path, "val")

    verify_labels_exist(base_train)
    verify_labels_exist(base_val)
    verify_labels_exist(base_test)
    verify_labels_exist(live_train)
    verify_labels_exist(live_val)

    oversampled_live_train: list[Path] = []
    for _ in range(live_oversample_factor):
        oversampled_live_train.extend(live_train)

    merged_train = base_train + oversampled_live_train
    merged_val = base_val + live_val
    merged_test = base_test

    train_txt = out_path / "train.txt"
    val_txt = out_path / "val.txt"
    test_txt = out_path / "test.txt"

    with open(train_txt, "w", encoding="utf-8") as f:
        for p in merged_train:
            f.write(f"{p}\n")

    with open(val_txt, "w", encoding="utf-8") as f:
        for p in merged_val:
            f.write(f"{p}\n")

    with open(test_txt, "w", encoding="utf-8") as f:
        for p in merged_test:
            f.write(f"{p}\n")

    data_yaml_file = out_path / "data.yaml"
    merged_config = {
        "path": str(out_path),
        "train": "train.txt",
        "val": "val.txt",
        "test": "test.txt",
        "names": {0: "sneaker"},
        "metadata": {
            "baseline_train": len(base_train),
            "baseline_val": len(base_val),
            "baseline_test": len(base_test),
            "live_train": len(live_train),
            "live_val": len(live_val),
            "live_oversample_factor": live_oversample_factor,
            "total_train": len(merged_train),
            "total_val": len(merged_val),
            "total_test": len(merged_test),
        },
    }

    with open(data_yaml_file, "w", encoding="utf-8") as f:
        yaml.safe_dump(merged_config, f, sort_keys=False)

    summary = {
        "output_dir": str(out_path),
        "data_yaml": str(data_yaml_file),
        "train_count": len(merged_train),
        "val_count": len(merged_val),
        "test_count": len(merged_test),
        "baseline_train": len(base_train),
        "live_train_unique": len(live_train),
        "oversample_factor": live_oversample_factor,
    }

    return summary


def main() -> None:
    """CLI interface for dataset merger."""
    parser = argparse.ArgumentParser(description="Merge baseline and live datasets using manifests")
    parser.add_argument("--baseline", type=str, default="datasets/sneakers/data.yaml")
    parser.add_argument("--live", type=str, default="datasets/sneakers_live/data.yaml")
    parser.add_argument("--output", type=str, default="datasets/sneakers_merged")
    parser.add_argument("--oversample", type=int, default=5)

    args = parser.parse_args()
    summary = merge_datasets(
        baseline_yaml=args.baseline,
        live_yaml=args.live,
        output_dir=args.output,
        live_oversample_factor=args.oversample,
    )
    print(f"Dataset merge complete: {summary['output_dir']}")
    print(f"  Train: {summary['train_count']} ({summary['baseline_train']} base + {summary['live_train_unique']} live x {summary['oversample_factor']})")
    print(f"  Val:   {summary['val_count']}")
    print(f"  Test:  {summary['test_count']}")


if __name__ == "__main__":
    main()
