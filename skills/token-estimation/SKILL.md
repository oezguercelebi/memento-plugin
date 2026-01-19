---
description: Token counting and context estimation expertise. Use when analyzing file sizes, estimating token costs, or planning context budgets for Claude Code sessions.
---

# Token Estimation Skill

## Quick Reference

### Token Estimates by File Type

| File Type | Avg Tokens/Line | Notes |
|-----------|-----------------|-------|
| TypeScript/JavaScript | 12-15 | Higher due to type annotations |
| Python | 10-12 | Clean syntax, fewer tokens |
| Go/Rust | 11-14 | Verbose but structured |
| Markdown | 8-10 | Natural language |
| JSON | 15-20 | High token density |
| YAML | 10-12 | Similar to Markdown |

### Context Budget Guidelines

| Component | Typical Size | Recommendation |
|-----------|--------------|----------------|
| System prompt | ~12,000 | Fixed, cannot change |
| CLAUDE.md (project) | 500-2,000 | Keep under 2,000 |
| CLAUDE.md (user) | 500-1,000 | Keep minimal |
| Skills (each) | 500-3,000 | Load on-demand |
| Commands (each) | 100-500 | Metadata only |
| Agents (each) | 500-2,000 | Metadata only |
| MCP schemas | 200-1,000 | Per server |

### Optimal Baseline Targets

| Rating | Baseline | % of 200k |
|--------|----------|-----------|
| Excellent | <15,000 | <7.5% |
| Good | 15-25,000 | 7.5-12.5% |
| Fair | 25-35,000 | 12.5-17.5% |
| Poor | 35-50,000 | 17.5-25% |
| Critical | >50,000 | >25% |

### Token Counting Methods

**Accurate (requires tiktoken)**:
```python
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
tokens = len(enc.encode(text))
```

**Estimation (no dependencies)**:
```python
# Rough estimate: ~4 chars per token for code
tokens = len(text) // 4

# Better estimate with line awareness
lines = text.count('\n') + 1
tokens = (len(text) // 4) + (lines * 2)  # Account for newlines
```

### Claude Code Context Sources

**Always Loaded (Tattoos)**:
1. System prompt (~12k, fixed)
2. User CLAUDE.md (`~/.claude/CLAUDE.md`)
3. Project CLAUDE.md (`./CLAUDE.md`, `./.claude/CLAUDE.md`)
4. Command descriptions (metadata only)
5. Agent descriptions (metadata only)
6. Enabled plugin metadata
7. MCP tool schemas

**On-Demand (Polaroids)**:
1. Skills (`.claude/skills/*/SKILL.md`) — loaded when relevant
2. @-mentioned files — loaded per request
3. Tool outputs — loaded during execution

### Optimization Strategies

**High Impact**:
1. Move CLAUDE.md sections to skills (saves 70%+ of those tokens)
2. Use line ranges instead of full files (@file:1-50)
3. Disable unused plugins

**Medium Impact**:
1. Consolidate similar agents
2. Use skills over detailed CLAUDE.md
3. Reference files instead of embedding content

**Low Impact**:
1. Trim verbose descriptions
2. Remove outdated context
3. Shorten command descriptions

### Line Range Estimation

For suggesting line ranges:
```
Full file: 2,340 tokens (156 lines) = 15 tokens/line

Suggested ranges:
- Lines 1-50:   ~750 tokens (imports, types)
- Lines 50-100: ~750 tokens (main logic)
- Lines 100-156: ~840 tokens (exports, utils)
```

### Budget Planning Formula

```
Available = Budget - Baseline - Conversation_Buffer

Where:
- Budget = Model context window (200,000)
- Baseline = Sum of all always-loaded context
- Conversation_Buffer = Reserve for back-and-forth (~20-30%)

Recommended working budget:
- Conservative: 50,000 tokens for files
- Standard: 100,000 tokens for files  
- Aggressive: 150,000 tokens for files
```
