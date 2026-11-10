# 03: Metric Evaluation, Latency Benchmark, and Model Export

**What to build:** Mathematically evaluate model metrics on the held-out test split, benchmark MPS inference throughput, export the validated model weights, and produce annotated visual inspection evidence.

**Blocked by:** 02: Sneaker YOLO11n Model Fine-Tuning

**Status:** done

- [x] Execute evaluation on the test split (`datasets/sneakers/test`) computing mAP50, Recall, and Precision.
- [x] Verify that model metrics satisfy acceptance thresholds: mAP50 >= 0.65, Recall >= 0.90, and Precision >= 0.85.
- [x] Measure pure forward-pass inference latency and throughput (FPS) on MPS over repeated benchmark iterations.
- [x] Export best trained checkpoint to canonical destination `models/yolo-sneaker.pt`.
- [x] Run inference on sample test image to generate visual evidence annotated with bounding boxes, labels, and confidence overlays.
