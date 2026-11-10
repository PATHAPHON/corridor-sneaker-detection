# Spec: Sneaker Dataset Ingestion & Auto-Box Annotation Pipeline

## Problem Statement

To train a dedicated YOLO11 Nano sneaker detection model (`models/yolo-sneaker.pt`) for the retail/entry tripwire monitoring system (ADR-0003), we need bounding box annotations around footwear. The raw dataset downloaded from Kaggle (`noobyogi0100/shoe-dataset`) currently contains 299 unannotated sneaker images located at `/Users/pat/Downloads/shoeTypeClassifierDataset/` with an inverted split (50 training images and 249 validation images). Manually drawing bounding boxes across 299 images is time-consuming and labor-intensive. We need an automated, reproducible ingestion and cloud auto-labeling pipeline using Roboflow.

## Solution

We build an automated Python ingestion script using the Roboflow SDK to:
1. Authenticate with the user's Roboflow workspace (`patapol-eing-gmail-com`).
2. Create or connect to an object detection project named `sneaker-detection`.
3. Normalize the inverted train/validation split by distributing all 299 images according to the standard 70% Train, 20% Valid, 10% Test ratio.
4. Execute an initial single-image verification test before streaming the full batch of 298 images.
5. Prepare the project on Roboflow for few-shot foundation model Auto-Labeling (`sneaker`), followed by YOLOv11 dataset export back to `datasets/sneakers/`.

## User Stories

1. As a computer vision developer, I want to authenticate against Roboflow using credentials stored in `.env`, so that API keys remain protected and outside version control.
2. As a computer vision developer, I want to verify existing workspace projects, so that I avoid duplicate project creation or overwriting existing datasets.
3. As a computer vision developer, I want to create an object detection project named `sneaker-detection` on Roboflow if it does not already exist, so that images are properly routed.
4. As a machine learning engineer, I want to rebalance the 50/249 inverted image split into a standard 70/20/10 ratio, so that the subsequent YOLO fine-tuning has adequate training diversity (~210 training images).
5. As an operator, I want a dry-run test upload of 1 image first, so that network connectivity, authentication, and project parameters are validated before bulk upload.
6. As an operator, I want automated progress and error-handling during bulk upload of all remaining 298 images, so that failed network calls can be retried without restarting from scratch.
7. As an annotator, I want all 299 images uploaded with a batch tag (`kaggle-sneakers`), so that I can filter, inspect, and run Roboflow Auto-Label with prompt `sneaker` effortlessly.
8. As a developer, I want clear post-upload instructions to export the annotated dataset in YOLOv11 format to `datasets/sneakers/`, so that the project can proceed to model fine-tuning (ADR-0003).

## Implementation Decisions

- **SDK and Runtime**: Python 3.12 managed via `uv run --with roboflow`, reading `.env` directly with standard parsing to avoid third-party env overhead.
- **Project Configuration**: Single object detection project `sneaker-detection` under workspace `patapol-eing-gmail-com` with annotation label `sneaker`.
- **Split Distribution**:
  - Pool all 299 images from `training/sneakers` (50) and `validation/sneakers` (249).
  - Deterministically assign splits using modular hashing or indexed assignment: 70% `train` (210 images), 20% `valid` (60 images), 10% `test` (29 images).
- **Execution Phasing**:
  - Phase 1: Upload first sample image and log confirmation URL.
  - Phase 2: Upload remaining 298 images with batch identifier `kaggle-sneakers`.
- **Export Target**: Exported YOLOv11 dataset lands at `datasets/sneakers/` containing `data.yaml`, `train/images/`, `train/labels/`, `valid/images/`, `valid/labels/`.

## Testing Decisions

- **Pre-flight Integrity Check**: High-level seam verifying that all 299 image files exist, are readable JPEG/PNG format, and have non-zero file sizes prior to triggering any network call.
- **Authentication & Workspace Seam**: Seam verifying that `ROBOFLOW_API_KEY` and `ROBOFLOW_WORKSPACE` correctly load from `.env` and authenticate against Roboflow API.
- **Single-Image Test Seam**: Verifying that 1 image successfully receives an HTTP 200/success response from the Roboflow upload endpoint before dispatching batch requests.
- **Bulk Progress Verification**: Tracking upload success count, checking that `success_count == 299` and `failed_count == 0`.

## Out of Scope

- Running local model training (handled in subsequent ticket/ADR-0003).
- Manual bounding box drawing in local image editing software.
- Full video pipeline integration (handled in subsequent tickets).

## Further Notes

- The Roboflow free tier quota provides sufficient image allowance for this 299-image batch.
- Auto-labeling will be executed via Roboflow's web interface using their foundation model (Grounding DINO / OWL-ViT) by specifying class name `sneaker`.
