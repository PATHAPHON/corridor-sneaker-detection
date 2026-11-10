# Project Agent Guidelines (AGENTS.md Template)

> [!IMPORTANT]
> **Status: Draft (Pending ADR Setup)**
> This is a baseline draft. Before production implementation, establish your Architecture Decision Record under `docs/adr/` and invoke the `setup-agent-and-glossary` skill to synthesize concrete stack details, commands, and rules.

This document is the Single Source of Truth (SSOT) for AI agents working in this repository.
AI agents must strictly follow these instructions, constraints, and workflows.

---

## 1. Project Stack
- **Language / Runtime**: [e.g. Python 3.11 / Node.js 22 / Rust 1.80]
- **Primary Framework / Core Libs**: [e.g. PyTorch 2.4, OpenCV / Next.js 16, Hono / FastAPI]
- **Data / Storage**: [e.g. SQLite, PostgreSQL, S3, HDF5]
- **Testing & Quality**: [e.g. pytest, cargo test, go test, npm test, linter]

---

## 2. Build, Run & Test Commands
- **Install Dependencies**: `[e.g. pip install -r requirements.txt | npm install]`
- **Run Application / Dev**: `[e.g. python -m src.main | npm run dev]`
- **Knowledge Graph (Mandatory)**: `graphify .` (build) | `graphify query "<target>"` (query) | `graphify update .` (sync)
- **Run Unit Tests**: `[e.g. pytest tests/unit | cargo test | go test ./...]`
- **Run Single Test**: `[e.g. pytest tests/unit/test_model.py -k "test_forward" | go test -run <Name>]`
- **Lint / Code Format**: `[e.g. ruff check . | npm run lint]`
- **Type Checking**: `[e.g. mypy src | npx tsc --noEmit]`

---

## 3. Code Style & Conventions
```[language]
// Good Example: Clean boundaries, explicit interfaces, no magic values
[Provide a 10-line ideal code pattern for this project]

// Bad Example: What is strictly forbidden
[Provide a bad code pattern showing what anti-pattern to avoid]
```

- **Naming**: `snake_case` for Python functions/files, `kebab-case` for TypeScript/React.
- **Interfaces**: Public APIs must declare explicit types / signatures; zero implicit `any` / dynamic untyped objects.

---

## 4. Architecture & Module Boundaries
- **Directory Layout**:
  - `src/` (or `app/`): Core implementation.
  - `tests/`: Automated unit and integration tests.
  - `.scratch/`: Dynamic feature specifications, tickets, and scratchpad.
  - `.agents/`: Project AI skills, hooks, and evolution logs.
  - `graphify-out/`: Mandatory knowledge graph, AST maps, and reports.
- **Encapsulation**: Cross-module imports must strictly go through package root public exports. Internal private submodules must not leak across domains.

---

## 5. Boundaries (Never-Touch Rules)
- **Zero Hardcoded Secrets / Paths**: Use environment variables or configuration files. Never commit API keys, absolute paths, or machine-dependent credentials.
- **Zero-Guessing Invariant (Search-First & Mandatory Graphify)**: Never guess file paths, function signatures, database columns, or tensor shapes. `graphify` must be installed and up-to-date. Always execute the Search-First sequence (`graphify query` / `graphify path` / `graphify explain` -> scoped grep -> targeted read) before writing code.
- **Zero Code Without Spec**: Never write production code without an approved specification and tickets generated via `to-spec` and `to-tickets` (for new features) or `to-edit` (for subsequent tweaks and fixes).
- **Test Coverage**: Always write or update tests for changed logic. Test suite must stay green before merge.

---

## 6. Standard Delivery Workflow
1. **Planning & Spec Phase**:
   - Trace dependencies using search-first hierarchy via mandatory `graphify` traversal.
   - Run `to-spec` to generate `.scratch/<feature-slug>/spec.md`.
   - Run `to-tickets` to generate `.scratch/<feature-slug>/issues/<NN>-<slug>.md`.
   - Present tickets to the user and wait for explicit approval before writing code.
2. **Implementation Phase**:
   - Implement production code ticket by ticket.
   - Clean, surgical edits only.
   - Synchronize knowledge graph via `graphify update .` after changes.
3. **Verification & Testing**:
   - Run test suite to verify no regressions.
4. **Follow-up Changes (Edits)**:
   - When the user asks for tweaks ("ไม่ถูกใจ", "แก้ตรงนี้หน่อย"), run `to-edit` to log feedback and create an edit ticket under `.scratch/<feature-slug>/edits/<NN>-<slug>.md`.
