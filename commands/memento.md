---
description: "What do I know?" — Analyze current project context and token usage. Like Leonard's condition, your context window has limits.
---

# Memento — Context Analysis

*"I have to believe in a world outside my own mind."*

Analyze the token usage of your Claude Code project configuration to understand your memory constraints.

## Instructions

1. First, check if tiktoken is available for accurate token counting:
   ```bash
   python3 -c "import tiktoken" 2>/dev/null && echo "tiktoken available" || echo "tiktoken not found - will use estimates"
   ```

2. Run the Memento token analyzer:
   ```bash
   python3 "$(dirname "$(which claude)")/../plugins/memento/scripts/count-tokens.py" --project . 2>/dev/null || python3 ~/.claude/plugins/*/memento/scripts/count-tokens.py --project . 2>/dev/null || python3 .claude/plugins/memento/scripts/count-tokens.py --project .
   ```

3. Parse the JSON output and present results in this format:

```
╭─────────────────────────────────────────────────────────────────╮
│  MEMENTO — "Remember Sammy Jankis"                              │
│  Context Token Analysis                                         │
╰─────────────────────────────────────────────────────────────────╯

📸 THE POLAROIDS (What's Always Loaded)
┌─────────────────────────────────────────────────────────────────┐
│ Component              │ Tokens    │ Files │ Notes             │
├────────────────────────┼───────────┼───────┼───────────────────┤
│ System Prompt          │ ~12,000   │   -   │ (estimated)       │
│ CLAUDE.md files        │   X,XXX   │   X   │                   │
│ Skills                 │   X,XXX   │   X   │ load on-demand    │
│ Commands               │   X,XXX   │   X   │ metadata only     │
│ Agents                 │   X,XXX   │   X   │                   │
│ Hooks                  │     XXX   │   X   │                   │
│ MCP Tool Schemas       │     XXX   │   1   │                   │
├────────────────────────┼───────────┼───────┼───────────────────┤
│ BASELINE TOTAL         │  XX,XXX   │       │                   │
└─────────────────────────────────────────────────────────────────┘

🧠 THE CONDITION (Your Memory Budget)
┌─────────────────────────────────────────────────────────────────┐
│ Model Context Window   │ 200,000 tokens                        │
│ Baseline Used          │  XX,XXX tokens (XX.X%)                │
│ Available for Work     │ XXX,XXX tokens                        │
│ ████████░░░░░░░░░░░░░░ │ XX% used                              │
└─────────────────────────────────────────────────────────────────┘

⚠️  TATTOOS (Permanent Memory — Largest Consumers)
   1. [filename]              X,XXX tokens  ← Consider splitting
   2. [filename]              X,XXX tokens
   3. [filename]              X,XXX tokens

💡 LEONARD'S NOTES
   • Skills load on-demand — move large CLAUDE.md sections there
   • Use @file:1-50 line ranges to reduce file token costs
   • Run /memento:polaroid @file before adding large files
   • Run /memento:burn to get optimization recommendations
```

4. If tiktoken is not available, add a note:
   ```
   ⚠️  Token counts are estimates (install tiktoken for accuracy):
       pip install tiktoken
   ```

5. If any single file exceeds 3,000 tokens, flag it with:
   ```
   🔴 [filename] is X,XXX tokens — consider splitting into skills
   ```

$ARGUMENTS may contain:
- `--json` — Output raw JSON instead of formatted display
- `--detailed` — Show all files, not just top consumers
