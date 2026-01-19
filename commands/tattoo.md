---
description: "The facts I choose to tattoo" — Show what's ALWAYS loaded into context. These are your permanent memories.
---

# Memento — Tattoo (Permanent Context)

*"I have to believe in a world outside my own mind. I have to believe that my actions still have meaning."*

Show all context that is ALWAYS loaded — your tattoos, the facts you've chosen to permanently remember.

## Instructions

1. Identify all "permanent" context sources:
   - System prompt (always present, ~12k tokens estimated)
   - User-level CLAUDE.md (`~/.claude/CLAUDE.md`)
   - Project-level CLAUDE.md (`./CLAUDE.md` or `./.claude/CLAUDE.md`)
   - User-level settings
   - Enabled plugins (command metadata, not full content)
   - MCP server tool schemas

2. Run analysis:
   ```bash
   python3 ~/.claude/plugins/*/memento/scripts/count-tokens.py --project .
   ```

3. Present results showing the hierarchy:

```
╭─────────────────────────────────────────────────────────────────╮
│  MEMENTO — Tattoos                                              │
│  "These are the facts. Write them down."                        │
╰─────────────────────────────────────────────────────────────────╯

🔒 SYSTEM TATTOOS (Cannot be removed)
┌─────────────────────────────────────────────────────────────────┐
│ Claude System Prompt                         ~12,000 tokens     │
│ ├── Core instructions                                           │
│ ├── Tool definitions                                            │
│ ├── Safety guidelines                                           │
│ └── Feature-specific context                                    │
└─────────────────────────────────────────────────────────────────┘

🏠 USER TATTOOS (~/.claude/)
┌─────────────────────────────────────────────────────────────────┐
│ ~/.claude/CLAUDE.md                           X,XXX tokens      │
│ ~/.claude/settings.json                         XXX tokens      │
│ Global commands (X files)                       XXX tokens      │
│ Global agents (X files)                         XXX tokens      │
└─────────────────────────────────────────────────────────────────┘

📁 PROJECT TATTOOS (./.claude/)
┌─────────────────────────────────────────────────────────────────┐
│ ./CLAUDE.md                                   X,XXX tokens      │
│ ./.claude/CLAUDE.md                           X,XXX tokens      │
│ Project commands (X files)                      XXX tokens      │
│ Project agents (X files)                        XXX tokens      │
│ MCP server schemas                              XXX tokens      │
└─────────────────────────────────────────────────────────────────┘

🔌 PLUGIN TATTOOS (Enabled plugins)
┌─────────────────────────────────────────────────────────────────┐
│ memento                                         XXX tokens      │
│ [other-plugin]                                  XXX tokens      │
│ (command/agent descriptions only)                               │
└─────────────────────────────────────────────────────────────────┘

📊 TATTOO SUMMARY
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Total Permanent Context:  XX,XXX tokens                        │
│                                                                 │
│  ████████████░░░░░░░░░░░  XX% of 200k budget                   │
│                                                                 │
│  This is loaded EVERY conversation.                             │
│  Everything else is temporary — like Leonard's Polaroids.       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

💡 UNLIKE POLAROIDS, TATTOOS CAN'T BE REMOVED MID-CONVERSATION
   To reduce tattoo burden:
   • Move CLAUDE.md sections to skills/ (load on-demand)
   • Disable unused plugins with /plugin
   • Keep CLAUDE.md under 2,000 tokens
```

4. Flag any tattoo over 3,000 tokens:
   ```
   🔴 WARNING: ./CLAUDE.md is X,XXX tokens
      This is tattooed on EVERY conversation.
      Consider moving sections to skills/ for on-demand loading.
   ```

5. Show which tattoos are user-controlled vs system-controlled:
   - 🔒 System = Cannot change
   - 🏠 User = Edit in ~/.claude/
   - 📁 Project = Edit in ./.claude/
