"""Fixtures for Boundary-layer AC-FR-01-01 tests."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.boundary.constants import GRID_SHAPE_ERROR_MESSAGE, INVALID_SIZE_CODE
from src.boundary.input_validator import InputValidator
from src.control.magic_square_resolver import MagicSquareResolver

# AC-FR-01-01 in-scope invalid shape fixtures only (no valid 4x4, no AC-FR-01-02~05 cases).
INVALID_SHAPE_GRIDS: dict[str, object] = {
    "none": None,
    "empty_list": [],
    "four_rows_zero_cols": [[]] * 4,
    "three_by_four": [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
    ],
    "four_by_three": [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [10, 11, 12],
    ],
}

# Out-of-scope for this module (AC-FR-01-02~05 / FR-02~05) — must not appear above.
OUT_OF_SCOPE_GRIDS: dict[str, list[list[int]]] = {
    "valid_4x4_two_blanks": [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 7, 0, 12],
        [4, 14, 15, 0],
    ],
    "four_by_four_one_blank": [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 0, 12],
        [13, 14, 15, 16],
    ],
    "four_by_four_duplicate": [
        [1, 1, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 0, 12],
        [13, 14, 15, 0],
    ],
    "four_by_four_out_of_range": [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 0, 12],
        [13, 14, 15, 17],
    ],
}


@pytest.fixture
def mock_resolver() -> MagicMock:
    """Domain resolver mock for isolation assertions."""
    return MagicMock(spec=MagicSquareResolver)


@pytest.fixture
def validator(mock_resolver: MagicMock) -> InputValidator:
    """InputValidator with injected resolver mock."""
    return InputValidator(resolver=mock_resolver)


@pytest.fixture
def prd_invalid_size_code() -> str:
    return INVALID_SIZE_CODE


@pytest.fixture
def prd_shape_error_message() -> str:
    return GRID_SHAPE_ERROR_MESSAGE
