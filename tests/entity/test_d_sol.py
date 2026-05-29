"""Track B — D-SOL-01~04 Solver RED skeletons (no Domain mocks)."""

from __future__ import annotations

import pytest

from src.entity.services.solver import MagicSquareSolver


class TestDSol01ReverseCombinationSuccess:
    """D-SOL-01 — SC-DOM-SOL-001 reverse placement succeeds on G0."""

    def test_d_sol_01_g0_returns_sc_dom_sol_001_output(self) -> None:
        # D-SOL-01
        # Given
        # solver = MagicSquareSolver()
        # grid = G0_GRID
        # When
        # result = solver.solve(grid)
        # Then
        pytest.fail("RED: D-SOL-01 — G0 solve returns [3,3,6,4,4,1] 1-index")


class TestDSol02G2Tbd:
    """D-SOL-02 — G2 fixture undefined; explicit TBD RED marker."""

    def test_d_sol_02_g2_tbd(self) -> None:
        pytest.fail("RED: D-SOL-02 — G2 TBD")


class TestDSol03SmallFirstFails:
    """D-SOL-03 — small-to-first-blank attempt fails magic validation."""

    def test_d_sol_03_small_first_combination_fails_validator(self) -> None:
        # D-SOL-03
        # Given
        # solver = MagicSquareSolver()
        # grid = G0_GRID
        # When
        # first_attempt_valid = solver.try_small_first(grid)
        # Then
        pytest.fail(
            "RED: D-SOL-03 — place smaller missing in first blank fails invariant"
        )


class TestDSol04BothCombinationsFail:
    """D-SOL-04 — neither placement yields valid magic square."""

    def test_d_sol_04_g3_both_combinations_unsolvable(self) -> None:
        # D-SOL-04
        # Given
        # solver = MagicSquareSolver()
        # grid = G3_GRID
        # When
        # result = solver.solve(grid)
        # Then
        pytest.fail("RED: D-SOL-04 — both combinations fail returns defined failure")
