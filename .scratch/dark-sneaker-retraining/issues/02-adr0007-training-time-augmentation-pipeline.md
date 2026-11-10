# 02: ADR-0007 Training-Time Augmentation Pipeline

**What to build:** An upgraded sneaker model fine-tuning pipeline and CLI that warm-starts from existing Sneaker Detector weights and forwards the full ADR-0007 training-time augmentation suite (`hsv_s=0.7`, `hsv_v=0.4`, `degrees=10.0`, `erasing=0.2`, `fliplr=0.5`, `mosaic=1.0`, `scale=0.5`) to achieve invariance to dark footwear, stride angle tilt, and leg depth occlusion with zero runtime overhead.

**Blocked by:** 01 (Manifest Dataset Merger with Hallway Oversampling)

**Status:** done

- [x] Training function and CLI accept and forward `hsv_h`, `hsv_s=0.7`, `hsv_v=0.4`, `degrees=10.0`, `erasing=0.2`, `fliplr=0.5`, `mosaic=1.0`, and `scale=0.5` to the YOLO trainer
- [x] Supports warm-starting from existing production sneaker weights for 30 epochs on `mps` (with CUDA/CPU fallback)
- [x] Preserves Invariant 7 by introducing zero image preprocessing filters into runtime capture or worker threads
- [x] Seam unit tests verify hyperparameter defaults and exact argument forwarding to the trainer
