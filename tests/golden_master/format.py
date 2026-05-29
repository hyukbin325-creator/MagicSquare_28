"""Serialize and parse Golden Master expected-output sections."""

from __future__ import annotations

import re
from dataclasses import dataclass

from tests.golden_master.constants import SECTION_SEPARATOR

Grid = list[list[int]]


@dataclass(frozen=True)
class GoldenSection:
    """Parsed Golden Master section with input grid and outcome lines."""

    name: str
    grid: Grid
    outcome_kind: str
    outcome_lines: tuple[str, ...]


def format_grid(grid: Grid) -> str:
    """Render a 4x4 grid as space-separated rows for Golden Master files."""
    return "\n".join(" ".join(str(cell) for cell in row) for row in grid)


def parse_grid(text: str) -> Grid:
    """Parse space-separated grid rows from Golden Master file text."""
    rows: Grid = []
    for line in text.strip().splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        rows.append([int(value) for value in stripped.split()])
    return rows


def format_success_output(values: list[int]) -> str:
    """Render a solver success payload as Golden Master output text."""
    inner = ",".join(str(value) for value in values)
    return f"[{inner}]"


def format_error_output(code: str) -> str:
    """Render a validation or solver failure code for Golden Master files."""
    return code


def format_section(
    name: str,
    grid: Grid,
    *,
    output: list[int] | None = None,
    error: str | None = None,
) -> str:
    """Build one Golden Master section block."""
    lines = [f"[{name}]", "Input:", format_grid(grid), ""]
    if error is not None:
        lines.extend(["Error:", error])
    elif output is not None:
        lines.extend(["Output:", format_success_output(output)])
    else:
        msg = "Golden Master section requires either output or error."
        raise ValueError(msg)
    return "\n".join(lines)


def format_document(sections: list[str]) -> str:
    """Join section blocks with the canonical separator."""
    body = f"\n{SECTION_SEPARATOR}\n\n".join(sections)
    return f"{body}\n"


def parse_document(text: str) -> dict[str, GoldenSection]:
    """Parse a Golden Master file into section objects keyed by section name."""
    chunks = re.split(rf"\n{re.escape(SECTION_SEPARATOR)}\n", text.strip())
    parsed: dict[str, GoldenSection] = {}
    for chunk in chunks:
        section = _parse_section_chunk(chunk)
        parsed[section.name] = section
    return parsed


def _parse_section_chunk(chunk: str) -> GoldenSection:
    lines = [line.rstrip() for line in chunk.strip().splitlines()]
    if not lines or not lines[0].startswith("[") or not lines[0].endswith("]"):
        msg = f"Invalid Golden Master section header: {lines[:1]!r}"
        raise ValueError(msg)

    name = lines[0][1:-1]
    input_idx = lines.index("Input:")
    outcome_idx = _find_outcome_index(lines, start=input_idx + 1)
    grid = parse_grid("\n".join(lines[input_idx + 1 : outcome_idx]))
    outcome_label = lines[outcome_idx]
    outcome_lines = tuple(lines[outcome_idx + 1 :])
    outcome_kind = outcome_label.rstrip(":").lower()
    return GoldenSection(
        name=name,
        grid=grid,
        outcome_kind=outcome_kind,
        outcome_lines=outcome_lines,
    )


def _find_outcome_index(lines: list[str], start: int) -> int:
    for index in range(start, len(lines)):
        if lines[index] in {"Output:", "Error:"}:
            return index
    msg = "Golden Master section missing Output: or Error: block."
    raise ValueError(msg)
