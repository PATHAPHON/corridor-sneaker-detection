# Spec: Sneaker Model Fine-Tuning & Evaluation Pipeline

## Problem Statement

The retail corridor tripwire monitoring system requires verifying whether pedestrians crossing the virtual boundary are wearing sneakers (ADR-0003). While the annotated single-class dataset (Version 1: 190 train, 56 validation, 28 test) is now downloaded and verified in the repository, no trained detector weights exist yet for footwear inspection. Attempting to run detection without a dedicated fine-tuned model blocks downstream footwear ROI extraction and crossing event persistence. Furthermore, the model must achieve sufficient detection precision and recall to avoid false alarms or missed detections without causing latency bottlenecks in the decoupled concurrency pipeline.

## Solution

We build an automated training and evaluation pipeline for a fine-tuned single-class YOLO11 Nano detector:
1. Establish project dependency standards by defining a pyproject configuration pinned via uv.
2. Fine-tune a pretrained YOLO11 Nano model on the annotated sneaker dataset targeting single class `0: sneaker`.
3. Apply mosaic and scale augmentations during training to generalize from close-up images to lower-body ROI crops.
4. Leverage Apple Silicon Metal hardware acceleration for efficient local training and low-latency inference.
5. Implement an automated evaluation and quality gate verifying model metrics against strict acceptance thresholds (mAP50, Recall, Precision).
6. Benchmark pure inference latency and throughput (FPS) on Metal Performance Shaders (MPS) and CPU.
7. Persist validated model weights and visual detection evidence for downstream pipeline integration.

## User Stories

1. As a computer vision developer, I want the project dependencies cleanly declared and reproducible in a pyproject configuration, so that all contributors and execution agents run on identical library versions.
2. As a computer vision developer, I want to initiate model fine-tuning from a pretrained YOLO11 Nano checkpoint, so that feature representations transfer effectively to sneaker recognition with minimal training time.
3. As a machine learning engineer, I want training to execute with mosaic and scale augmentations, so that the detector learns scale invariance and handles varied shoe distances within lower-body crops.
4. As a machine learning engineer, I want training to utilize Apple Silicon Metal acceleration automatically when available, so that training completes within 2–3 minutes on local hardware.
5. As a developer, I want training to enforce early stopping with patience, so that training terminates when validation loss stops improving and avoids overfitting.
6. As a quality engineer, I want an automated evaluation gate verifying that mAP50 reaches at least 0.65 on the test split, so that the baseline detection quality is mathematically verified before acceptance.
7. As a system operator, I want model Recall on the test split to reach at least 0.90, so that missed shoe detections (false negatives) are minimized.
8. As a system operator, I want model Precision on the test split to reach at least 0.85, so that floor patterns, socks, or non-sneaker items are not falsely classified as sneakers.
9. As a performance engineer, I want to benchmark single-frame model inference latency and throughput (FPS) on MPS, so that we guarantee the detector satisfies the real-time decoupled concurrency budget.
10. As a computer vision developer, I want the best performing model weights exported directly to the canonical model destination, so that downstream pipeline components can load it consistently.
11. As a developer, I want the evaluation script to run inference on a sample test image and output annotated visual evidence, so that bounding boxes, labels, and confidence overlays can be visually inspected.

## Implementation Decisions

- **Dependency Management**: Standardize the project under Python 3.12 managed via uv, declaring core computer vision dependencies including ultralytics, PyTorch, torchvision, supervision, and headless OpenCV.
- **Base Architecture**: Transfer learning starting from pretrained YOLO11 Nano (`yolo11n.pt`) with output restricted to single class `0: sneaker`.
- **Hardware Acceleration**: Automatic device resolution prioritizing Apple Silicon Metal (`mps`), with dynamic fallback to CUDA or CPU.
- **Training Strategy**: 50 maximum epochs with early stopping patience of 10 epochs, standard 640x640 input resolution, batch size of 16, and mosaic (1.0) plus scale (0.5) data augmentations.
- **Model Destination**: Export best-checkpoint weights to `models/yolo-sneaker.pt` upon successful completion of training.
- **Quality Gate Architecture**: Dedicated evaluation seam computing mAP50, Recall, Precision, and confusion statistics against the held-out test split, logging metrics in structured JSON format.
- **Inference Latency Benchmark**: Separate non-training timing module measuring pure model forward-pass latency over repeated iterations (warmup + 100 runs) reporting mean latency in milliseconds and FPS.

## Testing Decisions

- **Dependency Environment Seam**: Verification that all declared dependencies import correctly and can access PyTorch MPS/CPU acceleration.
- **Training Execution Seam**: Verification that the training routine runs to completion, honors early stopping, and generates weight artifacts.
- **Metric Quality Gate Seam**: Automated assertions verifying:
  - mAP50 >= 0.65
  - Recall >= 0.90
  - Precision >= 0.85
- **Model Export Seam**: Verification that the target model weight file exists, is non-empty, and can be instantiated as a valid YOLO detection model.
- **Inference Seam**: Verification that passing a test image through the exported model yields valid detection structures with bounding boxes and confidence scores >= 0.40.
- **Throughput Benchmark Seam**: Verification that inference latency on Apple Silicon satisfies real-time decoupled worker requirements (< 30ms per ROI crop).

## Out of Scope

- Live interactive webcam window and OpenCV GUI rendering (scheduled for the Core Video Pipeline feature).
- Multi-object pedestrian tracking and LineZone tripwire intersection calculations (handled in subsequent tracking tickets).
- Multi-class footwear classification (boots, sandals, high heels; strictly prohibited by ADR-0003).
- SQLite event persistence and file system evidence archiving (scheduled for the Storage feature).

## Further Notes

- The dataset contains 190 training, 56 validation, and 28 test images already partitioned and auto-labeled with class `0: sneaker`.
- Training on Apple Silicon M-series chips typically processes 50 epochs in under 3 minutes for this dataset size.
