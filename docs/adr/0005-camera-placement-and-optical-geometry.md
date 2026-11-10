# ADR-0005: Camera Placement and Optical Geometry Specification (MacBook Webcam)

**Date**: 2026-11-10
**Status**: accepted
**Deciders**: Pat (Developer), AI Assistant

## Context

The system utilizes a stationary **MacBook built-in webcam (1080p FaceTime HD camera)** as its primary sensor for both person tracking and footwear inspection. 

Unlike dedicated industrial CCTV mounts, a MacBook webcam introduces specific operational characteristics:
1. **Camera Location**: Placed stationary on a desk, table, or stand at standard waist height ($\approx 0.75 - 0.90 \text{ m}$).
2. **Field of View (FOV)**: Approximately $60^\circ - 70^\circ$ diagonal ($\approx 50^\circ$ horizontal, $\approx 30^\circ$ vertical).
3. **Lateral Perspective (Side View)**: Looking across the walkway corridor from the side, with people walking horizontally across the frame from Left to Right.

The physical optical geometry must guarantee that a full adult body ($\approx 1.60 - 1.85 \text{ m}$) is completely visible from head to toe (including both shoes on the floor) without head or foot cropping.

## Decision

We establish the **MacBook Stationary Lateral Side View (มุมกล้องมองด้านข้างทางเดิน)** as the primary optical baseline:

![Full-Body Side View Visualization](file:///Users/pat/Project/my-cv/docs/adr/assets/cv_full_body_detection_tripwire.jpg)

### 1. Physical Setup & Layout
- **Camera Device**: MacBook Built-in FaceTime HD Camera (1080p, 16:9 widescreen, $1920 \times 1080$).
- **Placement**: Stationary on a desk or table at height **$0.75 \text{ m} - 0.90 \text{ m}$**, screen tilted naturally at $\approx 100^\circ - 105^\circ$ to maintain a level horizontal optical axis.
- **Corridor Distance**: The pedestrian walkway centerline must be located **$2.8 \text{ m}$ to $3.5 \text{ m}$** perpendicular to the MacBook.
  - *Optical proof*: At distance $D = 3.0 \text{ m}$ and vertical FOV $\approx 32^\circ$, visible vertical frame span is $2 \cdot D \cdot \tan(16^\circ) \approx 1.72 \text{ m} + \text{tilt margins}$, comfortably fitting an upright human from head to toe.
- **Walking Direction (A → B)**: Pedestrians walk horizontally across the frame from **Left to Right** (Zone A on the left, Zone B on the right).

### 2. Virtual Tripwire (Vertical Line)
- **Line Orientation**: A vertical tripwire dividing the screen into left and right hemispheres:
  - $L_{start} = (960, 0)$
  - $L_{end} = (960, 1080)$
- **Directional Trigger (A → B Only)**:
  - **Zone A**: Left side of the frame ($x < 960$).
  - **Zone B**: Right side of the frame ($x > 960$).
  - Crossing event triggers only when person movement vector $(P_{t-1}, P_t)$ transitions from $x < 960$ to $x \ge 960$.
  - Walking Right to Left ($B \to A$) is a silent drop that resets the person's track cooldown.

### 3. Visual Detection HUD & Annotations
When viewing the real-time preview or logged evidence:
- **Person Bounding Box**: Solid green rectangle enclosing the full body, labeled `Person ID: 1 (conf: 0.95)`.
- **Sneaker Bounding Boxes**: Crisp cyan/blue bounding boxes tightly enclosing each detected sneaker on the floor, labeled `sneaker: 0.92` and `sneaker: 0.89`.
- **Tripwire Overlay**: Vertical neon line running down the corridor midpoint with directional arrow `A → B` pointing left-to-right.
- **Environment**: Clean indoor corridor/lab with balanced ambient lighting ($\ge 200 \text{ lux}$) to ensure sharp foot contrast against the floor.

## Alternatives Considered

### Alternative 1: High Ceiling External Mount (> 2.5m)
- **Pros**: Wider coverage area.
- **Cons**: Requires external IP/RTSP camera, ladder mounting, and additional cabling.
- **Why not**: The project requirement explicitly specifies the MacBook built-in webcam as the primary sensor.

### Alternative 2: Front-Facing Head-On View (Walking Directly Toward MacBook)
- **Pros**: Direct frontal view of faces.
- **Cons**: Frontal approach causes the torso/legs to occlude the trailing foot during walking; tripwire crossing is harder to calibrate from depth perspective than a clean lateral side-profile crossing.
- **Why not**: Lateral side view provides clean, unambiguous vertical line crossing and exposes both feet in mid-stride.

## Consequences

### Positive
- **Zero Additional Hardware**: Leverages the MacBook's native webcam without purchasing or mounting external CCTV cameras.
- **Clear Stride Separation**: Lateral side perspective clearly separates the leading foot and trailing foot during gait.
- **Trivial Tripwire Geometry**: A vertical line ($x = \text{const}$) simplifies line intersection math to a fast horizontal coordinate threshold check ($x_{prev} < X_{line} \le x_{curr}$).

### Negative
- **Fixed Walkway Distance**: The subject must walk along the $2.8 - 3.5 \text{ m}$ corridor line. Walking too close (< 2.0m) will crop the head or feet.

### Risks
- **Subject Shorter or Taller than Average**: Very tall individuals (> 1.95m) might clip their head if walking closer than 2.8m.
  - *Mitigation*: Slightly tilt the MacBook screen or set the corridor at 3.2m to ensure a 2.1m vertical clearance.
