#!/usr/bin/env python3
"""
Memento - Command Logger
"Every fact is a tattoo." — Track command usage for pattern analysis.

Logs Bash command usage to ~/.claude/memento-commands.json for usage analytics.
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

COMMANDS_FILE = Path.home() / ".claude" / "memento-commands.json"
MAX_COMMANDS = 500  # Keep last N commands


def load_commands() -> dict:
    """Load existing command log or create new structure."""
    if COMMANDS_FILE.exists():
        try:
            with open(COMMANDS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"commands": [], "version": "1.0"}


def save_commands(data: dict) -> None:
    """Save commands to file, creating directory if needed."""
    COMMANDS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(COMMANDS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def log_command(tool_input: str, project_path: str) -> None:
    """Log a command execution."""
    data = load_commands()

    # Parse tool input to extract command if JSON
    command = tool_input
    if tool_input.startswith('{'):
        try:
            parsed = json.loads(tool_input)
            command = parsed.get("command", tool_input)
        except json.JSONDecodeError:
            pass

    entry = {
        "command": command[:500],  # Truncate very long commands
        "project": os.path.basename(project_path) or project_path,
        "timestamp": datetime.now().isoformat()
    }

    data["commands"].append(entry)

    # Trim to max commands
    if len(data["commands"]) > MAX_COMMANDS:
        data["commands"] = data["commands"][-MAX_COMMANDS:]

    save_commands(data)


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Memento - Command Logger"
    )
    parser.add_argument(
        "--tool-input", "-i",
        default="",
        help="Tool input/command executed"
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

    if args.tool_input:
        log_command(args.tool_input, args.project)
        if not args.quiet:
            print(json.dumps({"status": "logged"}))


if __name__ == "__main__":
    main()
