# 05: Two-Stage Decoupled Pipeline and Concurrency Coordinator

**What to build:** An asynchronous two-stage pipeline coordinator that runs real-time video capture, person detection, tracking, and tripwire evaluation on a lightweight 30+ FPS main thread, dispatches crossing events non-blockingly into a bounded queue (maxsize=20), processes sneaker inspection in a background worker thread, and supports graceful shutdown.

**Blocked by:** 04: Lower-Body ROI Extraction and Sneaker Footwear Inspection

**Status:** done

- [x] Pipeline coordinator initiates the dedicated video capture and tracking loop maintaining 30+ FPS throughput
- [x] Inter-stage bounded queue is instantiated with a maximum capacity of 20 items to prevent memory bloat
- [x] Crossing events are enqueued non-blockingly; if queue is saturated, events drop with warning log without stalling capture loop
- [x] Background worker thread consumes crossing events, executes lower-body ROI extraction and sneaker detection, and prepares inspection records
- [x] Clean shutdown signal stops the capture stream, waits for worker queue draining, and safely releases resources
- [x] Integration tests verify end-to-end processing from synthetic frames through tracking, crossing, and worker inspection
