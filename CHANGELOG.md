# Changelog

All notable changes to Memento will be documented in this file.

## [1.0.0] - 2025-01-19

### Added

**Core Plugin**
- Plugin manifest with metadata and configuration
- Python token counting backend with tiktoken support (falls back to estimation)
- Leonard agent for context optimization assistance

**Commands**

- `/memento` — Analyze current project context and token usage with detailed breakdown
- `/memento:polaroid` — Preview token cost before adding files to context
- `/memento:tattoo` — Show permanently loaded context (system prompt, CLAUDE.md, plugins)
- `/memento:burn` — Get prioritized recommendations for reducing token usage
- `/memento:case` — Full investigation with efficiency scoring and "what-if" scenarios
- `/memento:budget` — Plan file loading within a specific token budget

**Features**
- Visual token budget displays with progress bars
- Efficiency scoring system (Excellent to Critical)
- Smart recommendations for moving content to skills
- Line range suggestions for large files
- Copy-paste ready file lists for budget planning
- JSON output mode for programmatic use

**Metaphor System**
- *Tattoos*: Always-loaded context (system prompt, CLAUDE.md)
- *Polaroids*: On-demand context (@-files, skills)
- *The Condition*: 200k token context limit

### Technical Details
- Discovers Claude Code configs automatically (CLAUDE.md, skills, commands, agents, hooks, MCP)
- Dual-mode counting: tiktoken (accurate) or character estimation (~4 chars/token)
- Token budget constants: 12k system prompt, 15k excellent baseline, 50k critical threshold
