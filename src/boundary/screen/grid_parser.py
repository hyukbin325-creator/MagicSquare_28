"""Convert GUI grid widgets into Boundary validation input."""

from __future__ import annotations

from PyQt6.QtWidgets import QSpinBox

from src.boundary.constants import GRID_SIZE


def read_grid_from_spin_boxes(
    spin_boxes: list[list[QSpinBox]],
) -> list[list[int]]:
    """Read a GRID_SIZE×GRID_SIZE integer grid from spin box widgets.

    Args:
        spin_boxes: Row-major spin boxes; each row must contain GRID_SIZE widgets.

    Returns:
        Nested list of cell values (0 represents a blank cell).
    """
    return [[cell.value() for cell in row] for row in spin_boxes]


def create_empty_grid() -> list[list[int]]:
    """Return a GRID_SIZE×GRID_SIZE grid filled with blank cells (0)."""
    return [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
