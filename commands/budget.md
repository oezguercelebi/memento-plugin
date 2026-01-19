---
description: "Plan within your condition" — Calculate how many files you can add within a token budget. Know your limits.
---

# Memento — Budget (Token Budget Planner)

*"I have this condition..."*

Plan your context within a specific token budget. Know exactly what you can load before you hit the wall.

## Instructions

1. Parse $ARGUMENTS for:
   - Budget number (e.g., `50000` for 50k tokens)
   - Optional: `--files src/` to analyze specific directory
   - Optional: `--priority large|small|balanced`

2. Resolve the Memento script path and get current baseline:
   ```bash
   # Script discovery: tries paths in order until one succeeds
   MEMENTO_SCRIPT=$(
     for p in \
       ~/.claude/plugins/memento/scripts/count-tokens.py \
       .claude/plugins/memento/scripts/count-tokens.py \
       ./scripts/count-tokens.py; do
       [ -f "$p" ] && echo "$p" && break
     done 2>/dev/null
   )
   [ -z "$MEMENTO_SCRIPT" ] && MEMENTO_SCRIPT=$(ls ~/.claude/plugins/*/memento/scripts/count-tokens.py 2>/dev/null | head -1)

   python3 "$MEMENTO_SCRIPT" --project .
   ```

3. If directory specified, analyze all files:
   ```bash
   find [directory] -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.md" \) -exec python3 "$MEMENTO_SCRIPT" {} +
   ```

4. Present budget planner:

```
╭─────────────────────────────────────────────────────────────────╮
│  MEMENTO — Budget Planner                                       │
│  "I have this condition..."                                     │
╰─────────────────────────────────────────────────────────────────╯

🎯 YOUR BUDGET
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Target Budget:         XX,XXX tokens                           │
│  Current Baseline:     -XX,XXX tokens                           │
│  ─────────────────────────────────                              │
│  Available for Files:   XX,XXX tokens                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

📊 WHAT CAN YOU FIT?
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Small files   (~500 tokens):    ~XX files                      │
│  Medium files  (~1,500 tokens):  ~XX files                      │
│  Large files   (~3,000 tokens):  ~XX files                      │
│  Extra large   (~5,000 tokens):  ~XX files                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

📁 FILES ANALYZED (from [directory])
┌─────────────────────────────────────────────────────────────────┐
│ File                                    │ Tokens │ Cumulative   │
├─────────────────────────────────────────┼────────┼──────────────┤
│ ✅ src/index.ts                         │    450 │      450     │
│ ✅ src/utils.ts                         │    820 │    1,270     │
│ ✅ src/api/routes.ts                    │  2,340 │    3,610     │
│ ✅ src/api/middleware.ts                │    890 │    4,500     │
│ ⚠️ src/api/handlers.ts                  │  3,200 │    7,700     │
│ ❌ src/services/database.ts             │  4,500 │   12,200     │
│ ❌ src/services/auth.ts                 │  3,800 │   16,000     │
│ ❌ ... (X more files not shown)         │        │              │
├─────────────────────────────────────────┼────────┼──────────────┤
│ FITS IN BUDGET (✅)                      │  X,XXX │              │
│ BORDERLINE (⚠️)                          │  X,XXX │              │
│ EXCEEDS BUDGET (❌)                      │  X,XXX │              │
└─────────────────────────────────────────────────────────────────┘

Legend:
  ✅ Fits within budget
  ⚠️ Fits but leaves <20% remaining
  ❌ Would exceed budget

💡 SMART RECOMMENDATIONS
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Best fit for XX,XXX token budget:                              │
│                                                                 │
│  Option A: Maximum Coverage (XX files, XX,XXX tokens)           │
│  ├── src/index.ts                                               │
│  ├── src/utils.ts                                               │
│  ├── src/api/routes.ts                                          │
│  └── src/api/middleware.ts                                      │
│                                                                 │
│  Option B: Core + Types (XX files, XX,XXX tokens)               │
│  ├── src/index.ts                                               │
│  ├── src/types/*.ts                                             │
│  └── src/api/routes.ts                                          │
│                                                                 │
│  Option C: Focused (XX files, XX,XXX tokens)                    │
│  └── @src/api/routes.ts:1-100 (just the relevant section)       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

📋 COPY-PASTE READY
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Add these files to your prompt:                                │
│                                                                 │
│  @src/index.ts @src/utils.ts @src/api/routes.ts                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

💭 LEONARD'S NOTE
   "I have to believe in a world outside my own mind."
   
   Stay within your budget. Leave room for conversation.
   A good rule: use <50% of budget for files, save rest for back-and-forth.
```

5. Default budget if not specified: 50,000 tokens (reasonable working budget)

6. If `--priority` specified:
   - `large`: Prioritize fewer large files (depth over breadth)
   - `small`: Prioritize many small files (breadth over depth)
   - `balanced`: Mix of both (default)

7. Usage examples in help:
   ```
   /memento:budget 30000                    # 30k token budget
   /memento:budget 50000 --files src/       # Analyze src/ for 50k budget
   /memento:budget 100000 --priority large  # Fit large files first
   ```
