---
name: setup-core
description: Core Tool Execution Optimizer & Trace Distiller. Establishes project core tool invocation standards (run_command, read_file, write_file, graphify) and distills execution traces from .agent-evolution into project-specific error correction rules in set-call.
---

# Setup-Core: Tool Invocation Standards & Evolution Distiller

`setup-core` optimizes how AI agents interact with core workspace tools and extracts lessons from real tool errors to prevent repetitive mistakes across turns.

---

## 1. Core Tool Invocation Standards

AI agents must adhere to these foundational execution patterns:

### A. Command Execution (`run_command`)
- **Deterministic & Non-Interactive**: Never launch interactive commands (e.g. commands waiting for terminal input like `nano`, `vi`, or unflagged `npm init`). Always pass non-interactive flags (`-y`, `--batch`, `-q`).
- **Quote-Safe Scripts**: When running multi-line Python or Node scripts via CLI, avoid nested quotes inside `-c`. Always use single-quoted Heredocs:
  ```bash
  python3 - << 'EOF'
  import sys
  print("Safe execution")
  EOF
  ```
- **Probe Safety**: When checking optional directories, files, or non-critical tools, append `|| true` to prevent non-zero exit codes from aborting multi-command runs.

### B. Knowledge Graph Traversal (`graphify`)
- **Search-First Sequence**:
  1. `graphify query "<target>"`: Scope subgraphs and caller/callee relationships before touching code.
  2. `graphify path "<Caller>" "<Callee>"`: Trace exact call paths.
  3. `graphify explain "<Symbol>"`: Inspect blast radius.
- **Sync Invariant**: Always run `graphify update .` after adding, modifying, or deleting code files in `src/`.

### C. File Operations (`read_file`, `write_file`, `edit_file`)
- **Zero-Guessing Invariant**: Never guess file names or directory locations. Confirm existence via `graphify query` or `rg --files` before calling `read_file`.
- **Surgical Edits**: When using `edit_file`, match exact indentation and context lines. Verify that changes do not introduce orphan imports or unused variables.

---

## 2. Trace Harvesting & Distillation Workflow

Every project initialized with SkillFlow records execution telemetry in `.agents/.agent-evolution/data/traces/`. When an agent experiences tool failures, trial-and-error retries, or command errors, `setup-core` distills these traces into permanent project rules.

### Step-by-Step Distillation Process:

1. **Sync Latest Session Traces**:
   ```bash
   python3 .agents/.agent-evolution/bin/sync-traces.py
   ```
2. **Run Error & Pattern Distillation**:
   ```bash
   python3 .agents/.agent-evolution/bin/distill.py
   ```
   This script parses recent trace files, aggregates exit codes != 0, identifies repeated tool calls on the same target, and generates summary insights under `.agents/.agent-evolution/data/distill/`.

3. **Update `set-call/SKILL.md`**:
   - Inspect the distillation output under `.agents/.agent-evolution/data/distill/`.
   - Identify concrete anti-patterns (e.g., incorrect CLI flags for this project's test runner, mistyped DB columns, or wrong import aliases).
   - Format each finding into an explicit **❌ Wrong** vs **✅ Correct** entry.
   - Append or update the finding under **Section 9 (Project-Specific Distilled Rules)** in `.agents/skills/set-call/SKILL.md`.

---

## 3. When to Run `setup-core`

1. **Initial Project Setup**: Run once to ensure all core tool configurations, Python virtual environments, and graphify markers are properly wired.
2. **After Bug Fixes / Debugging**: When an agent spent more than 2 turns troubleshooting a tool failure or command error, run the distillation workflow to record the fix permanently.
3. **Periodic Maintenance**: Run periodically to clean up stale trace files and maintain a lean error correction playbook.
