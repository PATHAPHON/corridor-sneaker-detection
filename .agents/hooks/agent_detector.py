#!/usr/bin/env python3
"""
agent_detector.py — Shared helper for SessionStart hooks.
Detects whether the current session is the Main Orchestrator Agent ('main')
or a specialized subagent, and formats context injection payloads.
"""
import glob
import json
import os
import sys


def parse_hook_input():
    """Reads and parses hook context from stdin (if available)."""
    if sys.stdin.isatty():
        return {}
    try:
        content = sys.stdin.read().strip()
        if not content:
            return {}
        return json.loads(content)
    except Exception:
        return {}


def detect_session_role(data=None, default_role="main"):
    """
    Detects if the session is the main orchestrator ('main') or a delegated subagent.
    """
    if data is None:
        data = parse_hook_input()

    agent_type = data.get("agent_type", "")
    if isinstance(agent_type, str) and agent_type.strip() and agent_type.lower() != "main":
        return agent_type.lower()

    metadata = data.get("agent", {}) or data.get("agentMetadata", {}) or {}
    metadata_type = str(metadata.get("type", "")).lower()
    if metadata_type and metadata_type not in ("main", "root"):
        return metadata_type

    # Check if this session was invoked as a subagent via parent message
    transcript_path = data.get("transcript_path", "") or data.get("transcriptPath", "") or ""
    if transcript_path:
        conv_dir = os.path.dirname(os.path.dirname(os.path.dirname(transcript_path)))
        messages_dir = os.path.join(conv_dir, ".system_generated", "messages")
        if os.path.isdir(messages_dir):
            for msg_file in glob.glob(os.path.join(messages_dir, "*.json")):
                if os.path.basename(msg_file) == "read.json":
                    continue
                try:
                    with open(msg_file, "r", encoding="utf-8") as f:
                        msg = json.load(f)
                    tool_call = msg.get("sourceMetadata", {}).get("tool", {}).get("toolCall", {})
                    args_raw = tool_call.get("argumentsJson", "{}")
                    args = json.loads(args_raw)
                    type_name = (args.get("TypeName") or "").lower()
                    if type_name and type_name != "self":
                        return type_name
                except Exception:
                    pass

    return default_role


def read_files_to_message(files, header_banner=""):
    """Reads a list of (path, label) tuples and returns a single formatted string."""
    parts = []
    for path, label in files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            parts.append(f"=== {label} ===\n{content}")
        except FileNotFoundError:
            parts.append(f"=== {label} === (NOT FOUND: {path})")

    message = header_banner + "\n\n" + "\n\n".join(parts) if header_banner else "\n\n".join(parts)
    return message


def is_codex_caller(data=None):
    """Detects if hook was triggered by Codex or Antigravity."""
    if data is None:
        data = parse_hook_input()
    return (
        "hook_event_name" in data
        or "hookEventName" in data
        or "prompt" in data
        or os.environ.get("CODEX_HOME") is not None
    )


def make_inject_payload(message, data=None):
    """Formats JSON response compatible with both Antigravity and Codex."""
    if is_codex_caller(data):
        return {
            "hookSpecificOutput": {
                "hookEventName": (data or {}).get(
                    "hook_event_name", (data or {}).get("hookEventName", "SessionStart")
                ),
                "additionalContext": message,
            }
        }
    return {
        "injectSteps": [
            {
                "systemMessage": {
                    "systemMessage": message,
                }
            }
        ]
    }


def make_empty_payload(data=None):
    """Formats empty JSON response compatible with both Antigravity and Codex."""
    if is_codex_caller(data):
        return {
            "hookSpecificOutput": {
                "hookEventName": (data or {}).get(
                    "hook_event_name", (data or {}).get("hookEventName", "SessionStart")
                ),
                "additionalContext": "",
            }
        }
    return {"injectSteps": []}
