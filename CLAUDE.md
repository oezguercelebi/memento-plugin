# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Memento is a Claude Code plugin that helps users manage their context window and token usage. It provides visibility into token consumption, previews token costs before adding files, and offers optimization recommendations. The project uses the film *Memento* as its conceptual framework throughout.

## Running Token Analysis

```bash
# Analyze entire project
python3 scripts/count-tokens.py --project .

# Analyze specific files
python3 scripts/count-tokens.py [filepath1] [filepath2]

# JSON output for parsing
python3 scripts/count-tokens.py --project . --json
```

Requires Python 3.8+. tiktoken library is optional but recommended for accurate counts.

## Architecture

### Plugin Structure
- **`.claude-plugin/plugin.json`** - Plugin manifest defining version and metadata
- **`commands/`** - Claude Code slash commands (invoked as `/memento`, `/memento:polaroid`, etc.)
- **`agents/leonard.md`** - Context optimization specialist agent
- **`skills/token-estimation/SKILL.md`** - Token counting reference loaded on-demand
- **`scripts/count-tokens.py`** - Python backend for all token analysis

### Command Files
Each command is a markdown file with YAML frontmatter:
```yaml
---
description: "User-facing description"
---
```
Commands reference the token script at `~/.claude/plugins/*/memento/scripts/count-tokens.py`.

### Metaphor System
| Term | Meaning |
|------|---------|
| Tattoos | Always-loaded context (system prompt, CLAUDE.md) |
| Polaroids | On-demand context (@-files, skills) |
| The Condition | 200k token context limit |

### Token Budget Constants
- System prompt: ~8-15k tokens (varies by enabled features)
- Target baseline: <15k tokens (Excellent)
- Warning threshold: >50k tokens (Critical)
- Context limit: 200k tokens

### Python Script (`count-tokens.py`)
- Dual-mode: tiktoken (accurate) or estimation (~4 chars/token)
- Discovers Claude Code configs (CLAUDE.md, skills, commands, agents, hooks, MCP)
- Outputs JSON with component breakdown and totals
