# Spec: Architecture Governance — AGENTS.md & GLOSSARY.md Synthesis

## Problem Statement

The computer vision project contains 6 detailed Architecture Decision Records (`docs/adr/0001` through `0006`), but lacked concrete operational guidelines (`AGENTS.md`) and domain definitions/invariants (`GLOSSARY.md`). Without these, agents and developers risk violating core architectural constraints (such as blocking the 30 FPS video thread, using incorrect anchor coordinates, or attempting multi-class shoe recognition).

## Solution

Synthesize the 6 accepted ADRs into root operational documents:
1. `AGENTS.md`: Defines runtime stack (Python 3.12, Ultralytics YOLO11, Supervision, SQLite WAL), build/test commands, clean decoupled 10-line pattern vs anti-patterns, module boundaries, and never-touch boundary rules.
2. `GLOSSARY.md`: Establishes canonical domain terminology (Person Detector, Ground Anchor Point, ByteTrack, LineZone, Directional Crossing, Cooldown Window, Lower-Body ROI, Sneaker Detector, Evidence Images, Crossing Event, FrameSource), forbidden synonyms, and 6 non-negotiable system invariants.
3. Synchronize the system knowledge graph via `graphify update .`.

## User Stories

1. As an AI agent or developer, I want clear build, run, and test commands in `AGENTS.md`, so that I run commands consistently via `uv run`.
2. As a software engineer, I want explicit architecture boundaries and forbidden anti-patterns in `AGENTS.md`, so that I never introduce blocking I/O into the 30 FPS main capture loop.
3. As a domain modeler, I want canonical terms and forbidden synonyms in `GLOSSARY.md`, so that all code entities, schemas, and conversations share unified language.
4. As a quality engineer, I want non-negotiable system invariants documented in `GLOSSARY.md`, so that core requirements (bottom-center anchor formula, bounded queue maxsize=20, SQLite WAL mode) are strictly preserved across PRs.

## Implementation Decisions

- Synthesized directly from ADR-0001 to ADR-0006.
- Invariants codified in `GLOSSARY.md`.
- Concurrency and module rules codified in `AGENTS.md`.
- Knowledge graph refreshed using `graphify update .`.

## Testing Decisions

- Validation via `graphify update .` to ensure all markdown documentation symbols and relationships are cleanly indexed without extraction errors.

## Out of Scope

- Modifying the underlying ADR decisions.
- Writing production application code (reserved for subsequent feature tickets).
