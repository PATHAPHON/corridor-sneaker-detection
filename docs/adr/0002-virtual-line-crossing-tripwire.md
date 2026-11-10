# ADR-0002: Virtual Line Crossing and Tripwire Mechanism

**Date**: 2026-11-10
**Status**: accepted
**Deciders**: Pat (Developer), AI Assistant

## Context

Once pedestrians are tracked across video frames, the system needs an accurate, reproducible mechanism to determine the exact moment an individual crosses a predefined line (tripwire) on the floor.

Core challenges:
- Discriminating direction of travel: Shoe inspection is required **strictly when individuals enter (Direction A → B)**, while pedestrians exiting (Direction B → A) must be ignored to save storage and computational resources.
- Handling discrete frame sampling where a fast-moving person jumps from one side of the line to the other between frame $t-1$ and frame $t$.
- Preventing duplicate triggers when someone stops or lingers near the boundary line, while allowing a person who exits and re-enters later to trigger again.

## Decision

We will implement a **Unidirectional (A → B Only) Virtual Tripwire using `supervision.LineZone`**:

1. **Line Definition & Spatial Orientation (Zone A vs Zone B)**:
   - The virtual line is defined by two Cartesian endpoints $L_{start}(x_1, y_1)$ and $L_{end}(x_2, y_2)$ configured in `config.yaml`.
   - The directed vector $\vec{V} = (x_2 - x_1, y_2 - y_1)$ mathematically bisects the plane:
     - **Zone A**: Left-hand side relative to the directed vector $\vec{V}$ (cross-product $> 0$).
     - **Zone B**: Right-hand side relative to the directed vector $\vec{V}$ (cross-product $< 0$).
   - The debug/preview screen displays a directional arrow pointing across the line indicating the active $A \to B$ crossing vector.

2. **Directional Event Triggering (A → B Only)**:
   - For each active `track_id`, the system monitors the movement vector formed by anchor point $P_{t-1}$ and $P_t$.
   - **Crossing A → B**: Verified when trajectory intersects $(L_1, L_2)$ and transitions from Zone A to Zone B. This triggers the downstream Stage 2 Footwear Detection and Event Logging.
   - **Crossing B → A (Reverse / Exit)**: **Silent Drop**. Does not run shoe detection, does not save images, and does not record to database. Crucially, reverse crossing B → A acts as an immediate **cooldown reset** for that `track_id`, allowing the same person to be re-evaluated if they re-enter from A to B later.

3. **Anti-Bounce & Deduplication**:
   - Maintain a cooldown map of processed `track_id`s. Once a `track_id` triggers an A → B crossing, further A → B triggers for that ID are suppressed for 3.0 seconds (configurable) unless a B → A exit reset occurs.

## Alternatives Considered

### Alternative 1: Bidirectional Processing (Evaluating both A → B and B → A)
- **Pros**: Collects data on both arrivals and departures.
- **Cons**: Doubles image storage requirements and executes needless shoe model inferences on exiting individuals who were already inspected on entry.
- **Why not**: Business requirement strictly mandates shoe inspection upon arrival (A → B); silent drop saves 50% compute and storage.

### Alternative 2: Custom Vector Mathematics (No External CV Library)
- **Pros**: Zero third-party library dependency for geometry.
- **Cons**: Requires custom maintenance of edge cases (collinear points, boundary clipping, direction tracking).
- **Why not**: `supervision.LineZone` is already battle-tested, actively maintained, and integrates seamlessly with ByteTrack.

### Alternative 3: Dual Virtual Lines / Polygon ROI Zone
- **Pros**: Physical buffer zone between Line A and Line B provides high resistance against hovering.
- **Cons**: Requires more complex spatial calibration from the camera perspective.
- **Why not**: Single line with trajectory vector intersection and ID cooldown delivers sufficient stability with simpler camera setup.

## Consequences

### Positive
- **50% Resource Savings**: Completely eliminates redundant shoe model inference and image writes for exiting pedestrians.
- **Smart Re-Entry Support**: Exiting (B → A) automatically clears the track ID cooldown, allowing re-entry triggers without waiting for timer expiry.
- **Clear Visual Orientation**: Directed vector convention ($L_{start} \to L_{end}$) provides predictable Zone A / Zone B orientation with visual arrow overlay.

### Negative
- **Setup Sensitivity**: Operator must set `start` and `end` coordinates in the correct order to ensure the arrow points in the desired A → B direction.

### Risks
- **Hovering on Line Boundary**: A person standing directly on the line could generate noisy oscillating vectors.
  - *Mitigation*: The 3-second cooldown gate prevents repeated triggers while lingering.

