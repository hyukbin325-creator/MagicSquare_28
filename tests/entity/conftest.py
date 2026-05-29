"""Entity-layer grid fixtures (G0~G3) — RED skeleton placeholders only."""

from __future__ import annotations

# G0: SC-DOM-SOL-001 partial grid — two blanks, missing 1 and 6 (row-major blanks at (2,2), (3,3) 0-index).
# G0_GRID: list[list[int]] = [
#     [16, 2, 3, 13],
#     [5, 11, 10, 8],
#     [9, 7, 0, 12],
#     [4, 14, 15, 0],
# ]

# G1: completed valid 4x4 magic square (validator positive control).
# G1_GRID: list[list[int]] = [...]

# G2: two blanks — small-first placement succeeds (SC-DOM-SOL-002 candidate).
# G2_GRID: list[list[int]] = [
#     [16, 0, 0, 13],
#     [5, 11, 10, 8],
#     [9, 7, 6, 12],
#     [4, 14, 15, 1],
# ]

# G3: two blanks, missing 6 and 16 — neither placement satisfies magic constant 34.
# G3_GRID: list[list[int]] = [
#     [1, 2, 3, 13],
#     [5, 11, 10, 8],
#     [9, 7, 0, 12],
#     [4, 14, 15, 0],
# ]
