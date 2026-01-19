---
description: "Burn the evidence" — Get recommendations for reducing token usage. Identify what memories to destroy.
---

# Memento — Burn (Optimize Context)

*"I'm not a killer. I'm just someone who wanted to make things right."*

Analyze your context and recommend what to burn — what to remove, split, or optimize to stay under rate limits.

## Instructions

1. Run full context analysis:
   ```bash
   python3 ~/.claude/plugins/*/memento/scripts/count-tokens.py --project .
   ```

2. Also analyze the content of large files for optimization opportunities:
   ```bash
   # For each CLAUDE.md file, look for:
   # - Duplicate information
   # - Sections that could be skills
   # - Verbose explanations
   # - Outdated information
   ```

3. Generate prioritized recommendations:

```
╭─────────────────────────────────────────────────────────────────╮
│  MEMENTO — Burn                                                 │
│  "I have to believe that when my eyes are closed,               │
│   the world's still there."                                     │
╰─────────────────────────────────────────────────────────────────╯

📊 CURRENT STATE
   Baseline: XX,XXX tokens (XX% of budget)
   Target:   <15,000 tokens (<8% of budget) for optimal performance

🔴 HIGH IMPACT — Burn These First (save 5,000+ tokens)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. SPLIT LARGE CLAUDE.md INTO SKILLS
   
   File: ./CLAUDE.md (8,500 tokens)
   
   Problem: Large CLAUDE.md files are tattooed on every conversation,
            even when that context isn't needed.
   
   Solution: Move domain-specific sections to skills/
   
   Before:
   └── CLAUDE.md (8,500 tokens) ← always loaded
   
   After:
   ├── CLAUDE.md (1,500 tokens) ← always loaded
   └── skills/
       ├── api-patterns/SKILL.md (2,500 tokens) ← on-demand
       ├── database-schema/SKILL.md (2,000 tokens) ← on-demand
       └── testing-guidelines/SKILL.md (2,500 tokens) ← on-demand
   
   Savings: ~7,000 tokens (skills load only when relevant)
   
   To implement:
   ```bash
   mkdir -p .claude/skills/api-patterns
   # Move API-related sections to .claude/skills/api-patterns/SKILL.md
   ```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟡 MEDIUM IMPACT — Consider Burning (save 1,000-5,000 tokens)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2. CONSOLIDATE SIMILAR AGENTS
   
   Found: 3 agents with overlapping instructions
   - code-reviewer.md (1,200 tokens)
   - pr-reviewer.md (1,100 tokens)  
   - quality-checker.md (900 tokens)
   
   Solution: Merge into single configurable agent
   
   Savings: ~2,100 tokens

3. REMOVE DUPLICATE CONTEXT
   
   Found: Same information in multiple places
   - Project description in CLAUDE.md AND README.md reference
   - API endpoints listed in CLAUDE.md AND in comments
   
   Solution: Single source of truth, reference don't repeat
   
   Savings: ~1,500 tokens

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟢 LOW IMPACT — Nice to Have (save <1,000 tokens)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4. TRIM VERBOSE COMMAND DESCRIPTIONS
   
   Found: 5 commands with >500 token descriptions
   
   Solution: Concise descriptions, move details to command body
   
   Savings: ~800 tokens

5. DISABLE UNUSED PLUGINS
   
   Found: 3 plugins that haven't been used in this project
   
   Solution: /plugin disable [plugin-name]
   
   Savings: ~500 tokens

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 PROJECTED RESULTS
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Current:  XX,XXX tokens  ████████████████░░░░  XX%            │
│  After:    ~X,XXX tokens  ████░░░░░░░░░░░░░░░░  X%             │
│                                                                 │
│  Potential savings: ~XX,XXX tokens                              │
│  More room for: ~XXX files @ 1k tokens average                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

💡 LEONARD'S FINAL NOTE
   "We all lie to ourselves to be happy."
   
   But your token counter doesn't lie.
   Burn what you don't need. Keep what matters.
```

4. For each recommendation, check if it's actionable:
   - Can the user actually make this change?
   - Provide specific file paths and commands
   - Estimate effort (easy/medium/hard)

5. If context is already optimal (<10,000 tokens), congratulate:
   ```
   ✅ YOUR MEMORY IS OPTIMIZED
   
   Baseline: X,XXX tokens (X% of budget)
   
   "The world doesn't just disappear when you close your eyes."
   Your context is lean. You have room to work.
   ```
