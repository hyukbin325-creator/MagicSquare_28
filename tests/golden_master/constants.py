"""Named constants for Golden Master scenario contracts."""

from pathlib import Path

MAGIC_CONSTANT: int = 34
EXPECTED_BLANK_COUNT: int = 2
MIN_CELL_VALUE: int = 1
MAX_CELL_VALUE: int = 16

INVALID_BLANK_COUNT_CODE: str = "INVALID_BLANK_COUNT"
DUPLICATE_NUMBER_CODE: str = "DUPLICATE_NUMBER"
NO_VALID_MAGIC_SQUARE_CODE: str = "NO_VALID_MAGIC_SQUARE"

SECTION_SEPARATOR: str = "________________________________________"

DEFAULT_GOLDEN_MASTER_PATH: Path = (
    Path(__file__).resolve().parent.parent / "golden_master_expected.txt"
)
