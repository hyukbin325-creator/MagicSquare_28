"""Approval-style Golden Master comparison with unified diff on mismatch."""

from __future__ import annotations

import difflib
from pathlib import Path

import pytest

from tests.golden_master.constants import DEFAULT_GOLDEN_MASTER_PATH
from tests.golden_master.format import format_document, format_section, parse_document
from tests.golden_master.reference_capture import (
    SolverResult,
    capture_solver_result,
    serialize_result,
)
from tests.golden_master.scenarios import GOLDEN_SCENARIOS, GoldenScenario, Grid


def read_expected(expected_path: Path) -> str:
    """Read Golden Master baseline file contents."""
    with expected_path.open(encoding="utf-8") as handle:
        return handle.read()


def build_expected_document() -> str:
    """Capture current solver output for all Golden Master scenarios."""
    sections = [build_section_block(scenario) for scenario in GOLDEN_SCENARIOS]
    return format_document(sections)


def build_section_block(scenario: GoldenScenario) -> str:
    """Capture and format one scenario section from the solver."""
    result = capture_solver_result(scenario.grid)
    return format_section_from_result(scenario.section, scenario.grid, result)


def format_section_from_result(
    section: str,
    grid: Grid,
    result: SolverResult,
) -> str:
    """Format one Golden Master section from a live solver result."""
    outcome_kind, payload = serialize_result(result)
    if outcome_kind == "error":
        assert isinstance(payload, str)
        return format_section(section, grid, error=payload)
    assert isinstance(payload, list)
    return format_section(section, grid, output=payload)


def approve(
    actual: str,
    expected_path: Path = DEFAULT_GOLDEN_MASTER_PATH,
) -> None:
    """Compare actual output to baseline using open(expected).read() vs actual."""
    if not expected_path.exists():
        expected_path.parent.mkdir(parents=True, exist_ok=True)
        with expected_path.open("w", encoding="utf-8") as handle:
            handle.write(actual)
        pytest.fail(
            f"Golden Master baseline created at {expected_path}. "
            "Re-run tests to verify against the new baseline."
        )

    expected = read_expected(expected_path)
    if actual == expected:
        return

    diff_text = format_unified_diff(expected, actual)
    pytest.fail(
        "Golden Master mismatch.\n"
        f"Expected file: {expected_path}\n"
        f"{diff_text}"
    )


def approve_section(
    actual_section: str,
    section_name: str,
    expected_path: Path = DEFAULT_GOLDEN_MASTER_PATH,
) -> None:
    """Compare one scenario section against the baseline file section."""
    if not expected_path.exists():
        write_baseline(expected_path)
        pytest.fail(
            f"Golden Master baseline created at {expected_path}. "
            "Re-run tests to verify against the new baseline."
        )

    expected_section = extract_section_text(read_expected(expected_path), section_name)
    if actual_section == expected_section:
        return

    diff_text = format_unified_diff(expected_section, actual_section)
    pytest.fail(
        f"Golden Master section mismatch: [{section_name}]\n"
        f"Expected file: {expected_path}\n"
        f"{diff_text}"
    )


def extract_section_text(document: str, section_name: str) -> str:
    """Extract one section block from a Golden Master document."""
    parsed = parse_document(document)
    section = parsed[section_name]
    if section.outcome_kind == "error":
        return format_section(section.name, section.grid, error=section.outcome_lines[0])
    output_text = section.outcome_lines[0]
    values = [int(value) for value in output_text.strip("[]").split(",")]
    return format_section(section.name, section.grid, output=values)


def format_unified_diff(expected: str, actual: str) -> str:
    """Render a unified diff with --- expected / +++ actual headers."""
    diff_lines = difflib.unified_diff(
        expected.splitlines(keepends=True),
        actual.splitlines(keepends=True),
        fromfile="expected",
        tofile="actual",
    )
    return "".join(diff_lines)


def write_baseline(path: Path = DEFAULT_GOLDEN_MASTER_PATH) -> Path:
    """Write the current solver capture to the Golden Master baseline file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        handle.write(build_expected_document())
    return path
