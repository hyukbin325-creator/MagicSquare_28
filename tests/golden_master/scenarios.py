"""Golden Master scenario definitions — input grids keyed by section name."""

from __future__ import annotations

from dataclasses import dataclass

Grid = list[list[int]]


@dataclass(frozen=True)
class GoldenScenario:
    """One Golden Master scenario with a stable section key and input grid."""

    test_id: str
    section: str
    grid: Grid


G0_GRID: Grid = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

G2_GRID: Grid = [
    [16, 0, 0, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 1],
]

G3_GRID: Grid = [
    [1, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

ONE_BLANK_GRID: Grid = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 0, 12],
    [13, 14, 15, 16],
]

DUPLICATE_GRID: Grid = [
    [1, 1, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 0, 12],
    [13, 14, 15, 0],
]

GOLDEN_SCENARIOS: tuple[GoldenScenario, ...] = (
    GoldenScenario(test_id="GM-TC-01", section="normal_success", grid=G2_GRID),
    GoldenScenario(test_id="GM-TC-02", section="reverse_success", grid=G0_GRID),
    GoldenScenario(
        test_id="GM-TC-03", section="invalid_blank_count", grid=ONE_BLANK_GRID
    ),
    GoldenScenario(test_id="GM-TC-04", section="duplicate_number", grid=DUPLICATE_GRID),
    GoldenScenario(
        test_id="GM-TC-05", section="no_valid_magic_square", grid=G3_GRID
    ),
)
