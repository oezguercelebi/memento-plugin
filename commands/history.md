---
description: "The facts, not the memory." — View token usage trends across past sessions.
---

# Memento — Session History

*"I have to believe in a world outside my own mind. I have to believe that my actions still have meaning."*

Display token usage history and trends across your Claude Code sessions.

## Instructions

1. Read the session history file:
   ```bash
   cat ~/.claude/memento-stats.json 2>/dev/null || echo '{"sessions":[]}'
   ```

2. Parse the JSON and present results in this format:

```
╭─────────────────────────────────────────────────────────────────╮
│  MEMENTO — "The Facts, Not the Memory"                          │
│  Session History Analysis                                        │
╰─────────────────────────────────────────────────────────────────╯

📜 RECENT SESSIONS (Last 10)
┌───────────────┬────────────────┬──────────┬──────────┬────────────┐
│ Date          │ Project        │ Start    │ End      │ Duration   │
├───────────────┼────────────────┼──────────┼──────────┼────────────┤
│ 2026-01-19    │ memento        │ 15,000   │ 45,000   │ 45 min     │
│ 2026-01-18    │ my-app         │ 12,000   │ 180,000  │ 2.5 hrs    │
│ ...           │                │          │          │            │
└───────────────┴────────────────┴──────────┴──────────┴────────────┘

📊 USAGE TRENDS
┌─────────────────────────────────────────────────────────────────┐
│ Total Sessions Tracked    │ XX sessions                        │
│ Average Session Duration  │ XX minutes                         │
│ Average Tokens Consumed   │ XX,XXX tokens/session              │
│ Token Growth Rate         │ ~XXX tokens/minute                 │
│ Sessions Near Limit       │ X/XX (XX%)   [>150k tokens]        │
└─────────────────────────────────────────────────────────────────┘

📈 PROJECT BREAKDOWN
   • memento-plugin    │ 5 sessions │ avg 35,000 tokens
   • my-other-project  │ 3 sessions │ avg 82,000 tokens

⚠️  PATTERN ALERTS
   • Project "my-app" frequently hits token limits
   • Morning sessions tend to be 40% longer

💡 LEONARD'S NOTES
   • Use /memento before starting heavy sessions
   • Consider splitting large projects into focused sessions
   • Your context grows ~500 tokens/minute on average
```

3. Calculate statistics from the session data:
   - **Total sessions**: Count of all recorded sessions
   - **Average duration**: Mean of `duration_minutes` across sessions
   - **Average tokens consumed**: Mean of `(final_tokens - baseline_tokens)`
   - **Token growth rate**: Average `(final_tokens - baseline_tokens) / duration_minutes`
   - **Sessions near limit**: Count where `final_tokens > 150000`

4. Group sessions by project name for the breakdown section.

5. If no sessions are recorded yet:
   ```
   ╭─────────────────────────────────────────────────────────────────╮
   │  MEMENTO — "The Facts, Not the Memory"                          │
   │  Session History Analysis                                        │
   ╰─────────────────────────────────────────────────────────────────╯

   📭 NO SESSIONS RECORDED YET

   Session tracking is enabled via hooks. Your first session will be
   logged automatically when you start and stop Claude Code.

   💡 To verify hooks are active:
      • Check ~/.claude/settings.json includes memento hooks
      • Or manually test: python3 <plugin>/scripts/log-session.py --event start -p .
   ```

6. If the stats file doesn't exist or is empty, show the "no sessions" message.

$ARGUMENTS may contain:
- `--last N` — Show only last N sessions (default: 10)
- `--project NAME` — Filter to sessions for specific project
- `--json` — Output raw JSON data instead of formatted display
