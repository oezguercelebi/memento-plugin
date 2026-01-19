---
description: "Take a Polaroid" — Preview token cost before adding files to context. Don't trust your memory, trust the photo.
---

# Memento — Polaroid (Preview Files)

*"We all need mirrors to remind ourselves who we are."*

Preview how many tokens files will consume BEFORE adding them to context.
Like Leonard's Polaroids, this shows you what you're about to commit to memory.

## Instructions

1. Parse $ARGUMENTS for file paths. Accept formats like:
   - `@src/api/routes.ts`
   - `src/api/routes.ts`
   - Multiple files: `@file1.ts @file2.ts @file3.ts`
   - Glob patterns: `src/**/*.ts` (expand first)

2. For each file, get token count:
   ```bash
   python3 ~/.claude/plugins/*/memento/scripts/count-tokens.py [filepath1] [filepath2] ...
   ```

3. Also get current baseline for comparison:
   ```bash
   python3 ~/.claude/plugins/*/memento/scripts/count-tokens.py --project .
   ```

4. Present results:

```
╭─────────────────────────────────────────────────────────────────╮
│  MEMENTO — Polaroid                                             │
│  "Taking a picture so I won't forget"                           │
╰─────────────────────────────────────────────────────────────────╯

📸 FILES TO ADD
┌─────────────────────────────────────────────────────────────────┐
│ File                          │ Tokens  │ Lines │ Tok/Line     │
├───────────────────────────────┼─────────┼───────┼──────────────┤
│ src/api/routes.ts             │  2,340  │  156  │  15.0        │
│ src/api/middleware.ts         │    890  │   62  │  14.4        │
│ src/types/index.ts            │    450  │   38  │  11.8        │
├───────────────────────────────┼─────────┼───────┼──────────────┤
│ TOTAL                         │  3,680  │  256  │              │
└─────────────────────────────────────────────────────────────────┘

🧠 IMPACT ON YOUR CONDITION
┌─────────────────────────────────────────────────────────────────┐
│ Current baseline         │  15,000 tokens                      │
│ After adding these       │  18,680 tokens  (+24.5%)            │
│ Remaining budget         │ 181,320 tokens                      │
│ ████████░░░░░░░░░░░░░░░░ │  9.3% of budget                     │
└─────────────────────────────────────────────────────────────────┘

💡 LEONARD'S NOTES
```

5. For large files (>2000 tokens), suggest line ranges:
   ```
   💡 TIP: src/api/routes.ts is 2,340 tokens
      Consider using line ranges:
      • @src/api/routes.ts:1-50    → ~750 tokens (just imports & types)
      • @src/api/routes.ts:50-100  → ~750 tokens (main handlers)
   ```

6. For binary or unreadable files:
   ```
   ⚠️  [filename] — Cannot analyze (binary file)
   ```

7. If no files specified:
   ```
   Usage: /memento:polaroid @file1 @file2 ...
   
   Example:
     /memento:polaroid @src/index.ts @src/utils.ts
     /memento:polaroid src/**/*.ts
   ```
