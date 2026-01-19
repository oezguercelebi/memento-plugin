# Memento Plugin Tests

Test suite for verifying `count-tokens.py` accuracy and plugin functionality.

## Quick Start

```bash
# Run all tests
python3 tests/test_count_tokens.py

# Install tiktoken for accurate testing (recommended)
pip install tiktoken
```

## Test Structure

```
tests/
├── test_count_tokens.py          # Main test script
├── fixtures/
│   ├── known-sizes/              # Files with verified token counts
│   │   ├── empty.txt             # 0 tokens
│   │   ├── single-word.txt       # 1 token
│   │   ├── ten-words.txt         # 10 tokens
│   │   ├── simple-code.py        # 23 tokens
│   │   ├── simple-markdown.md    # 39 tokens
│   │   └── simple-json.json      # 39 tokens
│   └── sample-project/           # Mock project for /memento testing
│       ├── CLAUDE.md
│       └── .claude/
│           ├── skills/sample-skill/SKILL.md
│           ├── commands/sample-command.md
│           ├── agents/sample-agent.md
│           └── hooks.json
└── README.md
```

## Test Categories

### Token Count Tests
Verifies that `count-tokens.py` returns accurate token counts for files with known sizes.

- **With tiktoken**: Expects exact matches
- **Without tiktoken**: Allows 25% tolerance for estimation

### Metadata Tests
Verifies correct line and byte counts for all test files.

### Multi-file Tests
Verifies analyzing multiple files simultaneously.

### Error Handling Tests
Verifies graceful handling of:
- Nonexistent files
- Permission errors
- Binary files

### Project Analysis Tests
Verifies the `--project` flag correctly:
- Discovers CLAUDE.md files
- Finds skills in `.claude/skills/`
- Finds commands in `.claude/commands/`
- Finds agents in `.claude/agents/`
- Calculates budget remaining

### Parameter Tests
Verifies CLI parameters:
- `--budget` custom budget
- `--json` output format
- `tiktoken_available` flag

## Expected Token Counts

All counts verified using tiktoken with `cl100k_base` encoding:

| File | Tokens | Bytes | Lines |
|------|--------|-------|-------|
| empty.txt | 0 | 0 | 0 |
| single-word.txt | 1 | 5 | 1 |
| ten-words.txt | 10 | 48 | 1 |
| simple-code.py | 23 | 87 | 5 |
| simple-markdown.md | 39 | 143 | 15 |
| simple-json.json | 39 | 84 | 6 |

## Adding New Tests

1. Add test files to `fixtures/known-sizes/`
2. Calculate expected tokens: `python3 -c "import tiktoken; enc = tiktoken.get_encoding('cl100k_base'); print(len(enc.encode(open('file').read())))"`
3. Add expectations to `EXPECTED_TOKENS` and `EXPECTED_METADATA` in `test_count_tokens.py`
4. Create a new test function following the `test_*` naming pattern
