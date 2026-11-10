"""Download annotated sneaker dataset version from Roboflow in YOLOv11 format."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
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


def main() -> None:
    """Download the specified YOLO dataset version from Roboflow to disk."""
    default_slug = os.getenv("ROBOFLOW_PROJECT_SLUG", "sneaker-detection-fggnt")
    parser = argparse.ArgumentParser(description="Download annotated sneaker dataset from Roboflow")
    parser.add_argument("--version", type=int, default=1, help="Dataset version number on Roboflow")
    parser.add_argument("--project-slug", type=str, default=default_slug, help="Roboflow project slug")
    parser.add_argument("--output-dir", type=str, default="datasets/sneakers", help="Target export directory")
    parser.add_argument("--model-format", type=str, default="yolov11", help="YOLO format ('yolov11' or 'yolov8')")
    args = parser.parse_args()

    env_vars = load_env_file(".env")
    api_key = os.getenv("ROBOFLOW_API_KEY") or env_vars.get("ROBOFLOW_API_KEY")
    workspace_name = os.getenv("ROBOFLOW_WORKSPACE") or env_vars.get("ROBOFLOW_WORKSPACE")

    if not api_key or not workspace_name:
        print("Error: Roboflow credentials not found in environment or .env", file=sys.stderr)
        sys.exit(1)

    print(f"Connecting to Roboflow workspace '{workspace_name}'...")
    rf = Roboflow(api_key=api_key)
    ws = rf.workspace(workspace_name)
    project = ws.project(args.project_slug)

    print(f"Fetching Version {args.version} for project '{args.project_slug}'...")
    try:
        version_obj = project.version(args.version)
    except Exception as e:
        print(f"Failed to access Version {args.version}: {e}", file=sys.stderr)
        print("Make sure you have generated Version 1 on the Roboflow web dashboard first.", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Downloading dataset in '{args.model_format}' format to {output_path}...")
    dataset = version_obj.download(
        model_format=args.model_format,
        location=str(output_path),
        overwrite=True,
    )
    print(f"\nDataset successfully downloaded to: {dataset.location}")
    print(f"data.yaml location: {output_path / 'data.yaml'}")


if __name__ == "__main__":
    main()
