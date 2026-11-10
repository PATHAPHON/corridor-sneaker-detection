#!/usr/bin/env python3
"""
trace_hook.py — Active Hook for Antigravity & Claude Code
Collects all tool calls into session-isolated and rolling trace logs.
"""
import json
import os
import sys
import time
from pathlib import Path

# Explicitly target .agents/.agent-evolution/data/traces
AGENTS_DIR = Path(__file__).resolve().parent.parent
TRACE_DIR = AGENTS_DIR / ".agent-evolution" / "data" / "traces"
TRACE_DIR.mkdir(parents=True, exist_ok=True)
CURRENT_TRACE_FILE = TRACE_DIR / "current_trace.json"

def get_trace_file(session_id: str) -> Path:
    if session_id:
        return TRACE_DIR / f"sess_{session_id}.json"
    return CURRENT_TRACE_FILE

def extract_latest_user_prompt(conversation_id: str) -> str:
    """Read the actual transcript for this conversation to get the latest user prompt."""
    if not conversation_id:
        return ""
    brain_dir = Path(os.path.expanduser("~/.gemini/antigravity/brain"))
    transcript_path = brain_dir / conversation_id / ".system_generated" / "logs" / "transcript.jsonl"
    if not transcript_path.exists():
        return ""
    try:
        import re
        last_prompt = ""
        with open(transcript_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                    if item.get("type") == "USER_INPUT" and item.get("content"):
                        content = item.get("content", "")
                        match = re.search(r"<USER_REQUEST>(.*?)</USER_REQUEST>", content, re.DOTALL)
                        if match:
                            last_prompt = match.group(1).strip()
                        else:
                            last_prompt = content.strip()
                except Exception:
                    continue
        return last_prompt
    except Exception:
        return ""

def load_trace(trace_path: Path, session_id: str, goal: str):
    if trace_path.exists():
        try:
            return json.loads(trace_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "version": "1.0.0",
        "session_id": session_id or f"sess_{int(time.time())}",
        "initial_goal": goal or "Interactive Agent Session",
        "current_goal": goal or "Interactive Agent Session",
        "goal": goal or "Interactive Agent Session",
        "context": {
            "cwd": os.getcwd(),
            "os": sys.platform
        },
        "prompts": [],
        "steps": [],
        "changed_files": []
    }

def save_trace(data: dict, session_id: str):
    serialized = json.dumps(data, indent=2, ensure_ascii=False)
    # 1. Always update pointer file
    CURRENT_TRACE_FILE.write_text(serialized, encoding="utf-8")
    # 2. Update session-specific file
    if session_id:
        sess_file = TRACE_DIR / f"sess_{session_id}.json"
        sess_file.write_text(serialized, encoding="utf-8")

def main():
    if sys.stdin.isatty():
        print(json.dumps({}))
        return

    try:
        raw = sys.stdin.read().strip()
        if not raw:
            print(json.dumps({}))
            return
        payload = json.loads(raw)
    except Exception:
        print(json.dumps({}))
        return

    # Extract Antigravity / Claude Code common fields
    conversation_id = (
        payload.get("conversationId")
        or os.environ.get("ANTIGRAVITY_CONVERSATION_ID")
        or payload.get("session_id")
        or ""
    )
    goal = payload.get("lastUserInput") or payload.get("prompt") or ""
    tool_call = payload.get("toolCall", {})
    tool_name = tool_call.get("name") or payload.get("tool_name") or "unknown_tool"
    args = tool_call.get("args") or payload.get("args") or {}

    command = args.get("CommandLine") or args.get("command") or args.get("Path") or str(args)
    error_msg = payload.get("error")
    exit_code = 1 if error_msg else 0

    trace_path = get_trace_file(conversation_id)
    trace = load_trace(trace_path, conversation_id, goal)

    # Context enhancement: Resolve active user prompt from payload or live transcript
    active_prompt = goal or extract_latest_user_prompt(conversation_id)
    if "prompts" not in trace:
        trace["prompts"] = []
    
    # Preserve initial goal permanently
    if "initial_goal" not in trace:
        trace["initial_goal"] = trace.get("goal") or active_prompt or "Interactive Agent Session"

    # If this is a new prompt or first prompt, append to prompts list (never deletes old prompts)
    if active_prompt and (not trace["prompts"] or trace["prompts"][-1].get("text") != active_prompt):
        trace["prompts"].append({
            "prompt_index": len(trace["prompts"]) + 1,
            "text": active_prompt,
            "started_at_step": len(trace["steps"]) + 1,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        })
        # Keep both: latest prompt (current_goal/goal) and original (initial_goal)
        trace["current_goal"] = active_prompt
        trace["goal"] = active_prompt

    current_prompt_index = len(trace["prompts"]) if trace.get("prompts") else 1

    step_record = {
        "step": len(trace["steps"]) + 1,
        "prompt_index": current_prompt_index,
        "prompt_context": active_prompt[:120] if active_prompt else None,
        "tool": tool_name,
        "command": command,
        "exit_code": exit_code,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "error": str(error_msg) if error_msg else None,
        "args_snippet": str(args)[:300]
    }
    trace["steps"].append(step_record)
    save_trace(trace, conversation_id)

    # Standard hook return expected by Antigravity PostToolUse
    print(json.dumps({}))

if __name__ == "__main__":
    main()
