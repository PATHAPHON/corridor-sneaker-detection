#!/usr/bin/env python3
"""
session-start-main.py — SessionStart hook for Main Orchestrator Agent.
Injects project-specific AGENTS.md, GLOSSARY.md, and core lifecycle guidelines
into the system prompt context at the start of each session.
"""
import json
import os
import shutil
import subprocess
import sys

# Ensure hooks directory is in sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from agent_detector import (
    parse_hook_input,
    detect_session_role,
    read_files_to_message,
    make_inject_payload,
    make_empty_payload,
)

agents_dir = os.path.dirname(script_dir)
project_root = os.path.dirname(agents_dir)

data = parse_hook_input()
force = "--force" in sys.argv
role = detect_session_role(data, default_role="main")

# If this session belongs to a specialized subagent, skip main context
if not force and role != "main":
    print(json.dumps(make_empty_payload(data)))
    sys.exit(0)

def is_graphify_available(root: str) -> bool:
    graphify_py_path = os.path.join(root, "graphify-out", ".graphify_python")
    if os.path.exists(graphify_py_path):
        try:
            with open(graphify_py_path, "r", encoding="utf-8") as f:
                py_bin = f.read().strip()
                if py_bin and os.path.exists(py_bin):
                    res = subprocess.run([py_bin, "-c", "import graphify"], capture_output=True, timeout=3)
                    if res.returncode == 0:
                        return True
        except Exception:
            pass
    if shutil.which("graphify"):
        return True
    for py in (sys.executable, "python3", "python"):
        resolved = shutil.which(py)
        if resolved:
            try:
                res = subprocess.run([resolved, "-c", "import graphify"], capture_output=True, timeout=3)
                if res.returncode == 0:
                    return True
            except Exception:
                pass
    return False


# The mandatory SSOT files injected into main agent sessions if present
MANDATORY_FILES = [
    (os.path.join(project_root, "AGENTS.md"), "AGENTS.md"),
    (os.path.join(project_root, "GLOSSARY.md"), "GLOSSARY.md"),
    (os.path.join(agents_dir, "skills", "lifecycle", "SKILL.md"), "lifecycle SKILL.md"),
]

# Filter only files that actually exist to avoid polluting prompt if absent
existing_files = [item for item in MANDATORY_FILES if os.path.exists(item[0])]

if existing_files:
    message = read_files_to_message(existing_files)
    if not is_graphify_available(project_root):
        message += (
            "\n\n🚨 CRITICAL ALERT: 'graphify' is NOT installed in this environment!\n"
            "SkillFlow mandates graphify for Search-First exploration and code mutation gating.\n"
            "Please run 'uv tool install graphifyy' or 'pip install graphifyy'."
        )
    print(json.dumps(make_inject_payload(message, data)))
else:
    print(json.dumps(make_empty_payload(data)))
