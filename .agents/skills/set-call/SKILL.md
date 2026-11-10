---
name: set-call
description: Universal Tool-Call & Command Error Correction Playbook (Synthesized from Agent Evolution Traces & Distillations). Prevents trial-and-error guessing across SQL/DB schemas, file paths, shell quoting, test runners, Python unittests, and background task management.
---

# Set-Call: Universal Tool-Call & Command Error Correction Playbook

Synthesized from `.agents/.agent-evolution/data/distill` and `.agents/.agent-evolution/data/traces` to eliminate trial-and-error tool calls across `run_command`, `read_file`, `write_file`, and `manage_task`.

---

## 1. Database Schema & Query Execution (Zero Schema Guessing)

Agents repeatedly fail with `OperationalError: no such table / column` or syntax errors when guessing table and column names.

- ❌ **Wrong (Forbidden Guesses)**:
  - Blindly executing `SELECT` or `UPDATE` queries with assumed column names without checking schema definitions.
  - Guessing schema structures in inline SQL scripts.
- ✅ **Correct (Canonical Schema Verification)**:
  - Always check schema files (`schema.ts`, `schema.sql`, or migration files) first via `read_file`.
  - **SQLite Pre-Query Inspection**: If querying a local SQLite `.db` file directly, inspect existing tables first:
    ```bash
    sqlite3 <database-file> "SELECT name, sql FROM sqlite_master WHERE type='table';"
    ```
  - Always bound query reads with `LIMIT` when testing.

---

## 2. File Reading, Creation & Directory Paths (Zero Path Guessing)

- ❌ **Wrong**:
  - Calling `read_file` or `edit_file` on guessed file paths that do not exist (`file does not exist` error).
  - Writing files via shell redirection (`cat << 'EOF' > path/to/file`) when parent directories do not exist (`zsh: no such file or directory`).
  - Listing multiple optional paths with `ls` without error suppression (`ls path1 path2` exits code 1 if one path is absent).
- ✅ **Correct**:
  - Always resolve file existence first using `graphify query` or targeted `rg --files <directory>`.
  - Use the native `write_file` tool (which creates parent directories automatically), or prefix shell commands with `mkdir -p <dir> &&`.
  - Append `|| true` when probing optional directories with shell tools: `ls -la optional_dir 2>/dev/null || true`.

---

## 3. Git Commands & Diff Safety

- ❌ **Wrong**:
  - Running `git diff /external/path` across repository boundaries (`fatal: ... is outside repository`, Exit Code `128`).
  - Running raw `diff -u fileA fileB` directly, which returns exit code `1` when differences exist and fails the tool call.
- ✅ **Correct**:
  - Target external or submodule directories explicitly using `-C`: `git -C <target-dir> diff ...`.
  - When comparing files with `diff -u`, append `|| true` to prevent non-zero exit codes: `diff -u fileA fileB || true`.

---

## 4. Shell Quoting & Inline Python Scripts

- ❌ **Wrong**:
  - Nesting double and single quotes inside `python3 -c "..."` in zsh (causes `SyntaxError: unexpected character after line continuation character`).
  - Relying on brittle backslash escapes in complex command-line arguments.
- ✅ **Correct**:
  - Use single-quoted Heredoc (`<< 'EOF'`) for multi-line or quote-heavy inline scripts:
    ```bash
    python3 - << 'EOF'
    import json, os, sys
    # Write standard Python safely without escaping quotes
    EOF
    ```

---

## 5. Python Unittest Execution

- ❌ **Wrong**:
  - Running `python3 -m unittest path/to/test_file.py` with leading dots (e.g. `.agents/...`), which Python treats as an invalid dotted module name.
- ✅ **Correct**:
  - Run the test file directly as a script: `python3 path/to/test_file.py -v`.
  - Or use standard test runner discovery: `python3 -m unittest discover -s <test-dir> -p "test_*.py" -v` or `pytest <test-dir>`.

---

## 6. Test Runners & Typecheck CLI Calls

- ❌ **Wrong**:
  - Running test runners with project-specific flags that are not configured in the active repository.
  - Modifying function/component signatures without simultaneously updating call sites in test files, resulting in type errors during `tsc` or `mypy`.
- ✅ **Correct**:
  - Consult the project's [AGENTS.md](file:///Users/pat/Project/skillflow/AGENTS.md) for the exact test commands.
  - Before running typecheckers (`tsc`, `mypy`, `ruff`), run a scoped search (`rg -n "<SymbolName>"`) to update both production code and test callers in the same turn.

---

## 7. Background Tasks & Subagent Management (`manage_task` & `invoke_subagent`)

- ❌ **Wrong**:
  - Calling `manage_task` with `Action: "kill"` on a task that has already finished (`cannot kill task: task is not running (status: DONE)`).
  - Polling tasks or subagents in a tight loop with multiple `manage_task` or `schedule` calls.
- ✅ **Correct**:
  - Always check task state via `manage_task(Action: "list")` or `"status"` before attempting `kill`.
  - For long-running synchronous commands, increase `WaitMsBeforeAsync` (e.g. 10000).
  - For asynchronous tasks or subagents, stop calling tools and end your turn—the runtime automatically wakes the agent upon task completion.

---

## 8. Spec Enforcement & Hook Gating (Zero Probing & Immediate Halt)

- ❌ **Wrong**:
  - Executing inspection scripts, python one-liners, or git diffs to probe or reverse-engineer hook enforcement logic when blocked by `PreToolUse`.
  - Attempting to bypass spec boundaries or asking the user for permission to bypass security hooks.
- ✅ **Correct**:
  - **Zero Probing Invariant**: If a tool is denied by `PreToolUse` because no approved spec/ticket exists in `.scratch/`, stop immediately.
  - Do not call tools in loops. In 1 concise sentence, inform the user that production code modification requires an approved feature spec via `to-spec` / `to-tickets` or an edit ticket via `to-edit`.

---

## 9. Project-Specific Distilled Rules (Generated via `setup-core`)

*(This section is updated dynamically by `setup-core` when new trial-and-error patterns are distilled from `.agent-evolution/data/traces/`)*
