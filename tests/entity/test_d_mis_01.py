"""Track B — D-MIS-01 MissingNumberFinder RED skeleton (no Domain mocks)."""

from __future__ import annotations

import pytest

from src.entity.services.missing_number_finder import MissingNumberFinder


class TestDMis01MissingNumbers:
    """D-MIS-01 — find two missing values from 1..16 excluding zeros."""

    def test_d_mis_01_g0_grid_returns_one_and_six_ascending(self) -> None:
        # D-MIS-01
        # Given
        # finder = MissingNumberFinder()
        # grid = G0_GRID
        # When
        # missing = finder.find_missing(grid)
        # Then
        pytest.fail("RED: D-MIS-01 — G0 missing numbers are [1, 6] ascending")
