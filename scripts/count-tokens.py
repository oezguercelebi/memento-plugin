#!/usr/bin/env python3
"""
Memento - Token Counter
"Remember Sammy Jankis" — and remember your token budget.

Analyzes Claude Code project context and estimates token usage.
Uses tiktoken with cl100k_base encoding (similar to Claude's tokenization).
"""

import json
import sys
import os
from pathlib import Path
from typing import Optional

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False


def count_tokens(text: str) -> int:
    """Count tokens using tiktoken or fallback to estimation."""
    if TIKTOKEN_AVAILABLE:
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    else:
        # Rough estimation: ~4 characters per token for code
        return len(text) // 4


def analyze_file(filepath: str) -> dict:
    """Analyze a single file for token usage."""
    path = Path(filepath).expanduser()
    
    if not path.exists():
        return {
            "file": filepath,
            "exists": False,
            "error": "File not found"
        }
    
    try:
        content = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return {
            "file": filepath,
            "exists": True,
            "error": "Binary file - cannot analyze"
        }
    except Exception as e:
        return {
            "file": filepath,
            "exists": True,
            "error": str(e)
        }
    
    tokens = count_tokens(content)
    lines = len(content.splitlines())
    
    return {
        "file": filepath,
        "exists": True,
        "tokens": tokens,
        "lines": lines,
        "bytes": len(content.encode('utf-8')),
        "tokens_per_line": round(tokens / max(lines, 1), 1),
        "estimated": not TIKTOKEN_AVAILABLE
    }


def find_claude_configs(root: Path) -> dict:
    """Find all Claude Code configuration files in project."""
    configs = {
        "claude_md": [],
        "skills": [],
        "commands": [],
        "agents": [],
        "hooks": [],
        "mcp_config": None
    }
    
    # Project-level CLAUDE.md
    for claude_md_path in [
        root / "CLAUDE.md",
        root / ".claude" / "CLAUDE.md"
    ]:
        if claude_md_path.exists():
            configs["claude_md"].append(str(claude_md_path))
    
    # User-level CLAUDE.md
    user_claude_md = Path.home() / ".claude" / "CLAUDE.md"
    if user_claude_md.exists():
        configs["claude_md"].append(str(user_claude_md))
    
    # Skills
    skills_dirs = [
        root / ".claude" / "skills",
        Path.home() / ".claude" / "skills"
    ]
    for skills_dir in skills_dirs:
        if skills_dir.exists():
            for skill_md in skills_dir.rglob("SKILL.md"):
                configs["skills"].append(str(skill_md))
    
    # Commands
    commands_dirs = [
        root / ".claude" / "commands",
        Path.home() / ".claude" / "commands"
    ]
    for commands_dir in commands_dirs:
        if commands_dir.exists():
            for cmd in commands_dir.glob("*.md"):
                configs["commands"].append(str(cmd))
    
    # Agents
    agents_dirs = [
        root / ".claude" / "agents",
        Path.home() / ".claude" / "agents"
    ]
    for agents_dir in agents_dirs:
        if agents_dir.exists():
            for agent in agents_dir.glob("*.md"):
                configs["agents"].append(str(agent))
    
    # Hooks
    hooks_files = [
        root / ".claude" / "hooks.json",
        Path.home() / ".claude" / "hooks.json"
    ]
    for hooks_file in hooks_files:
        if hooks_file.exists():
            configs["hooks"].append(str(hooks_file))
    
    # MCP config
    mcp_files = [
        root / ".mcp.json",
        root / ".claude" / ".mcp.json",
        Path.home() / ".claude" / ".mcp.json"
    ]
    for mcp_file in mcp_files:
        if mcp_file.exists():
            configs["mcp_config"] = str(mcp_file)
            break
    
    return configs


