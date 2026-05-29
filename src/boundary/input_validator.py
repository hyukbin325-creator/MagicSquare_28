"""Boundary input validator — shape and contract checks before Domain invocation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.boundary.constants import GRID_SHAPE_ERROR_MESSAGE, INVALID_SIZE_CODE
from src.boundary.schemas import ValidationErrorResponse

if TYPE_CHECKING:
    from src.control.magic_square_resolver import MagicSquareResolver


class InputValidator:
    """Validates incoming grid shape before delegating to the Domain resolver."""

    def __init__(self, resolver: MagicSquareResolver | None = None) -> None:
        self._resolver = resolver

    def validate_grid(self, grid: object) -> ValidationErrorResponse | None:
        """Return a validation error when shape is invalid; None when shape is 4x4."""
        if grid is None:
            return ValidationErrorResponse(
                code=INVALID_SIZE_CODE,
                message=GRID_SHAPE_ERROR_MESSAGE,
            )
        if isinstance(grid, list) and len(grid) == 0:
            return ValidationErrorResponse(
                code=INVALID_SIZE_CODE,
                message=GRID_SHAPE_ERROR_MESSAGE,
            )
        raise NotImplementedError("GREEN phase: AC-FR-01-01 shape validation")

    def handle_input(self, grid: object) -> ValidationErrorResponse | list[int]:
        """Validate input and invoke resolver only when shape validation passes."""
        raise NotImplementedError("GREEN phase: Boundary orchestration")
