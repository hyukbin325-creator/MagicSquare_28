"""Capture and serialize Magic Square solver results for Golden Master tests."""

from __future__ import annotations

import io
import sys
from contextlib import redirect_stdout

from tests.golden_master.approve import format_section_from_result
from tests.golden_master.format import format_success_output
from tests.golden_master.reference_capture import (
    SolverResult,
    capture_solver_result,
    serialize_result,
)
from tests.golden_master.scenarios import GoldenScenario, Grid


def capture_api_result(grid: Grid) -> SolverResult:
    """Capture solver output via API result (DTO or success list)."""
    return capture_solver_result(grid)


def serialize_api_result(result: SolverResult) -> str:
    """Serialize a solver API result to Golden Master outcome text."""
    outcome_kind, payload = serialize_result(result)
    if outcome_kind == "error":
        assert isinstance(payload, str)
        return payload
    assert isinstance(payload, list)
    return format_success_output(payload)


def capture_stdout_result(grid: Grid) -> str:
    """Capture solver output written to stdout (fallback capture strategy)."""
    buffer = io.StringIO()
    result = capture_api_result(grid)
    with redirect_stdout(buffer):
        sys.stdout.write(serialize_api_result(result))
    return buffer.getvalue()


def capture_section_text(scenario: GoldenScenario) -> str:
    """Serialize one scenario block for Golden Master file comparison."""
    result = capture_api_result(scenario.grid)
    return format_section_from_result(scenario.section, scenario.grid, result)
