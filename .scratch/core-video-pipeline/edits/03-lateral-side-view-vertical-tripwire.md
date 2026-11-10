# Edit 03: Realign Tripwire to Lateral Side-View Vertical Geometry per ADR-0005

**Status:** done

## Rationale & Impact
The user attached screenshots from their webcam testing and a reference diagram showing a side-profile camera viewing a pedestrian walking horizontally past the camera (Lateral Side View).
In the previous implementation, `PipelineConfig` defaulted to a horizontal line across the middle of the frame: `(0, 360) -> (1280, 360)`. In the webcam feed, this line passed through the user's forehead/upper body rather than crossing the walking path at the feet level, causing strong dissatisfaction ("ไม่ถูกใจ").
Per ADR-0005 (Camera Placement and Optical Geometry Specification), the setup is explicitly designed as a stationary lateral side view where:
1. The camera observes a corridor from the side.
2. Pedestrians walk horizontally from Left to Right across the frame ($A \to B$).
3. The virtual tripwire must be a vertical dividing line at the corridor midpoint:
   $L_{start} = (w/2, 0)$ to $L_{end} = (w/2, h)$, specifically $(960, 0) \to (960, 1080)$ on 1080p.
4. The ground anchor point $P_{anchor} = ((x_{min} + x_{max})/2, y_{max})$ at the floor contact plane crosses from Zone A ($x < 960$) to Zone B ($x \ge 960$).

## Target Files
- `src/config/settings.py`
- `src/pipeline/hud.py`
- `src/pipeline/coordinator.py`
- `tests/integration/test_pipeline.py`
- `tests/unit/test_tripwire.py`

## Planned Changes
- Update default tripwire coordinates in `PipelineConfig` to a vertical line: `(960, 0) -> (960, 1080)` (matching ADR-0005 Section 2).
- Dynamically calibrate/scale tripwire endpoints to the active frame source resolution if width/height differ (e.g. $w/2$ from top to bottom).
- Enhance HUD visual rendering:
  - Draw vertical neon tripwire line running down the frame.
  - Draw a prominent directional arrow pointing Left to Right ($A \to B$).
  - Render floor-plane indicator / anchor crossing crosshair clearly at the bottom.
- Ensure all tests pass with the vertical lateral geometry.

## Acceptance Criteria
- [x] Tripwire default coordinates represent a vertical line ($x=960$ on 1080p, or $x = w/2$) dividing left (Zone A) and right (Zone B).
- [x] Crossing triggers when moving from Left to Right ($A \to B$) at the ground anchor level.
- [x] HUD displays the vertical line with directional arrow $A \to B$ pointing rightwards.
- [x] All unit and integration tests pass cleanly.
