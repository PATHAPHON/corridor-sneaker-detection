# GLOSSARY.md — Domain Terminology & System Invariants

## 1. Domain Terminology

| Canonical Term | Definition | Context / Scope | Forbidden Synonyms (Do Not Use) |
| :--- | :--- | :--- | :--- |
| **Person Detector** | Pretrained YOLO11 Nano model (`yolo11n.pt`) filtered strictly to COCO Class 0 (`person`), bounding pedestrians in real-time. | `src/tracking` | Human Detector, Pedestrian Classifier, Body Segmenter |
| **Ground Anchor Point** | The bottom-center point of a person bounding box: $P_{anchor} = \left(\frac{x_{min} + x_{max}}{2}, y_{max}\right)$, representing the floor contact plane. | `src/tracking`, `src/tripwire` | Footpoint, Base Point, Centerpoint, Feet Coordinate |
| **Multi-Object Tracker** | `supervision.ByteTrack` tracker maintaining persistent tracking IDs (`track_id`) across consecutive video frames during movement and occlusion. | `src/tracking` | SORT, DeepSORT, Object Re-identifier |
| **Tripwire / Virtual Line** | A directed 2D line segment between two user-defined coordinates $A(x_1, y_1) \to B(x_2, y_2)$ spanning the entrance corridor on the floor plane. | `src/tripwire` | Boundary Line, Laser Gate, Crossing Zone, Border Line |
| **LineZone** | `supervision.LineZone` geometric module calculating whether a track anchor transitioned across the virtual line using 2D vector cross products. | `src/tripwire` | Collision Box, Crossing Sensor, Trigger Area |
| **Directional Crossing** | The directed transit of a person: $A \to B$ represents **Entry** (triggers footwear inspection); $B \to A$ represents **Exit** (ignored/logged without inspection). | `src/tripwire`, `src/pipeline` | Step-over, Line Infiltration, Direction Inversion |
| **Cooldown Window** | A temporal debounce window (default: 2.0 seconds) per `track_id` that prevents duplicate trigger events if an individual hovers or steps back and forth over the line. | `src/tripwire` | Debounce Delay, Sleep Time, Lockout Period |
| **Lower-Body ROI** | Spatial crop of the person bounding box covering the bottom 30% of height with a 10% horizontal padding margin, framing feet and ankles. | `src/footwear` | Shoe Crop, Leg Cutout, Feet Snippet, Ankle Box |
| **Sneaker Detector** | Fine-tuned YOLO11 Nano model (`models/yolo-sneaker.pt`) detecting single class `0: sneaker` with confidence threshold $\ge 0.40$. | `src/footwear` | Footwear Classifier, Shoe Recognizer, Multi-class Shoe Model |
| **Evidence Images** | The visual JPEG files persisted on crossing: full context frame (`{timestamp}_{track_id}_full.jpg`) and annotated feet crop (`{timestamp}_{track_id}_crop.jpg`). | `src/storage` | Screenshots, Audit Photos, Snaps, Evidence Dumps |
| **Crossing Event** | An immutable data record persisted to SQLite `crossing_events` table documenting timestamp, track ID, direction, shoe status, confidence, and paths. | `src/storage` | Audit Log, Trigger Record, Crossing Row |
| **FrameSource** | High-level abstraction for video input (`CameraFrameSource`, `VideoFileFrameSource`, `SyntheticFrameSource`) decoupled from OpenCV implementations. | `src/capture` | Video Reader, Camera Grabber, Frame Streamer |

---

## 2. System Invariants & Non-Negotiable Rules

### Invariant 1: 30+ FPS Real-Time Capture Guarantee
- The primary video capture and tracking thread MUST NOT execute blocking operations, file I/O, network requests, or secondary model inferences.
- Heavy inspection tasks MUST be dispatched asynchronously to the background event worker thread via an in-memory queue.

### Invariant 2: Bounded Event Queue (Max Capacity = 20)
- The inter-thread event queue MUST be instantiated with `maxsize=20`.
- In the event of extreme congestion or burst entries, older or dropped events must be logged with warning; the main thread must NEVER block waiting for queue space.

### Invariant 3: Single-Class Inspection Scope
- Footwear inspection is strictly restricted to **Sneakers (`0: sneaker`)**.
- No attempts shall be made to classify heels, flip-flops, or dress shoes. If sneakers are not detected with confidence $\ge 0.40$, the system records `shoes_detected = FALSE`.

### Invariant 4: Floor-Plane Anchor Formulation
- The ground-contact representative coordinate for all tripwire intersection mathematics MUST strictly use bottom-center:
  $$P_{anchor} = \left(\frac{x_{min} + x_{max}}{2}, y_{max}\right)$$
  Bounding box centroids $(x_c, y_c)$ or keypoints outside bottom-center are strictly prohibited for tripwire calculations.

### Invariant 5: SQLite WAL Mode Persistence
- SQLite database connections MUST execute `PRAGMA journal_mode=WAL;` and `PRAGMA synchronous=NORMAL;` upon opening to enable concurrent non-blocking reads and background writes without locking errors.

### Invariant 6: Zero Secrets in Source Code
- All credentials, API keys (e.g. `ROBOFLOW_API_KEY`), and external tokens MUST be loaded from environment variables or `.env`. No credential strings may ever be committed to git.

### Invariant 7: Training-Time Augmentation over Runtime Preprocessing
- Do not introduce image processing filters (such as CLAHE or unsharp masking) into the live capture or footwear inspection path. All invariance to indoor lighting, dark footwear, and walking motion blur must be achieved through training-time data augmentations (ADR-0007).

