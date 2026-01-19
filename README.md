# Memento

> *"I have to believe in a world outside my own mind."*

**Context simulator and token optimizer for Claude Code.**

Know exactly what you're loading before you hit rate limits. Like Leonard Shelby in *Memento*, your context window has limits — and you need a system to work within them.

## The Problem

Claude Code users consistently hit rate limits because they don't know:
- How many tokens their CLAUDE.md files consume
- What's always loaded vs. on-demand
- How much room they have for files
- What to optimize first

**Memento solves this.** Preview token costs before committing, understand your baseline, and optimize for maximum efficiency.

## Installation

```bash
# Add the marketplace (if not already added)
/plugin marketplace add [your-github-username]/memento

# Install the plugin
/plugin install memento
```

Or install directly from GitHub:
```bash
/plugin install memento@[your-github-username]/memento
```

## Commands

| Command | Description |
|---------|-------------|
| `/memento` | "What do I know?" — Full context analysis |
| `/memento:polaroid` | Preview token cost of adding files |
| `/memento:tattoo` | Show always-loaded context |
| `/memento:burn` | Get optimization recommendations |
| `/memento:case` | Deep investigation with efficiency score |
| `/memento:budget` | Plan files within a token budget |

## Quick Start

### 1. Check your baseline
```
/memento
```
See how many tokens are consumed before you even start typing.

### 2. Preview before adding files
```
/memento:polaroid @src/api/routes.ts @src/types/index.ts
```
Know the cost before committing files to context.

### 3. Get optimization tips
```
/memento:burn
```
Prioritized recommendations for reducing token usage.

### 4. Plan within a budget
```
/memento:budget 50000 --files src/
```
See which files fit within a 50k token budget.

## The Memento Metaphor

Like Leonard in the film, Claude Code has a "condition" — limited memory (context window).

| Film Concept | Claude Code Equivalent |
|--------------|------------------------|
| **Tattoos** | Always-loaded context (CLAUDE.md, system prompt) |
| **Polaroids** | On-demand context (skills, @-mentioned files) |
| **Notes** | Conversation history |
| **The Condition** | 200k token context limit |

Leonard's system:
- Tattoo the important facts (permanent)
- Polaroids for temporary references
- Keep notes organized
- Work within the condition

Your system:
- Keep CLAUDE.md lean (< 2k tokens)
- Move domain knowledge to skills (on-demand)
- Preview files before adding
- Know your budget

## Example Output

```
╭─────────────────────────────────────────────────────────────────╮
│  MEMENTO — "Remember Sammy Jankis"                              │
│  Context Token Analysis                                         │
╰─────────────────────────────────────────────────────────────────╯

📸 THE POLAROIDS (What's Always Loaded)
┌─────────────────────────────────────────────────────────────────┐
│ Component              │ Tokens    │ Files │ Notes             │
├────────────────────────┼───────────┼───────┼───────────────────┤
│ System Prompt          │ ~8-15k    │   -   │ (varies by setup) │
│ CLAUDE.md files        │   3,240   │   2   │                   │
│ Skills                 │   4,500   │   3   │ load on-demand    │
│ Commands               │     450   │   5   │ metadata only     │
│ Agents                 │     800   │   2   │                   │
├────────────────────────┼───────────┼───────┼───────────────────┤
│ BASELINE TOTAL         │  16,490   │       │                   │
└─────────────────────────────────────────────────────────────────┘

🧠 THE CONDITION (Your Memory Budget)
┌─────────────────────────────────────────────────────────────────┐
│ Model Context Window   │ 200,000 tokens                        │
│ Baseline Used          │  16,490 tokens (8.2%)                 │
│ Available for Work     │ 183,510 tokens                        │
│ ████░░░░░░░░░░░░░░░░░░ │ 8% used                               │
└─────────────────────────────────────────────────────────────────┘
```

## Dependencies

**Required:**
- Python 3.8+

**Optional (recommended):**
- tiktoken (`pip install tiktoken`) — For accurate token counting

Without tiktoken, Memento uses estimation (~4 chars per token).

## Components

```
memento/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── commands/
│   ├── memento.md           # Main analysis command
│   ├── polaroid.md          # Preview file additions
│   ├── tattoo.md            # Show permanent context
│   ├── burn.md              # Optimization recommendations
│   ├── case.md              # Full investigation
│   └── budget.md            # Budget planner
├── agents/
│   └── leonard.md           # Optimization specialist agent
├── skills/
│   └── token-estimation/
│       └── SKILL.md         # Token counting expertise
├── scripts/
│   └── count-tokens.py      # Python token analyzer
└── README.md
```

## Philosophy

> *"We all need mirrors to remind ourselves who we are."*

This plugin is your mirror for context management. It doesn't change how Claude works — it shows you what's happening so you can make informed decisions.

**Core principles:**
1. **Visibility** — Know exactly what's consuming tokens
2. **Prevention** — Preview costs before committing
3. **Optimization** — Actionable recommendations, not just reports
4. **Education** — Understand the system, don't just follow rules

## Contributing

Found a bug? Have a suggestion?

1. Open an issue
2. Submit a PR
3. Share your optimization tips

## Feedback

Which command do you use most?
- 👍 React on [this discussion](link) for /memento
- 🎉 React for /memento:polaroid
- ❤️ React for /memento:burn
- 🚀 React for /memento:budget

## License

MIT

---

*"Don't believe his lies."* — But believe your token counter.
