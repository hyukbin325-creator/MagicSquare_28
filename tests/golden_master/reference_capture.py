"""Reference solver capture used to bootstrap Golden Master baseline files."""

from __future__ import annotations

from dataclasses import dataclass

from src.boundary.schemas import ValidationErrorResponse
from tests.golden_master.constants import (
    DUPLICATE_NUMBER_CODE,
    EXPECTED_BLANK_COUNT,
    INVALID_BLANK_COUNT_CODE,
    MAGIC_CONSTANT,
    MAX_CELL_VALUE,
    MIN_CELL_VALUE,
    NO_VALID_MAGIC_SQUARE_CODE,
)

Grid = list[list[int]]
SolverResult = list[int] | ValidationErrorResponse


@dataclass(frozen=True)
class BlankPlacement:
    """Zero-index blank coordinates in row-major order."""

    row: int
    col: int


def capture_solver_result(grid: Grid) -> SolverResult:
    """Run reference validation and solver logic for Golden Master capture."""
    validation_error = _validate_grid(grid)
    if validation_error is not None:
        return validation_error
    return _solve_two_blank_grid(grid)


def serialize_result(result: SolverResult) -> tuple[str, list[int] | str]:
    """Convert a solver result into Golden Master outcome kind and payload."""
    if isinstance(result, ValidationErrorResponse):
        return "error", result.code
    return "output", result


def _validate_grid(grid: Grid) -> ValidationErrorResponse | None:
    blank_count = sum(row.count(0) for row in grid)
    if blank_count != EXPECTED_BLANK_COUNT:
        return ValidationErrorResponse(
            code=INVALID_BLANK_COUNT_CODE,
            message="Grid must contain exactly two blank cells.",
        )

    seen: set[int] = set()
    for row in grid:
        for value in row:
            if value == 0:
                continue
            if value < MIN_CELL_VALUE or value > MAX_CELL_VALUE:
                msg = f"Cell value {value} is outside allowed range."
                return ValidationErrorResponse(code="INVALID_VALUE", message=msg)
            if value in seen:
                return ValidationErrorResponse(
                    code=DUPLICATE_NUMBER_CODE,
                    message="Duplicate non-zero values are not allowed.",
                )
            seen.add(value)
    return None


def _solve_two_blank_grid(grid: Grid) -> list[int]:
    blanks = _find_blanks(grid)
    missing = _find_missing_numbers(grid)
    small, large = sorted(missing)
    first_blank, second_blank = blanks

    if _is_valid_completion(grid, first_blank, small, second_blank, large):
        return _build_output(first_blank, small, second_blank, large)

    if _is_valid_completion(grid, first_blank, large, second_blank, small):
        return _build_output(first_blank, large, second_blank, small)

    return ValidationErrorResponse(
        code=NO_VALID_MAGIC_SQUARE_CODE,
        message="No valid magic square completion exists for the given grid.",
    )


def _find_blanks(grid: Grid) -> list[BlankPlacement]:
    blanks: list[BlankPlacement] = []
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            if value == 0:
                blanks.append(BlankPlacement(row=row_index, col=col_index))
    return blanks


def _find_missing_numbers(grid: Grid) -> list[int]:
    present = {value for row in grid for value in row if value != 0}
    return [
        value
        for value in range(MIN_CELL_VALUE, MAX_CELL_VALUE + 1)
        if value not in present
    ]


def _build_output(
    first_blank: BlankPlacement,
    first_value: int,
    second_blank: BlankPlacement,
    second_value: int,
) -> list[int]:
    return [
        first_blank.row + 1,
        first_blank.col + 1,
        first_value,
        second_blank.row + 1,
        second_blank.col + 1,
        second_value,
    ]


def _is_valid_completion(
    grid: Grid,
    first_blank: BlankPlacement,
    first_value: int,
    second_blank: BlankPlacement,
    second_value: int,
) -> bool:
    completed = [row[:] for row in grid]
    completed[first_blank.row][first_blank.col] = first_value
    completed[second_blank.row][second_blank.col] = second_value
    return _is_magic_square(completed)


def _is_magic_square(grid: Grid) -> bool:
    row_sums = [sum(row) for row in grid]
    col_sums = [
        sum(grid[row_index][col_index] for row_index in range(4))
        for col_index in range(4)
    ]
    diag_main = sum(grid[index][index] for index in range(4))
    diag_anti = sum(grid[index][3 - index] for index in range(4))
    expected = [MAGIC_CONSTANT] * 10
    return row_sums + col_sums + [diag_main, diag_anti] == expected
