"""Domain resolution entry point invoked from Control after Boundary validation."""

from __future__ import annotations


class MagicSquareResolver:
    """Resolves a valid 4x4 partial grid into the solver output contract."""

    def resolve(self, grid: list[list[int]]) -> list[int]:
        """Return [r1, c1, n1, r2, c2, n2] for the given grid."""
        raise NotImplementedError("GREEN phase: Domain resolution")
