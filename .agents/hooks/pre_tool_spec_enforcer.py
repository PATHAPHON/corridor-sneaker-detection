#!/usr/bin/env python3
"""
pre_tool_spec_enforcer.py — Antigravity PreToolUse Hook
Enforces the 'Zero Code Without Spec' and 'TrueEdit' lifecycle policy:
- Production Change Scope:
    Every new production feature/change task MUST start fresh in its own feature folder under .scratch/<feature-slug>/.
    Historical features from previous sessions are permanently CLOSED and IMMUTABLE.
    They cannot be re-used, modified, or extended with edit tickets across sessions.
- Round 1 (Initial Feature Lifecycle in Current Session):
    Main agent and user discuss initial feature. Requires:
      1. .scratch/<feature-slug>/spec.md (via to-spec, fresh in active session)
      2. .scratch/<feature-slug>/issues/*.md (at least one tracer ticket via to-tickets)
      3. User Approval Gate: user must approve in a subsequent turn before implementation.
    Round 1 is strictly for feature inception. Once initial build is approved/done,
    spec.md and issues/*.md become FROZEN and IMMUTABLE.
- Round 2+ (Subsequent Edits within Current Session via to-edit):
    All subsequent changes, user feedback ("ไม่ถูกใจ"), bug fixes, or tweaks within this session
    MUST be recorded as dedicated edit tickets in .scratch/<feature-slug>/edits/<NN>-<slug>.md.
    Strict Pre-requisite: The feature MUST belong to the current session and have completed to-spec and to-tickets.
    Feedback Analysis: The edit ticket must analyze user feedback (why the edit is requested / what was disliked).
    Never accepts Antigravity brain artifacts (.gemini/antigravity/brain/) as a substitute for .scratch/.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# File paths/patterns considered protected production code
PROTECTED_PREFIXES = ("src/", "app/", "lib/", "models/", "pipelines/", "data/", "e2e/", "scripts/")
PROTECTED_FILES = ("GLOSSARY.md", "AGENTS.md", "package.json", "pyproject.toml", "requirements.txt")
PROTECTED_EXTENSIONS = (
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".mjs",
    ".sql",
    ".css",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".cu",
    ".rs",
    ".go",
)

# Exempt paths (specifications, notes, test reports, hooks, docs)
EXEMPT_PREFIXES = (
    ".scratch/",
    ".agents/",
    ".gemini/",
    ".git/",
    "docs/",
    "graphify-out/",
)

# Fallback fresh window (seconds) when transcript start time is unavailable (e.g. CLI test runs)
DEFAULT_FRESH_WINDOW_SECONDS = 7200  # 2 hours


def get_project_root() -> Path:
    """Resolve the repository root deterministically from this script's location."""
    return Path(__file__).resolve().parent.parent.parent


