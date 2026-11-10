# 04: Lower-Body ROI Extraction and Sneaker Footwear Inspection

**What to build:** An event-triggered footwear inspection module that extracts a lower-body region of interest (bottom 30% of height with 10% horizontal padding) from the triggering pedestrian's bounding box and runs inference using the fine-tuned single-class sneaker YOLO11n detector to identify sneakers, bounding boxes, and detection confidence.

**Blocked by:** 03: Virtual Line Tripwire and Anti-Bounce Debounce Engine

**Status:** done

- [x] Lower-body ROI extractor crops the bottom 30% vertical region of the bounding box with 10% horizontal margin clamped to frame boundaries
- [x] Sneaker inspector loads the fine-tuned single-class sneaker YOLO11n weights with automatic hardware acceleration (MPS/CUDA/CPU)
- [x] Footwear inference detects sneakers above the required confidence threshold (default 0.40) and returns count, bounding boxes, and scores
- [x] Detection result accurately flags whether compliance was satisfied (shoes detected = True when at least one sneaker meets threshold)
- [x] Unit tests verify ROI bounding box calculations, margin clamping on boundary edges, and mock sneaker inference outputs
