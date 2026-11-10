---
name: setup-agent-and-glossary
description: Architecture-to-Guideline Synthesizer. Reads Architecture Decision Records (ADRs) from docs/adr/ and synthesizes them into concrete AGENTS.md and GLOSSARY.md rules. If ADRs do not exist, guides the user through ADR creation first.
---

# Setup Agent & Glossary: Architecture-to-Guideline Synthesizer

In a generic baseline setup, project requirements, architectural patterns, and domain terminology are unknown until Architecture Decision Records (ADRs) are established. This skill bridges the gap between high-level architectural decisions in `docs/adr/` and the concrete operational rules in `AGENTS.md` and `GLOSSARY.md`.

---

## 1. Process Flow

```text
Check docs/adr/ ──► [Missing ADR] ──► Guide/Draft docs/adr/0001-architecture-baseline.md
       │
  [ADR Exists]
       ▼
Extract Tech Stack, Boundaries, Commands & Domain Terms
       │
       ├──────────────────────────────┐
       ▼                              ▼
Write AGENTS.md               Write GLOSSARY.md
(Stack, Build/Test, Rules)    (Entities, Invariants)
       │                              │
       └──────────────┬───────────────┘
                      ▼
            graphify update .
```

---

## 2. Step-by-Step Procedure

### Step 1: Scan for ADRs in `docs/adr/`
Check for existing ADR files:
- Inspect files matching `docs/adr/*.md`.
- If no ADR exists, or if only an empty skeleton is present, proceed to **Step 2A**.
- If one or more approved ADRs exist, proceed directly to **Step 2B**.

### Step 2A: Guide ADR Creation (If No ADR Exists)
Guide the user to draft `docs/adr/0001-architecture-baseline.md`. Use the standard MADR structure:
```markdown
# 0001: Architecture Baseline & Technology Stack

- **Status**: Accepted
- **Date**: YYYY-MM-DD
- **Decision Makers**: [User / Team]

## Context & Problem Statement
What system or application is this project building, and what core constraints exist?

## Decision Drivers
- Performance, latency, or hardware budget
- Developer ergonomics and ecosystem compatibility
- Security and compliance boundaries

## Considered Options
- Option 1 (Chosen)
- Option 2

## Decision Outcome
- **Language / Runtime**: [e.g. Python 3.12, TypeScript 5, Go 1.23]
- **Primary Framework**: [e.g. FastAPI, Next.js 16, PyTorch 2.4]
- **Data & Storage**: [e.g. PostgreSQL, SQLite, Qdrant, S3]
- **Testing & Quality Tooling**: [e.g. pytest, cargo test, go test, npm test, linter]
- **Architecture Pattern**: [e.g. Layered Clean Architecture, Medallion, Feature-sliced]

## Consequences
- Positive impact
- Tradeoffs / Constraints
```
Ask the user clarifying questions if any decision is ambiguous before writing the ADR.

---

### Step 2B: Synthesize ADR into `AGENTS.md` and `GLOSSARY.md`

#### 1. Generate `AGENTS.md`
Read the ADR(s) and populate the project root [AGENTS.md](file:///Users/pat/Project/skillflow/AGENTS.md):
- **1. Project Stack**: Language, framework, database, and test tools specified in the ADR.
- **2. Build, Run & Test Commands**: Exact terminal commands for dependencies, local dev, testing, linting, and mandatory `graphify` (`graphify .`, `graphify query`, `graphify update .`).
- **3. Code Style & Conventions**: Clean 10-line ideal pattern vs forbidden anti-patterns based on chosen framework.
- **4. Architecture & Module Boundaries**: Directory structure (`src/`, `tests/`, etc.) and encapsulation rules.
- **5. Boundaries (Never-Touch Rules)**:
  - Zero hardcoded secrets/paths.
  - Mandatory Graphify Invariant (Zero-Guessing).
  - Zero code without approved spec in `.scratch/`.
- **6. Standard Delivery Workflow**: Spec -> Tickets -> Approval -> Implementation -> Unit/E2E testing -> Edit.

#### 2. Generate `GLOSSARY.md`
Extract core domain concepts, entities, and invariants from the ADR into the project root [GLOSSARY.md](file:///Users/pat/Project/skillflow/GLOSSARY.md):
- **1. Domain Terminology**: Primary entities, processes, and forbidden synonyms.
- **2. System Invariants & Non-Negotiable Rules**:
  - Data Grounding (source of truth).
  - Idempotency & determinism.
  - Resource safety and bounding constraints.

---

### Step 3: Synchronize Knowledge Graph
After writing `AGENTS.md` and `GLOSSARY.md`, immediately update the project's knowledge graph:
```bash
graphify update .
```

---

## 3. When to Invoke `setup-agent-and-glossary`

1. **Initial Project Onboarding**: Immediately after project bootstrap, once the team/developer is ready to define architectural decisions.
2. **Major Architectural Changes**: When a new ADR is adopted (e.g. switching ORM, adding a vector database, or restructuring directory layout), re-run this skill to keep `AGENTS.md` and `GLOSSARY.md` in sync with the new decisions.
