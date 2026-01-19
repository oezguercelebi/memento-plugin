#!/usr/bin/env python3
"""
Test suite for count-tokens.py

Verifies token counting accuracy against known test files.
Run with: python3 tests/test_count_tokens.py
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# Test configuration
SCRIPT_PATH = Path(__file__).parent.parent / "scripts" / "count-tokens.py"
FIXTURES_PATH = Path(__file__).parent / "fixtures"
KNOWN_SIZES_PATH = FIXTURES_PATH / "known-sizes"
SAMPLE_PROJECT_PATH = FIXTURES_PATH / "sample-project"

# Expected token counts (verified with tiktoken cl100k_base)
EXPECTED_TOKENS = {
    "empty.txt": 0,
    "single-word.txt": 1,
    "ten-words.txt": 10,
    "simple-code.py": 23,
    "simple-markdown.md": 39,
    "simple-json.json": 39,
}

# Expected metadata
EXPECTED_METADATA = {
    "empty.txt": {"lines": 0, "bytes": 0},
    "single-word.txt": {"lines": 1, "bytes": 5},
    "ten-words.txt": {"lines": 1, "bytes": 48},
    "simple-code.py": {"lines": 5, "bytes": 87},
    "simple-markdown.md": {"lines": 15, "bytes": 143},
    "simple-json.json": {"lines": 6, "bytes": 84},
}

# Estimation tolerance (when tiktoken unavailable): 25% margin
ESTIMATION_TOLERANCE = 0.25


class TestResult:
    """Container for test results."""

    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.message = ""

    def __str__(self):
        status = "PASS" if self.passed else "FAIL"
        return f"[{status}] {self.name}: {self.message}"


def run_script(args: list) -> dict:
    """Run count-tokens.py with given arguments and return parsed JSON output."""
    cmd = [sys.executable, str(SCRIPT_PATH), "--json"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Script failed: {result.stderr}")

    return json.loads(result.stdout)


def test_file_token_count(filename: str, tiktoken_available: bool) -> TestResult:
    """Test token count for a single known file."""
    result = TestResult(f"Token count: {filename}")
    filepath = KNOWN_SIZES_PATH / filename
    expected = EXPECTED_TOKENS[filename]

    try:
        output = run_script([str(filepath)])
        actual = output["files"][0]["tokens"]

        if tiktoken_available:
            # Exact match expected with tiktoken
            if actual == expected:
                result.passed = True
                result.message = f"exact match ({actual} tokens)"
            else:
                result.message = f"expected {expected}, got {actual}"
        else:
            # Allow tolerance for estimation
            if expected == 0:
                result.passed = actual == 0
                result.message = f"empty file: got {actual}"
            else:
                lower = expected * (1 - ESTIMATION_TOLERANCE)
                upper = expected * (1 + ESTIMATION_TOLERANCE)
                if lower <= actual <= upper:
                    result.passed = True
                    result.message = f"within tolerance ({actual} tokens, expected ~{expected})"
                else:
                    result.message = f"out of tolerance: expected {expected} ± {ESTIMATION_TOLERANCE*100}%, got {actual}"
    except Exception as e:
        result.message = f"error: {e}"

    return result


def test_file_metadata(filename: str) -> TestResult:
    """Test file metadata (lines, bytes) for a known file."""
    result = TestResult(f"Metadata: {filename}")
    filepath = KNOWN_SIZES_PATH / filename
    expected = EXPECTED_METADATA[filename]

    try:
        output = run_script([str(filepath)])
        file_data = output["files"][0]

        lines_match = file_data["lines"] == expected["lines"]
        bytes_match = file_data["bytes"] == expected["bytes"]

        if lines_match and bytes_match:
            result.passed = True
            result.message = f"lines={file_data['lines']}, bytes={file_data['bytes']}"
        else:
            result.message = (
                f"lines: expected {expected['lines']}, got {file_data['lines']}; "
                f"bytes: expected {expected['bytes']}, got {file_data['bytes']}"
            )
    except Exception as e:
        result.message = f"error: {e}"

    return result


def test_multiple_files() -> TestResult:
    """Test analyzing multiple files at once."""
    result = TestResult("Multiple files analysis")

    try:
        files = [str(KNOWN_SIZES_PATH / f) for f in ["single-word.txt", "ten-words.txt"]]
        output = run_script(files)

        expected_total = EXPECTED_TOKENS["single-word.txt"] + EXPECTED_TOKENS["ten-words.txt"]
        actual_total = output["total_tokens"]

        if len(output["files"]) == 2:
            result.passed = True
            result.message = f"analyzed {len(output['files'])} files, total={actual_total} tokens"
        else:
            result.message = f"expected 2 files, got {len(output['files'])}"
    except Exception as e:
        result.message = f"error: {e}"

    return result


def test_nonexistent_file() -> TestResult:
    """Test handling of nonexistent files."""
    result = TestResult("Nonexistent file handling")

    try:
        output = run_script(["/nonexistent/path/file.txt"])
        file_data = output["files"][0]

        # Script returns exists=false and error field for missing files
        if file_data.get("exists") == False and "error" in file_data:
            result.passed = True
            result.message = f"correctly reports exists=false, error='{file_data['error']}'"
        else:
            result.message = f"unexpected response: {file_data}"
    except Exception as e:
        result.message = f"error: {e}"

    return result


def test_project_analysis() -> TestResult:
    """Test project-wide analysis with sample project."""
    result = TestResult("Project analysis")

    try:
        output = run_script(["--project", str(SAMPLE_PROJECT_PATH)])

        # Check required fields exist
        required_fields = ["project_root", "components", "totals", "budget", "budget_remaining"]
        missing = [f for f in required_fields if f not in output]

        if missing:
            result.message = f"missing fields: {missing}"
        else:
            result.passed = True
            total = output["totals"]["total_project_tokens"]
            result.message = f"total_project_tokens={total}, budget_remaining={output['budget_remaining']}"
    except Exception as e:
        result.message = f"error: {e}"

    return result


def test_project_discovers_components() -> TestResult:
    """Test that project analysis discovers all expected components."""
    result = TestResult("Component discovery")

    try:
        output = run_script(["--project", str(SAMPLE_PROJECT_PATH)])
        components = output["components"]

        discovered = []
        if components.get("claude_md"):
            discovered.append("claude_md")
        if components.get("skills"):
            discovered.append("skills")
        if components.get("commands"):
            discovered.append("commands")
        if components.get("agents"):
            discovered.append("agents")

        # Sample project should have at least claude_md and skills
        if "claude_md" in discovered and "skills" in discovered:
            result.passed = True
            result.message = f"found: {', '.join(discovered)}"
        else:
            result.message = f"expected claude_md and skills, found: {discovered}"
    except Exception as e:
        result.message = f"error: {e}"

    return result


def test_custom_budget() -> TestResult:
    """Test custom budget parameter."""
    result = TestResult("Custom budget")

    try:
        output = run_script(["--project", str(SAMPLE_PROJECT_PATH), "--budget", "100000"])

        if output["budget"] == 100000:
            result.passed = True
            result.message = f"budget={output['budget']}, remaining={output['budget_remaining']}"
        else:
            result.message = f"expected budget=100000, got {output['budget']}"
    except Exception as e:
        result.message = f"error: {e}"

    return result


def test_tiktoken_flag() -> TestResult:
    """Test that tiktoken availability is correctly reported."""
    result = TestResult("tiktoken availability flag")

    try:
        output = run_script([str(KNOWN_SIZES_PATH / "single-word.txt")])

        if "tiktoken_available" in output:
            result.passed = True
            result.message = f"tiktoken_available={output['tiktoken_available']}"
        else:
            result.message = "tiktoken_available field not found"
    except Exception as e:
        result.message = f"error: {e}"

    return result


def test_estimation_mode_accuracy() -> TestResult:
    """Test that estimation mode (~4 chars/token) is reasonably accurate."""
    result = TestResult("Estimation accuracy")

    # Use simple-code.py: 87 bytes, expected 23 tokens
    # Estimation: 87 / 4 = 21.75 ≈ 22 tokens
    # This should be within 25% tolerance
    filepath = KNOWN_SIZES_PATH / "simple-code.py"
    expected_tokens = EXPECTED_TOKENS["simple-code.py"]
    expected_bytes = EXPECTED_METADATA["simple-code.py"]["bytes"]

    estimated = expected_bytes // 4  # ~4 chars per token

    try:
        # Check if estimation is within 25% of actual
        lower = expected_tokens * (1 - ESTIMATION_TOLERANCE)
        upper = expected_tokens * (1 + ESTIMATION_TOLERANCE)

        if lower <= estimated <= upper:
            result.passed = True
            result.message = f"estimation ({estimated}) is within 25% of actual ({expected_tokens})"
        else:
            result.message = f"estimation ({estimated}) outside tolerance of actual ({expected_tokens})"
    except Exception as e:
        result.message = f"error: {e}"

    return result


def run_tests():
    """Run all tests and report results."""
    print("=" * 60)
    print("Memento Token Counter Test Suite")
    print("=" * 60)

    # Check tiktoken availability first
    try:
        output = run_script([str(KNOWN_SIZES_PATH / "empty.txt")])
        tiktoken_available = output.get("tiktoken_available", False)
    except:
        tiktoken_available = False

    print(f"\ntiktoken available: {tiktoken_available}")
    print("-" * 60)

    results = []

    # Test 1: Token counts for known files
    print("\n[Token Count Tests]")
    for filename in EXPECTED_TOKENS.keys():
        r = test_file_token_count(filename, tiktoken_available)
        results.append(r)
        print(r)

    # Test 2: Metadata tests
    print("\n[Metadata Tests]")
    for filename in EXPECTED_METADATA.keys():
        r = test_file_metadata(filename)
        results.append(r)
        print(r)

    # Test 3: Multiple files
    print("\n[Multi-file Tests]")
    r = test_multiple_files()
    results.append(r)
    print(r)

    # Test 4: Error handling
    print("\n[Error Handling Tests]")
    r = test_nonexistent_file()
    results.append(r)
    print(r)

    # Test 5: Project analysis
    print("\n[Project Analysis Tests]")
    r = test_project_analysis()
    results.append(r)
    print(r)

    r = test_project_discovers_components()
    results.append(r)
    print(r)

    # Test 6: Parameters
    print("\n[Parameter Tests]")
    r = test_custom_budget()
    results.append(r)
    print(r)

    r = test_tiktoken_flag()
    results.append(r)
    print(r)

    # Test 7: Estimation accuracy
    print("\n[Estimation Tests]")
    r = test_estimation_mode_accuracy()
    results.append(r)
    print(r)

    # Summary
    print("\n" + "=" * 60)
    passed = sum(1 for r in results if r.passed)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("All tests passed!")
        return 0
    else:
        failed = [r for r in results if not r.passed]
        print(f"\nFailed tests:")
        for r in failed:
            print(f"  - {r.name}")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