def analyze_project(root_path: str = ".") -> dict:
    """Full project context analysis."""
    root = Path(root_path).resolve()
    configs = find_claude_configs(root)
    
    results = {
        "project_root": str(root),
        "tiktoken_available": TIKTOKEN_AVAILABLE,
        "components": {
            "claude_md": [],
            "skills": [],
            "commands": [],
            "agents": [],
            "hooks": [],
            "mcp": None
        },
        "totals": {
            "claude_md_tokens": 0,
            "skills_tokens": 0,
            "commands_tokens": 0,
            "agents_tokens": 0,
            "hooks_tokens": 0,
            "mcp_tokens": 0,
            "total_project_tokens": 0
        },
        "estimates": {
            # System prompt varies by enabled features:
            # Base: ~8k | +Web search: 1.5k | +MCP servers: 0.5-2k each
            # +Computer use: 2k | +Memory: 0.5k → Range: 8k-20k+
            "system_prompt_tokens": 10000,  # Conservative baseline estimate
            "baseline_total": 0
        }
    }
    
    # Analyze each component type
    for claude_md in configs["claude_md"]:
        analysis = analyze_file(claude_md)
        results["components"]["claude_md"].append(analysis)
        if "tokens" in analysis:
            results["totals"]["claude_md_tokens"] += analysis["tokens"]
    
    for skill in configs["skills"]:
        analysis = analyze_file(skill)
        results["components"]["skills"].append(analysis)
        if "tokens" in analysis:
            results["totals"]["skills_tokens"] += analysis["tokens"]
    
    for cmd in configs["commands"]:
        analysis = analyze_file(cmd)
        results["components"]["commands"].append(analysis)
        if "tokens" in analysis:
            results["totals"]["commands_tokens"] += analysis["tokens"]
    
    for agent in configs["agents"]:
        analysis = analyze_file(agent)
        results["components"]["agents"].append(analysis)
        if "tokens" in analysis:
            results["totals"]["agents_tokens"] += analysis["tokens"]
    
    for hooks in configs["hooks"]:
        analysis = analyze_file(hooks)
        results["components"]["hooks"].append(analysis)
        if "tokens" in analysis:
            results["totals"]["hooks_tokens"] += analysis["tokens"]
    
    if configs["mcp_config"]:
        analysis = analyze_file(configs["mcp_config"])
        results["components"]["mcp"] = analysis
        if "tokens" in analysis:
            results["totals"]["mcp_tokens"] = analysis["tokens"]
    
    # Calculate totals
    results["totals"]["total_project_tokens"] = (
        results["totals"]["claude_md_tokens"] +
        results["totals"]["skills_tokens"] +
        results["totals"]["commands_tokens"] +
        results["totals"]["agents_tokens"] +
        results["totals"]["hooks_tokens"] +
        results["totals"]["mcp_tokens"]
    )
    
    results["estimates"]["baseline_total"] = (
        results["estimates"]["system_prompt_tokens"] +
        results["totals"]["total_project_tokens"]
    )
    
    return results


def analyze_files(filepaths: list[str]) -> dict:
    """Analyze multiple specific files."""
    results = {
        "files": [],
        "total_tokens": 0,
        "total_lines": 0,
        "tiktoken_available": TIKTOKEN_AVAILABLE
    }
    
    for filepath in filepaths:
        analysis = analyze_file(filepath)
        results["files"].append(analysis)
        if "tokens" in analysis:
            results["total_tokens"] += analysis["tokens"]
        if "lines" in analysis:
            results["total_lines"] += analysis["lines"]
    
    return results


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Memento - Context Token Analyzer for Claude Code"
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Specific files to analyze (if none, analyzes project context)"
    )
    parser.add_argument(
        "--project", "-p",
        default=".",
        help="Project root directory (default: current directory)"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output raw JSON"
    )
    parser.add_argument(
        "--budget", "-b",
        type=int,
        default=200000,
        help="Context window budget in tokens (default: 200000)"
    )
    
    args = parser.parse_args()
    
    if args.files:
        results = analyze_files(args.files)
    else:
        results = analyze_project(args.project)
        results["budget"] = args.budget
        results["budget_remaining"] = args.budget - results["estimates"]["baseline_total"]
        results["budget_used_percent"] = round(
            (results["estimates"]["baseline_total"] / args.budget) * 100, 1
        )
    
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
