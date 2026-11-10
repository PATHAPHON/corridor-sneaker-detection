"""Roboflow Dataset Ingestion Script for Sneaker Detection.

Uploads images from local dataset to Roboflow workspace, organizing them with
standard Train/Validation/Test splits for YOLO11 training.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import List, Tuple
from roboflow import Roboflow


def load_env_file(filepath: Path | str = ".env") -> dict[str, str]:
    """Parse key-value pairs from a .env file."""
    env_vars = {}
    env_path = Path(filepath)
    if not env_path.is_file():
        return env_vars

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env_vars[k.strip()] = v.strip().strip("\"'")
    return env_vars


def collect_images(base_dir: Path) -> List[Path]:
    """Collect all valid sneaker images from training and validation folders."""
    extensions = ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.webp")
    images: List[Path] = []
    
    subdirs = ["training/sneakers", "validation/sneakers"]
    for sub in subdirs:
        dir_path = base_dir / sub
        if not dir_path.exists():
            print(f"Warning: Directory not found: {dir_path}")
            continue
        for ext in extensions:
            images.extend(dir_path.glob(ext))

    # Fallback: scan any image under base_dir recursively if subdirs empty
    if not images:
        for ext in extensions:
            images.extend(base_dir.rglob(ext))

    images = sorted(list(set(images)))
    return images


def assign_splits(images: List[Path], train_ratio: float = 0.70, valid_ratio: float = 0.20) -> List[Tuple[Path, str]]:
    """Assign deterministic splits (train/valid/test) to an image list."""
    total = len(images)
    n_train = int(total * train_ratio)
    n_valid = int(total * valid_ratio)
    
    assigned: List[Tuple[Path, str]] = []
    for idx, img_path in enumerate(images):
        if idx < n_train:
            split = "train"
        elif idx < n_train + n_valid:
            split = "valid"
        else:
            split = "test"
        assigned.append((img_path, split))
    return assigned


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload sneaker dataset to Roboflow")
    default_dataset_dir = os.getenv("SNEAKER_DATASET_DIR", "/Users/pat/Downloads/shoeTypeClassifierDataset")
    parser.add_argument("--dataset-dir", type=str, default=default_dataset_dir,
                        help="Path to source shoe dataset directory (default: SNEAKER_DATASET_DIR env or local path)")
    parser.add_argument("--project-name", type=str, default="sneaker-detection",
                        help="Roboflow project name")
    parser.add_argument("--test-one", action="store_true",
                        help="Upload only 1 image as a verification test")
    parser.add_argument("--batch-name", type=str, default="kaggle-sneakers",
                        help="Roboflow upload batch identifier")
    args = parser.parse_args()

    # 1. Credentials
    env_vars = load_env_file(".env")
    api_key = os.getenv("ROBOFLOW_API_KEY") or env_vars.get("ROBOFLOW_API_KEY")
    workspace_name = os.getenv("ROBOFLOW_WORKSPACE") or env_vars.get("ROBOFLOW_WORKSPACE")

    if not api_key or "your_" in api_key:
        print("Error: ROBOFLOW_API_KEY not configured in .env", file=sys.stderr)
        sys.exit(1)
    if not workspace_name or "your_" in workspace_name:
        print("Error: ROBOFLOW_WORKSPACE not configured in .env", file=sys.stderr)
        sys.exit(1)

    print(f"Connecting to Roboflow workspace: {workspace_name}...")
    rf = Roboflow(api_key=api_key)
    ws = rf.workspace(workspace_name)

    # 2. Project resolution
    existing_project_slugs = [str(p).split("/")[-1] for p in ws.projects()]
    print(f"Existing project slugs in workspace: {existing_project_slugs}")

    matched_slug = None
    for slug in existing_project_slugs:
        if slug == args.project_name or slug.startswith(f"{args.project_name}-"):
            matched_slug = slug
            break

    if matched_slug:
        print(f"Found matching project: '{matched_slug}'")
        project = ws.project(matched_slug)
    else:
        print(f"Creating new object-detection project: '{args.project_name}'...")
        try:
            project = ws.create_project(
                project_name=args.project_name,
                project_type="object-detection",
                project_license="CC BY 4.0",
                annotation="sneaker",
            )
            print(f"Project '{args.project_name}' created successfully (id: {project.id}).")
        except Exception as e:
            print(f"Failed to create project: {e}", file=sys.stderr)
            sys.exit(1)

    # 3. Collect Images
    dataset_dir = Path(args.dataset_dir)
    images = collect_images(dataset_dir)
    print(f"Found {len(images)} images in {dataset_dir}")
    if not images:
        print("No images found to upload.", file=sys.stderr)
        sys.exit(1)

    assigned = assign_splits(images)
    train_count = sum(1 for _, s in assigned if s == "train")
    val_count = sum(1 for _, s in assigned if s == "valid")
    test_count = sum(1 for _, s in assigned if s == "test")
    print(f"Split distribution: {train_count} train, {val_count} valid, {test_count} test")

    # 4. Upload Execution
    targets = assigned[:1] if args.test_one else assigned
    print(f"Target images to upload: {len(targets)} (test_one={args.test_one})")

    success_count = 0
    fail_count = 0

    for idx, (img_path, split) in enumerate(targets, start=1):
        try:
            print(f"[{idx}/{len(targets)}] Uploading {img_path.name} to split '{split}'...", end=" ", flush=True)
            res = project.upload(
                image_path=str(img_path),
                split=split,
                batch_name=args.batch_name,
                tag_names=["kaggle-sneakers"],
                num_retry_uploads=3,
            )
            is_dup = False
            if isinstance(res, list) and len(res) > 0 and isinstance(res[0], dict):
                is_dup = res[0].get("image", {}).get("duplicate", False)
            if is_dup:
                print("OK (duplicate)")
            else:
                print("OK")
            success_count += 1
        except Exception as e:
            print(f"FAILED: {e}")
            fail_count += 1

    print("\n" + "=" * 50)
    print(f"Upload Summary: {success_count} succeeded, {fail_count} failed out of {len(targets)} attempted.")
    project_slug = getattr(project, "id", f"{workspace_name}/{args.project_name}").split("/")[-1]
    print(f"Project URL: https://app.roboflow.com/{workspace_name}/{project_slug}")
    print("=" * 50)

    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
