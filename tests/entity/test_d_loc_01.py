"""Track B — D-LOC-01 BlankFinder RED skeleton (no Domain mocks)."""

from __future__ import annotations

import pytest

from src.entity.services.blank_finder import BlankFinder


class TestDLoc01BlankCoordinates:
    """D-LOC-01 — locate exactly two blank cells in row-major order."""

    def test_d_loc_01_g0_grid_returns_two_row_major_coords(self) -> None:
        # D-LOC-01
        # Given
        # finder = BlankFinder()
        # grid = G0_GRID
        # When
        # coords = finder.find_blanks(grid)
        # Then
        pytest.fail(
            "RED: D-LOC-01 — return two 0-index (row,col) pairs in row-major order"
        )
