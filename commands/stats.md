---
description: "Remember Sammy Jankis." — View command usage patterns and trends.
---

# Memento — Usage Stats

*"I have to believe in the world outside my own mind. I have to believe that what I do matters."*

Display command usage patterns and trends across your Claude Code sessions.

## Instructions

1. Read the command log file:
   ```bash
   cat ~/.claude/memento-commands.json 2>/dev/null || echo '{"commands":[]}'
   ```

2. Parse the JSON and present results in this format:

```
╭─────────────────────────────────────────────────────────────────╮
│  MEMENTO — "Remember Sammy Jankis"                              │
│  Command Usage Statistics                                        │
╰─────────────────────────────────────────────────────────────────╯

📊 COMMAND FREQUENCY (Top 10)
┌──────────────────────────────────────┬───────────┬───────────────┐
│ Command Pattern                       │ Count     │ Last Used     │
├──────────────────────────────────────┼───────────┼───────────────┤
│ git status                           │ 45        │ 2 min ago     │
│ npm run build                        │ 23        │ 15 min ago    │
│ pytest                               │ 18        │ 1 hr ago      │
│ npm test                             │ 12        │ 3 hrs ago     │
│ ...                                  │           │               │
└──────────────────────────────────────┴───────────┴───────────────┘

📁 PROJECT BREAKDOWN
┌────────────────────────────────────────────────────────────────┐
│ Project              │ Commands  │ Most Common                 │
├──────────────────────────────────────────────────────────────────┤
│ memento-plugin       │ 156       │ git status, npm test        │
│ my-app               │ 89        │ npm run build, pytest       │
└────────────────────────────────────────────────────────────────┘

⏰ ACTIVITY TIMELINE (Last 7 Days)
Mon  ████████████████████████░░░░░░  78 commands
Tue  ██████████████░░░░░░░░░░░░░░░░  45 commands
Wed  ██████████████████████████████  120 commands
Thu  ████████████████████░░░░░░░░░░  65 commands
Fri  ██████████░░░░░░░░░░░░░░░░░░░░  32 commands
Sat  ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░  8 commands
Sun  ████░░░░░░░░░░░░░░░░░░░░░░░░░░  15 commands

🔧 COMMAND CATEGORIES
   • git commands       │ 45% ████████████████████
   • build/test         │ 30% █████████████
   • file operations    │ 15% ██████
   • other              │ 10% ████

💡 LEONARD'S OBSERVATIONS
   • Peak activity: Wednesday afternoons
   • You run "git status" frequently - consider git aliases
   • Test commands make up 30% of activity (good coverage!)
```

3. Calculate statistics from the command data:
   - **Command frequency**: Group identical/similar commands and count occurrences
   - **Project breakdown**: Group by project field
   - **Activity timeline**: Group by day of week from timestamps
   - **Categories**: Classify commands (git, npm/yarn, pytest/jest, file ops, etc.)

4. Command pattern matching:
   - Normalize paths and arguments for grouping (e.g., `git commit -m "..."` → `git commit`)
   - Group similar commands together (all `npm test` variants)
   - Truncate long commands in display

5. If no commands are logged yet:
   ```
   ╭─────────────────────────────────────────────────────────────────╮
   │  MEMENTO — "Remember Sammy Jankis"                              │
   │  Command Usage Statistics                                        │
   ╰─────────────────────────────────────────────────────────────────╯

   📭 NO COMMANDS LOGGED YET

   Command tracking is enabled via the PostToolUse hook.
   Bash commands will be automatically logged as you work.

   💡 To verify:
      • Check hooks are active in ~/.claude/settings.json
      • Run any bash command and check ~/.claude/memento-commands.json
   ```

6. If the commands file doesn't exist or is empty, show the "no commands" message.

$ARGUMENTS may contain:
- `--last N` — Show stats for only last N commands (default: all)
- `--project NAME` — Filter to commands from specific project
- `--json` — Output raw JSON data instead of formatted display
