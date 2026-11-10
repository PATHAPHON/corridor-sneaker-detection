# 03: Roboflow Auto-Label and YOLO Export

**What to build:** Execute Auto-Label on Roboflow Annotate tab using prompt `sneaker`, generate dataset version 1, and export the dataset as YOLOv11 PyTorch into `datasets/sneakers/` ready for model fine-tuning.

**Blocked by:** 02: Bulk Dataset Upload and Split

**Status:** done

- [x] Provide automated download script (`scripts/download_from_roboflow.py`) ready to pull YOLOv11 dataset once Version 1 is generated.
- [x] Execute Roboflow Auto-Label on Roboflow Annotate UI with prompt `sneaker` across all uploaded images.
- [x] Spot-check 10 annotations on Roboflow UI for tight bounding box coverage around footwear.
- [x] Generate Dataset Version 1 on Roboflow Web UI.
- [x] Run `scripts/download_from_roboflow.py` to export dataset in YOLOv11 PyTorch format to `datasets/sneakers/data.yaml`.
