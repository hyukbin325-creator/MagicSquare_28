"""Generate Golden Master baseline file from current solver capture output."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests.golden_master.approve import write_baseline
from tests.golden_master.constants import DEFAULT_GOLDEN_MASTER_PATH


def main() -> int:
    """Write the Golden Master expected-output file from live solver capture."""
    parser = argparse.ArgumentParser(
        description="Generate tests/golden_master_expected.txt from solver output."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_GOLDEN_MASTER_PATH,
        help="Path to the Golden Master baseline file.",
    )
    args = parser.parse_args()

    output_path = write_baseline(args.output)
    print(f"Golden Master baseline written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
