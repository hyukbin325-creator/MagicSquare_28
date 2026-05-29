"""Shared pytest configuration."""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Dual-Track RED skeleton — G0~G3 grid fixtures (see tests/entity/conftest.py).
# G0: partial two-blank grid (SC-DOM-SOL-001). G1: valid completed magic square.
# G2: TBD. G3: completed grid failing magic invariant.
