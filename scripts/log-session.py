#!/usr/bin/env python3
"""
Memento - Session Logger
"Facts, not memory." — Track your token usage across sessions.

Logs session token data to ~/.claude/memento-stats.json for trend analysis.
"""

import json
import sys
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

# Import token counting from sibling module
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

try:
    from importlib.util import spec_from_loader, module_from_spec
    from importlib.machinery import SourceFileLoader

    count_tokens_path = SCRIPT_DIR / "count-tokens.py"
    spec = spec_from_loader("count_tokens", SourceFileLoader("count_tokens", str(count_tokens_path)))
    count_tokens_module = module_from_spec(spec)
    spec.loader.exec_module(count_tokens_module)
    analyze_project = count_tokens_module.analyze_project
except Exception:
    # Fallback: run as subprocess
    analyze_project = None


STATS_FILE = Path.home() / ".claude" / "memento-stats.json"
MAX_SESSIONS = 50  # Keep last N sessions


def load_stats() -> dict:
    """Load existing stats or create new structure."""
    if STATS_FILE.exists():
        try:
            with open(STATS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"sessions": [], "version": "1.0"}


def save_stats(stats: dict) -> None:
    """Save stats to file, creating directory if needed."""
    STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)


def get_baseline_tokens(project_path: str) -> int:
    """Get current baseline token count for project."""
    if analyze_project:
        try:
            result = analyze_project(project_path)
            return result.get("estimates", {}).get("baseline_total", 0)
        except Exception:
            pass

    # Fallback: run count-tokens.py as subprocess
    import subprocess
    try:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "count-tokens.py"), "--project", project_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get("estimates", {}).get("baseline_total", 0)
    except Exception:
        pass

    return 0


def log_session_start(project_path: str) -> str:
    """Log a new session start. Returns session ID."""
    stats = load_stats()

    session_id = str(uuid.uuid4())[:8]
    baseline_tokens = get_baseline_tokens(project_path)

    session = {
        "id": session_id,
        "project": os.path.basename(project_path) or project_path,
        "project_path": str(Path(project_path).resolve()),
        "started_at": datetime.now().isoformat(),
        "ended_at": None,
        "baseline_tokens": baseline_tokens,
        "final_tokens": None,
        "duration_minutes": None
    }

    stats["sessions"].append(session)

    # Trim to max sessions
    if len(stats["sessions"]) > MAX_SESSIONS:
        stats["sessions"] = stats["sessions"][-MAX_SESSIONS:]

    save_stats(stats)
    return session_id


def log_session_stop(project_path: str) -> Optional[str]:
    """Log session end. Updates most recent matching session."""
    stats = load_stats()
    project_path_resolved = str(Path(project_path).resolve())

    # Find most recent open session for this project
    for session in reversed(stats["sessions"]):
        if session.get("project_path") == project_path_resolved and session.get("ended_at") is None:
            now = datetime.now()
            started = datetime.fromisoformat(session["started_at"])
            duration = (now - started).total_seconds() / 60

            # Estimate final tokens (baseline + estimated conversation)
            # This is a rough estimate - actual would require API access
            baseline = session.get("baseline_tokens", 0)
            estimated_conversation = int(duration * 500)  # ~500 tokens/min average

            session["ended_at"] = now.isoformat()
            session["final_tokens"] = baseline + estimated_conversation
            session["duration_minutes"] = round(duration, 1)

            save_stats(stats)
            return session["id"]

    return None


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Memento - Session Token Logger"
    )
    parser.add_argument(
        "--event", "-e",
        required=True,
        choices=["start", "stop"],
        help="Session event type"
    )
    parser.add_argument(
        "--project", "-p",
        default=".",
        help="Project path"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress output"
    )

    args = parser.parse_args()

    if args.event == "start":
        session_id = log_session_start(args.project)
        if not args.quiet:
            print(json.dumps({"status": "started", "session_id": session_id}))
    else:
        session_id = log_session_stop(args.project)
        if not args.quiet:
            if session_id:
                print(json.dumps({"status": "stopped", "session_id": session_id}))
            else:
                print(json.dumps({"status": "no_open_session"}))


if __name__ == "__main__":
    main()
