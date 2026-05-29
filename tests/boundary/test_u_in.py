"""Track A — U-IN-04~08 Boundary input validation RED skeletons."""

from __future__ import annotations

import pytest

from src.boundary.input_validator import InputValidator


class TestUIn04BlankCount:
    """U-IN-04 — blank cell count must be exactly two."""

    def test_u_in_04_one_blank_returns_e002(self) -> None:
        # U-IN-04
        # Given
        # validator = InputValidator(resolver=mock_resolver)
        # grid = four_by_four_one_blank  # exactly one zero
        # When
        # result = validator.validate_grid(grid)
        # Then
        pytest.fail("RED: U-IN-04 — blank count != 2 returns E002 contract failure")


class TestUIn05Duplicate:
    """U-IN-05 — non-zero duplicate values rejected."""

    def test_u_in_05_duplicate_non_zero_returns_e003(self) -> None:
        # U-IN-05
        # Given
        # validator = InputValidator(resolver=mock_resolver)
        # grid = four_by_four_duplicate
        # When
        # result = validator.validate_grid(grid)
        # Then
        pytest.fail("RED: U-IN-05 — duplicate non-zero values returns E003")


class TestUIn06ValueRange:
    """U-IN-06 — cell values must be 0 or 1..16."""

    def test_u_in_06_out_of_range_returns_e004(self) -> None:
        # U-IN-06
        # Given
        # validator = InputValidator(resolver=mock_resolver)
        # grid = four_by_four_out_of_range
        # When
        # result = validator.validate_grid(grid)
        # Then
        pytest.fail("RED: U-IN-06 — value outside 0|1..16 returns E004")


class TestUIn07BlankCountEdge:
    """U-IN-07 — zero-blank count edge cases (none or three+)."""

    def test_u_in_07_three_blanks_returns_e002(self) -> None:
        # U-IN-07
        # Given
        # validator = InputValidator(resolver=mock_resolver)
        # grid = four_by_four_three_blanks
        # When
        # result = validator.validate_grid(grid)
        # Then
        pytest.fail("RED: U-IN-07 — three zero cells returns E002 blank-count failure")

    def test_u_in_07_no_blanks_returns_e002(self) -> None:
        # U-IN-07
        # Given
        # validator = InputValidator(resolver=mock_resolver)
        # grid = four_by_four_no_blanks
        # When
        # result = validator.validate_grid(grid)
        # Then
        pytest.fail("RED: U-IN-07 — zero blank cells returns E002 blank-count failure")


class TestUIn08ResolverIsolation:
    """U-IN-08 — value/blank/duplicate failures never invoke Domain resolver."""

    def test_u_in_08_duplicate_grid_resolve_not_called(self) -> None:
        # U-IN-08
        # Given
        # validator = InputValidator(resolver=mock_resolver)
        # grid = four_by_four_duplicate
        # When
        # validator.handle_input(grid)
        # Then
        # mock_resolver.resolve.assert_not_called()
        pytest.fail("RED: U-IN-08 — validation failure must not call Domain resolve()")