def get_user_inputs(transcript_path: str) -> list[float]:
    """
    Parse transcript.jsonl and return sorted list of UNIX timestamps (epoch seconds)
    of all messages sent by the user (USER_EXPLICIT / USER_INPUT).
    """
    if not transcript_path:
        return []
    tpath = Path(transcript_path)
    if not tpath.exists():
        return []

    user_times = []
    try:
        with open(tpath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    is_user = (
                        entry.get("source") == "USER_EXPLICIT"
                        or entry.get("type") == "USER_INPUT"
                    )
                    if is_user:
                        ts_str = entry.get("created_at")
                        if ts_str:
                            if ts_str.endswith("Z"):
                                ts_str = ts_str[:-1] + "+00:00"
                            epoch = datetime.fromisoformat(ts_str).timestamp()
                            user_times.append(epoch)
                except Exception:
                    continue
    except Exception:
        pass

    user_times.sort()
    return user_times


def get_latest_user_input_time(transcript_path: str) -> float:
    """Return UNIX timestamp of the most recent user input, or 0.0 if not found."""
    user_inputs = get_user_inputs(transcript_path)
    return user_inputs[-1] if user_inputs else 0.0


def get_session_start_mtime(transcript_path: str) -> float:
    """
    Determine the minimum modification timestamp for an active session's spec.
    First tries to read created_at from the first line of transcript.jsonl.
    Falls back to file stat birth/ctime - 60s, or time.time() - 2 hours.
    """
    if transcript_path:
        tpath = Path(transcript_path)
        if tpath.exists():
            try:
                with open(tpath, "r", encoding="utf-8") as f:
                    first_line = f.readline().strip()
                    if first_line:
                        data = json.loads(first_line)
                        ts = data.get("created_at")
                        if ts:
                            if ts.endswith("Z"):
                                ts = ts[:-1] + "+00:00"
                            return datetime.fromisoformat(ts).timestamp() - 60.0
            except Exception:
                pass
            try:
                stat = tpath.stat()
                birth = getattr(stat, "st_birthtime", None) or stat.st_ctime
                return float(birth) - 60.0
            except Exception:
                pass
    return time.time() - DEFAULT_FRESH_WINDOW_SECONDS


def get_spec_creation_time(spec_file: Path) -> float:
    """Get the birth/creation time of the spec file, falling back to min(ctime, mtime)."""
    st = spec_file.stat()
    return getattr(st, "st_birthtime", None) or min(st.st_ctime, st.st_mtime)


def is_frozen_spec_target(target_path: str, project_root: Path, transcript_path: str = "") -> tuple[bool, str]:
    """
    Check if a tool targets a feature's spec.md or issues/*.md after Round 1 is complete.
    Once initial build is completed or edits exist, spec.md and issues/*.md are permanently frozen.
    """
    if not target_path:
        return False, ""
    try:
        p = Path(target_path)
        resolved = p.resolve() if p.is_absolute() else (project_root / p).resolve()
        rel = str(resolved.relative_to(project_root.resolve()))
    except Exception:
        return False, ""

    # Check if target is inside .scratch/<feature>/spec.md
    parts = Path(rel).parts
    if len(parts) >= 3 and parts[0] == ".scratch":
        feature_name = parts[1]
        sub = parts[2]
        # Only spec.md is frozen against direct modification once Round 1 is complete.
        # issues/*.md can always be updated to tick checkboxes (- [x]) and update status.
        if sub == "spec.md":
            feature_dir = project_root / ".scratch" / feature_name
            if not feature_dir.exists():
                return False, ""

            # Check 1: Do edits already exist? Once edits exist, initial round spec is closed.
            edits_dir = feature_dir / "edits"
            if edits_dir.exists() and list(edits_dir.glob("*.md")):
                return True, rel

            # Check 2: Was spec created before current session window? Historical specs are closed.
            spec_file = feature_dir / "spec.md"
            if spec_file.exists():
                session_start = get_session_start_mtime(transcript_path)
                spec_creation = get_spec_creation_time(spec_file)
                if spec_creation < session_start:
                    return True, rel
    return False, ""


def is_production_code_modification(
    tool_name: str, args: dict, project_root: Path, transcript_path: str = ""
) -> tuple[bool, str]:
    """Check if the tool call targets production code or frozen specs/tickets."""
    target_path = ""
    project_root = project_root.resolve()

    if tool_name in ("write_file", "edit_file"):
        target_path = args.get("Path") or args.get("path") or ""
    elif tool_name == "run_command":
        cmd = args.get("CommandLine") or args.get("command") or ""
        # 1. Detect shell redirection or file-mutating commands targeting paths
        match = re.search(r"(?:>|>>|\bcp\b|\bmv\b|\bsed\b|\bpatch\b)\s+([^\s;&|]+)", cmd)
        if match:
            target_path = match.group(1).strip()
        else:
            # 2. Detect database mutation commands
            if re.search(r"(?i)\b(sqlite3|wrangler\s+d1|db:seed|db:migrate|drizzle-kit)\b", cmd):
                if re.search(r"(?i)\b(update|insert|delete|drop|alter|create|replace|apply|seed)\b", cmd):
                    return True, f"db_mutation: {cmd.strip()[:80]}"
            # 3. Detect inline scripts performing DB / code mutations
            if re.search(r"(?i)\b(node|python3?|tsx|ts-node)\s+.*-e\s+.*(update|insert|delete|drop|exec|run)\b", cmd):
                return True, f"inline_script_mutation: {cmd.strip()[:80]}"

    if not target_path:
        return False, ""

    # Check if target is a frozen spec or frozen tracer ticket
    is_frozen, frozen_rel = is_frozen_spec_target(target_path, project_root, transcript_path)
    if is_frozen:
        return True, f"frozen_spec: {frozen_rel}"

    try:
        p = Path(target_path)
        resolved = p.resolve() if p.is_absolute() else (project_root / p).resolve()

        # Check protected specific files (like GLOSSARY.md, AGENTS.md, package.json)
        if p.name in PROTECTED_FILES:
            return True, str(p.name)

        rel_path = str(resolved.relative_to(project_root))
    except Exception:
        rel_path = target_path

    # Normalize leading ./
    if rel_path.startswith("./"):
        rel_path = rel_path[2:]

    # Check exemptions first
    for ex in EXEMPT_PREFIXES:
        if rel_path.startswith(ex):
            return False, rel_path

    # Check protected targets
    for prefix in PROTECTED_PREFIXES:
        if rel_path.startswith(prefix):
            return True, rel_path

    # Check root-level code files
    for ext in PROTECTED_EXTENSIONS:
        if rel_path.endswith(ext) and "/" not in rel_path:
            return True, rel_path

    return False, rel_path


def validate_edit_ticket_content(edit_file: Path) -> tuple[bool, str]:
    """
    Verify that an edit ticket (.scratch/<feature-slug>/edits/<NN>-<slug>.md) contains
    substantive analysis of user feedback:
      - Why the user requested the edit / what was disliked or unsatisfactory
      - Planned changes / target files
    """
    try:
        text = edit_file.read_text(encoding="utf-8").strip()
    except Exception as e:
        return False, f"Cannot read edit ticket '{edit_file.name}': {e}"

    if len(text) < 80:
        return (
            False,
            f"Edit ticket '{edit_file.name}' is too short ({len(text)} bytes). "
            f"It must provide a detailed change spec and feedback analysis.",
        )

    # Check for rationale / feedback analysis
    has_rationale = bool(
        re.search(
            r"(?i)(#+\s*rationale|#+\s*user\s*feedback|\bwhy\b|requested\s*change|pain\s*point|ไม่ถูกใจ|เหตุผล)",
            text,
        )
    )
    if not has_rationale:
        return (
            False,
            f"Edit ticket '{edit_file.name}' is missing user feedback analysis / rationale.\n"
            f"Per lifecycle rules, you must analyze why the user requested the edit "
            f"(what was unsatisfactory or disliked) under '## Rationale & Impact' or 'Requested Change'.",
        )

    # Check for planned changes or scope
    has_changes = bool(
        re.search(
            r"(?i)(#+\s*planned\s*changes|#+\s*acceptance\s*criteria|\btarget\s*files\b|##\s*changes|- \[[ x]\])",
            text,
        )
    )
    if not has_changes:
        return (
            False,
            f"Edit ticket '{edit_file.name}' is missing planned changes or acceptance criteria.\n"
            f"Include '## Planned Changes' or '## Acceptance Criteria' to specify the verifiable scope.",
        )

    return True, ""


def check_spec_in_workspace(project_root: Path, transcript_path: str = "", target_path: str = "") -> tuple[bool, str]:
    """
    Strictly verify that an active feature folder in .scratch/<feature-slug>/ satisfies either:
      Stage 1 (Initial Feature Lifecycle in Current Session):
        1. .scratch/<feature-slug>/spec.md (fresh in active session via to-spec)
        2. .scratch/<feature-slug>/issues/*.md (at least one ticket file via to-tickets)
        3. ZERO edits in .scratch/<feature-slug>/edits/
        4. User Approval Gate: user approved in a subsequent turn (exactly 1 user input after spec).
      Stage 2 (Subsequent Edit / Modification within Current Session via to-edit):
        Pre-requisites:
        - The feature MUST belong to the CURRENT session (spec.md created in active session).
        - Both spec.md AND issues/*.md MUST exist (completed initial lifecycle).
        - .scratch/<feature-slug>/edits/<NN>-<slug>.md dedicated edit ticket created/updated
          AFTER the most recent user request via to-edit.
        - Edit ticket contains substantive user feedback analysis.
      Cross-Session Rule:
        Historical features from previous sessions are closed. You CANNOT attach edit tickets
        to historical features across sessions. Every new session starts with to-spec and to-tickets.
    Note: Antigravity brain artifacts (.gemini/antigravity/brain/) are NEVER accepted.
    """
    if target_path.startswith("frozen_spec:"):
        frozen_file = target_path.split(":", 1)[1].strip()
        return (
            False,
            f"🚨 FROZEN SPEC/TICKETS: Modifying '{frozen_file}' is forbidden!\n"
            f"'to-spec' and 'to-tickets' are strictly for the initial round (inception) before implementation.\n"
            f"Once the initial build is completed, you cannot edit 'spec.md' or 'issues/*.md'.\n"
            f"All subsequent changes, tweaks, and bug fixes must be recorded as edit tickets in "
            f"'.scratch/<feature-slug>/edits/<NN>-<slug>.md' using 'to-edit'.",
        )

    project_root = project_root.resolve()
    scratch_dir = project_root / ".scratch"
    if not scratch_dir.exists():
        return False, "No .scratch/ directory found in project workspace."

    session_start_mtime = get_session_start_mtime(transcript_path)
    user_inputs = get_user_inputs(transcript_path)
    latest_user_time = user_inputs[-1] if user_inputs else 0.0

    # Required threshold for edit ticket: must be newer than the latest user prompt
    edit_min_mtime = (latest_user_time - 5.0) if latest_user_time > 0 else session_start_mtime

    # 1. Check for dedicated edit tickets created for THIS specific user request (Stage 2)
    candidate_edits = list(scratch_dir.glob("*/edits/*.md"))
    fresh_edits = [f for f in candidate_edits if f.stat().st_mtime >= edit_min_mtime]
    if fresh_edits:
        fresh_edits.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        latest_edit = fresh_edits[0]
        feature_dir = latest_edit.parent.parent
        rel_edit = latest_edit.relative_to(project_root)
        rel_feature = feature_dir.relative_to(project_root)

        spec_file = feature_dir / "spec.md"
        issues_dir = feature_dir / "issues"
        issue_files = list(issues_dir.glob("*.md")) if issues_dir.exists() else []

        # MANDATORY GATE: to-edit is ONLY allowed if the feature already completed to-spec and to-tickets!
        if not spec_file.exists() or not issue_files:
            return (
                False,
                f"🚨 STRICT ORDER VIOLATION: Found edit ticket '{rel_edit}', but feature '{rel_feature}' "
                f"has NOT completed the initial lifecycle!\n"
                f"Every task MUST start with 'to-spec' (.scratch/<feature-slug>/spec.md) "
                f"followed by 'to-tickets' (.scratch/<feature-slug>/issues/*.md).\n"
                f"'to-edit' is ONLY valid for subsequent edits AFTER to-spec and to-tickets are completed.",
            )

        # MANDATORY SESSION BOUNDARY GATE:
        # to-edit can ONLY be used within a feature that was created in THIS session!
        # Historical features from previous sessions are closed and immutable.
        spec_creation_epoch = get_spec_creation_time(spec_file)
        if spec_creation_epoch < session_start_mtime:
            return (
                False,
                f"🚨 CROSS-SESSION EDIT FORBIDDEN: Feature '{rel_feature}' was created in a previous session (closed).\n"
                f"You CANNOT attach edit tickets to historical features across sessions!\n"
                f"Every new session / task MUST start fresh with 'to-spec' (.scratch/<new-feature-slug>/spec.md) "
                f"followed by 'to-tickets' (.scratch/<new-feature-slug>/issues/*.md).\n"
                f"Historical features may be referenced for context ('หยิบยกมาดูได้'), but cannot be modified.",
            )

        # Content validation: verify user feedback analysis
        valid_content, err_msg = validate_edit_ticket_content(latest_edit)
        if not valid_content:
            return False, f"🚨 INCOMPLETE EDIT TICKET: {err_msg}"

        return (
            True,
            f"Verified dedicated edit ticket '{rel_edit}' created for this user request under '{rel_feature}' "
            f"(with {len(issue_files)} base ticket(s) in issues/).",
        )

    # 2. Check for fresh initial build specs (.scratch/<feature-slug>/spec.md) created in THIS session
    candidate_specs = list(scratch_dir.glob("*/spec.md"))
    fresh_specs = [f for f in candidate_specs if get_spec_creation_time(f) >= session_start_mtime]
    if not fresh_specs:
        return (
            False,
            f"🚨 NO ACTIVE SPEC IN CURRENT SESSION: No feature specification was created in this session.\n"
            f"Every new task / session MUST start fresh with 'to-spec' (.scratch/<new-feature-slug>/spec.md) "
            f"followed by 'to-tickets' (.scratch/<new-feature-slug>/issues/*.md).\n"
            f"You CANNOT reuse or edit historical features from past sessions (e.g. past database/feature folders).\n"
            f"Run 'to-spec' to create a new feature spec for this session's work.",
        )

    # Sort fresh specs by creation time (most recent first)
    fresh_specs.sort(key=get_spec_creation_time, reverse=True)
    latest_spec = fresh_specs[0]
    feature_dir = latest_spec.parent
    rel_feature = feature_dir.relative_to(project_root)
    spec_created_epoch = get_spec_creation_time(latest_spec)

    # Check if this feature has already entered edit mode (has existing edits)
    edits_dir = feature_dir / "edits"
    existing_edits = list(edits_dir.glob("*.md")) if edits_dir.exists() else []
    if existing_edits:
        return (
            False,
            f"🚨 EDIT TICKET REQUIRED: Feature '{rel_feature}' has already completed its initial round "
            f"and has {len(existing_edits)} existing edit ticket(s).\n"
            f"Per lifecycle rules, 'to-spec' and 'to-tickets' cannot be re-used after the initial build.\n"
            f"You MUST use 'to-edit' to create a new edit ticket in '{rel_feature}/edits/<NN>-<slug>.md' "
            f"analyzing user feedback for this request.",
        )

    # Check for issues/ tickets (.scratch/<feature-slug>/issues/*.md)
    issues_dir = feature_dir / "issues"
    issue_files = list(issues_dir.glob("*.md")) if issues_dir.exists() else []
    if not issue_files:
        return (
            False,
            f"Found '{rel_feature}/spec.md', but no tracer-bullet ticket files found in '{rel_feature}/issues/*.md'.\n"
            f"STRICT ORDER: You must run 'to-tickets' to create tickets in '{rel_feature}/issues/*.md' "
            f"BEFORE writing any production code!",
        )

    # Check User Approval Gate (Turn Separation)
    if user_inputs:
        post_spec_user_times = [t for t in user_inputs if t >= (spec_created_epoch - 2.0)]

        if len(post_spec_user_times) == 0:
            return (
                False,
                f"🚨 USER APPROVAL GATE: Active spec '{rel_feature}/spec.md' was created in the CURRENT turn "
                f"(spec created at: {spec_created_epoch:.1f} > user input: {latest_user_time:.1f}).\n"
                f"You CANNOT implement in the same turn you create the spec!\n"
                f"You MUST stop now, present the spec and tickets to the user, and wait for their explicit approval "
                f"in a subsequent turn before modifying protected code or database state.",
            )

        if len(post_spec_user_times) >= 2:
            return (
                False,
                f"🚨 EDIT TICKET REQUIRED: Feature '{rel_feature}' completed its initial build in a previous turn.\n"
                f"The user has sent subsequent feedback/modifications. Modifying code using 'spec.md' is no longer permitted.\n"
                f"Per lifecycle rules, all subsequent changes must use 'to-edit' to create a new ticket in "
                f"'{rel_feature}/edits/<NN>-<slug>.md' analyzing why the change was requested.",
            )

    return (
        True,
        f"Verified active approved initial spec at '{rel_feature}/spec.md' with {len(issue_files)} ticket(s) in '{rel_feature}/issues/'.",
    )


def check_graphify_installed(project_root: Path) -> tuple[bool, str]:
    """
    Verify that graphify is installed and accessible in the environment.
    SkillFlow mandates graphify for the Zero-Guessing architecture invariant.
    """
    # 1. Check persisted .graphify_python
    graphify_py_path = project_root / "graphify-out" / ".graphify_python"
    if graphify_py_path.exists():
        py_bin = graphify_py_path.read_text(encoding="utf-8").strip()
        if py_bin and Path(py_bin).exists():
            try:
                res = subprocess.run([py_bin, "-c", "import graphify"], capture_output=True, timeout=5)
                if res.returncode == 0:
                    return True, ""
            except Exception:
                pass

    # 2. Check binary in PATH
    bin_path = shutil.which("graphify")
    if bin_path:
        return True, ""

    # 3. Check current python interpreters
    for py in (sys.executable, "python3", "python"):
        resolved_py = shutil.which(py)
        if resolved_py:
            try:
                res = subprocess.run([resolved_py, "-c", "import graphify"], capture_output=True, timeout=5)
                if res.returncode == 0:
                    return True, ""
            except Exception:
                pass

    return (
        False,
        "🚨 MANDATORY GRAPHIFY MISSING: 'graphify' is required for all projects in SkillFlow.\n"
        "The Zero-Guessing Invariant requires graph traversal before modifying code.\n"
        "Install graphify via: 'uv tool install graphifyy' or 'pip install graphifyy' and re-run.",
    )


def validate_scratch_write(tool_name: str, args: dict, project_root: Path) -> tuple[bool, str]:
    """
    Validate that writes to .scratch/<feature-slug>/ follow the canonical templates
    prescribed by to-spec and to-tickets, preventing non-compliant or guessed specs/tickets.
    """
    if tool_name not in ("write_file", "edit_file"):
        return True, ""

    raw_path = args.get("Path") or args.get("path") or ""
    if not raw_path:
        return True, ""

    try:
        p = Path(raw_path)
        resolved = p.resolve() if p.is_absolute() else (project_root / p).resolve()
        rel = str(resolved.relative_to(project_root.resolve())).replace("\\", "/")
    except Exception:
        rel = raw_path.replace("\\", "/")

    parts = rel.split("/")
    if len(parts) >= 3 and parts[0] == ".scratch":
        feature_name = parts[1]
        sub = parts[2]

        if tool_name == "edit_file":
            try:
                target_file = resolved if resolved.exists() else (project_root / rel)
                if target_file.exists():
                    existing_text = target_file.read_text(encoding="utf-8")
                    target = args.get("Target", "")
                    replacement = args.get("Replacement", "")
                    content = existing_text.replace(target, replacement)
                else:
                    content = args.get("Replacement") or ""
            except Exception:
                content = args.get("Replacement") or ""
        else:
            content = args.get("Content") or ""

        # 1. Validate .scratch/<feature>/spec.md
        if sub == "spec.md":
            required_sections = [
                (r"(?i)##\s*Problem\s*Statement", "## Problem Statement"),
                (r"(?i)##\s*Solution", "## Solution"),
                (r"(?i)##\s*User\s*Stories", "## User Stories"),
                (r"(?i)##\s*Implementation\s*Decisions", "## Implementation Decisions"),
                (r"(?i)##\s*Testing\s*Decisions", "## Testing Decisions"),
                (r"(?i)##\s*Out\s*of\s*Scope", "## Out of Scope"),
            ]
            missing = [name for pat, name in required_sections if not re.search(pat, content)]
            if missing:
                return (
                    False,
                    f"🚨 INVALID SPEC TEMPLATE: '.scratch/{feature_name}/spec.md' is missing required sections from 'to-spec':\n"
                    f"  Missing: {', '.join(missing)}\n"
                    f"Per lifecycle rules, you MUST read '.agents/skills/to-spec/SKILL.md' and follow the canonical template:\n"
                    f"  - ## Problem Statement\n"
                    f"  - ## Solution\n"
                    f"  - ## User Stories (Long numbered list: 1. As an <actor>, I want <feature>, so that <benefit>)\n"
                    f"  - ## Implementation Decisions (High-level decisions, NO raw code or fragile file paths)\n"
                    f"  - ## Testing Decisions (Key behavior, system boundaries, invariants)\n"
                    f"  - ## Out of Scope",
                )

        # 2. Validate .scratch/<feature>/issues/<NN>-<slug>.md
        elif sub == "issues" and len(parts) >= 4 and parts[3].endswith(".md"):
            required_fields = [
                (r"(?i)\*\*What to build:\*\*", "**What to build:**"),
                (r"(?i)\*\*Blocked by:\*\*", "**Blocked by:**"),
                (r"(?i)\*\*Status:\*\*", "**Status:** ready-for-agent"),
            ]
            missing_fields = [name for pat, name in required_fields if not re.search(pat, content)]
            if missing_fields:
                return (
                    False,
                    f"🚨 INVALID TICKET TEMPLATE: '.scratch/{feature_name}/issues/{parts[3]}' is missing required fields from 'to-tickets':\n"
                    f"  Missing: {', '.join(missing_fields)}\n"
                    f"Per lifecycle rules, you MUST read '.agents/skills/to-tickets/SKILL.md' and format each tracer-bullet ticket as:\n"
                    f"  # <NN>: <Ticket title>\n"
                    f"  **What to build:** <end-to-end behavior>\n"
                    f"  **Blocked by:** <blockers or 'None (can start immediately)'>\n"
                    f"  **Status:** ready-for-agent\n"
                    f"  - [ ] Acceptance criteria checkboxes",
                )

    return True, ""


def main():
    if sys.stdin.isatty():
        print(json.dumps({"decision": "allow"}))
        return

    try:
        raw = sys.stdin.read().strip()
        if not raw:
            print(json.dumps({"decision": "allow"}))
            return
        payload = json.loads(raw)
    except Exception:
        print(json.dumps({"decision": "allow"}))
        return

    tool_call = payload.get("toolCall", {})
    tool_name = tool_call.get("name") or payload.get("tool_name") or ""
    args = tool_call.get("args") or payload.get("args") or {}
    transcript_path = payload.get("transcriptPath") or payload.get("transcript_path") or ""

    project_root = get_project_root()
    is_protected, target_path = is_production_code_modification(tool_name, args, project_root, transcript_path)

    if not is_protected:
        # Validate format of any .scratch/ writes
        is_valid_scratch, scratch_err = validate_scratch_write(tool_name, args, project_root)
        if not is_valid_scratch:
            print(json.dumps({
                "decision": "deny",
                "reason": scratch_err
            }))
            return

        # Non-code modifications (e.g. writing .scratch/ specs, tickets, unit/e2e matrices) are allowed
        print(json.dumps({"decision": "allow"}))
        return

    # Check graphify installation (MANDATORY in SkillFlow)
    is_graphify_ready, graphify_err = check_graphify_installed(project_root)
    if not is_graphify_ready:
        print(json.dumps({
            "decision": "deny",
            "reason": graphify_err
        }))
        return

    # Strictly check .scratch/<feature-slug>/ in workspace
    has_workspace_spec, ws_msg = check_spec_in_workspace(project_root, transcript_path, target_path)

    if has_workspace_spec:
        print(json.dumps({"decision": "allow"}))
        return

    # No valid .scratch/<feature-slug>/ spec & issues or edit tickets found -> HARD BLOCK!
    deny_reason = (
        f"🚨 SPEC ENFORCEMENT GATE: Blocked modification to '{target_path}'.\n"
        f"Reason: {ws_msg}\n"
        f"MANDATORY WORKSPACE STRUCTURE (.scratch/<feature-slug>/):\n"
        f"  - Initial Feature (Round 1 only): Run 'to-spec' (.scratch/<feature-slug>/spec.md) and 'to-tickets' (.scratch/<feature-slug>/issues/<NN>-<slug>.md)\n"
        f"  - Subsequent Edit / Fix (Round 2+): Run 'to-edit' (.scratch/<feature-slug>/edits/<NN>-<slug>.md) with user feedback analysis\n"
        f"NOTE: Writing specs only to Antigravity brain artifacts (.gemini/antigravity/brain/) is NOT permitted."
    )

    print(json.dumps({
        "decision": "deny",
        "reason": deny_reason
    }))


if __name__ == "__main__":
    main()
