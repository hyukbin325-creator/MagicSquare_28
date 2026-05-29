"""Track A — U-OUT-01~03 Boundary success output contract RED skeletons."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.boundary.input_validator import InputValidator
from src.control.magic_square_resolver import MagicSquareResolver


class TestUOut01ResultShape:
    """U-OUT-01 — successful solve returns int[6]."""

    def test_u_out_01_valid_grid_returns_six_int_list(self) -> None:
        # U-OUT-01
        # Given
        # mock_resolver = MagicMock(spec=MagicSquareResolver)
        # mock_resolver.resolve.return_value = [3, 3, 6, 4, 4, 1]
        # validator = InputValidator(resolver=mock_resolver)
        # grid = valid_4x4_two_blanks  # G0
        # When
        # result = validator.handle_input(grid)
        # Then
        pytest.fail("RED: U-OUT-01 — success path returns list of six integers")


class TestUOut02OneIndexedCoordinates:
    """U-OUT-02 — output coordinates use 1-index contract."""

    def test_u_out_02_coordinates_are_one_indexed(self) -> None:
        # U-OUT-02
        # Given
        # mock_resolver = MagicMock(spec=MagicSquareResolver)
        # mock_resolver.resolve.return_value = [3, 3, 6, 4, 4, 1]
        # validator = InputValidator(resolver=mock_resolver)
        # grid = valid_4x4_two_blanks
        # When
        # result = validator.handle_input(grid)
        # Then
        pytest.fail("RED: U-OUT-02 — r/c in output are 1-index per PRD §8.2")


class TestUOut03PlacementOrder:
    """U-OUT-03 — output follows [r1,c1,n1,r2,c2,n2] placement contract."""

    def test_u_out_03_output_format_matches_prd_tuple(self) -> None:
        # U-OUT-03
        # Given
        # mock_resolver = MagicMock(spec=MagicSquareResolver)
        # mock_resolver.resolve.return_value = [3, 3, 6, 4, 4, 1]
        # validator = InputValidator(resolver=mock_resolver)
        # grid = valid_4x4_two_blanks
        # When
        # result = validator.handle_input(grid)
        # Then
        pytest.fail("RED: U-OUT-03 — success payload is [r1,c1,n1,r2,c2,n2]")
