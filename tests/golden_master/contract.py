"""Golden Master solver output contract assertions."""

from __future__ import annotations

from src.boundary.schemas import ValidationErrorResponse
from src.boundary.constants import GRID_SIZE
from tests.golden_master.constants import (
    DUPLICATE_NUMBER_CODE,
    INVALID_BLANK_COUNT_CODE,
    MAX_CELL_VALUE,
    MIN_CELL_VALUE,
    NO_VALID_MAGIC_SQUARE_CODE,
)
from tests.golden_master.reference_capture import (
    BlankPlacement,
    _find_blanks,
    _find_missing_numbers,
    _is_valid_completion,
)

Grid = list[list[int]]


def assert_success_output_contract(grid: Grid, result: list[int]) -> None:
    """Verify int[6] success payload, row-major blanks, and 1-index coordinates."""
    assert isinstance(result, list)
    assert len(result) == 6
    assert all(isinstance(value, int) for value in result)

    row1, col1, number1, row2, col2, number2 = result
    for row, col in ((row1, col1), (row2, col2)):
        assert MIN_CELL_VALUE <= row <= GRID_SIZE
        assert MIN_CELL_VALUE <= col <= GRID_SIZE
    for number in (number1, number2):
        assert MIN_CELL_VALUE <= number <= MAX_CELL_VALUE

    blanks = _find_blanks(grid)
    assert len(blanks) == 2
    assert (row1, col1) == (blanks[0].row + 1, blanks[0].col + 1)
    assert (row2, col2) == (blanks[1].row + 1, blanks[1].col + 1)
    assert _row_major_index(blanks[0]) < _row_major_index(blanks[1])


def assert_small_first_combination(grid: Grid, result: list[int]) -> None:
    """Verify the solver applied the smaller missing value at the first blank."""
    blanks = _find_blanks(grid)
    small, large = sorted(_find_missing_numbers(grid))
    _, _, number1, _, _, number2 = result
    assert number1 == small
    assert number2 == large
    assert _is_valid_completion(grid, blanks[0], small, blanks[1], large)


def assert_reverse_fallback_combination(grid: Grid, result: list[int]) -> None:
    """Verify small-first fails and reverse placement succeeds."""
    blanks = _find_blanks(grid)
    small, large = sorted(_find_missing_numbers(grid))
    assert not _is_valid_completion(grid, blanks[0], small, blanks[1], large)

    _, _, number1, _, _, number2 = result
    assert number1 == large
    assert number2 == small
    assert _is_valid_completion(grid, blanks[0], large, blanks[1], small)


def assert_error_contract(
    result: ValidationErrorResponse,
    *,
    expected_code: str,
) -> None:
    """Verify ValidationErrorResponse error contract fields."""
    assert isinstance(result, ValidationErrorResponse)
    assert result.code == expected_code
    assert isinstance(result.message, str)
    assert result.message.strip() != ""


def assert_invalid_blank_count_contract(result: ValidationErrorResponse) -> None:
    """Verify INVALID_BLANK_COUNT error contract."""
    assert_error_contract(result, expected_code=INVALID_BLANK_COUNT_CODE)


def assert_duplicate_number_contract(result: ValidationErrorResponse) -> None:
    """Verify DUPLICATE_NUMBER error contract."""
    assert_error_contract(result, expected_code=DUPLICATE_NUMBER_CODE)


def assert_no_valid_magic_square_contract(result: ValidationErrorResponse) -> None:
    """Verify NO_VALID_MAGIC_SQUARE error contract."""
    assert_error_contract(result, expected_code=NO_VALID_MAGIC_SQUARE_CODE)


def _row_major_index(blank: BlankPlacement) -> int:
    return blank.row * GRID_SIZE + blank.col
