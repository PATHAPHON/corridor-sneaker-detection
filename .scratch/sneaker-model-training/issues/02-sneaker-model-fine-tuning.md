# 02: Sneaker YOLO11n Model Fine-Tuning

**What to build:** Execute fine-tuning of pretrained YOLO11 Nano detector on the single-class sneaker dataset using mosaic and scale augmentations with automated early stopping.

**Blocked by:** 01: Project Dependencies and Hardware Acceleration Preflight

**Status:** done

- [x] Provide fine-tuning script targeting single class `0: sneaker` on the dataset defined in `datasets/sneakers/data.yaml`.
- [x] Configure training parameters to 50 epochs, batch size 16, input resolution 640x640, and early stopping patience of 10 epochs.
- [x] Enable mosaic (1.0) and scale (0.5) data augmentations to bridge domain gap between dataset images and lower-body ROI crops.
- [x] Execute training run utilizing Metal Performance Shaders (MPS) device acceleration.
