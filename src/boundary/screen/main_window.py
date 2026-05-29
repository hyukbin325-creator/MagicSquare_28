"""Main PyQt window for MagicSquare grid input and validation."""

from __future__ import annotations

import logging

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from src.boundary.constants import GRID_SIZE
from src.boundary.input_validator import InputValidator
from src.boundary.schemas import ValidationErrorResponse
from src.boundary.screen.constants import (
    BLANK_CELL_DISPLAY,
    CELL_MAX_VALUE,
    CELL_MIN_VALUE,
    CLEAR_BUTTON_LABEL,
    PENDING_VALIDATION_MESSAGE,
    RESULT_LABEL_PREFIX,
    VALIDATE_BUTTON_LABEL,
    WINDOW_TITLE,
)
from src.boundary.screen.grid_parser import read_grid_from_spin_boxes

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """4×4 grid editor that delegates validation to the Boundary layer."""

    def __init__(self, validator: InputValidator | None = None) -> None:
        """Initialize the main window.

        Args:
            validator: Optional injected validator for testing or wiring.
        """
        super().__init__()
        self._validator = validator or InputValidator()
        self._spin_boxes: list[list[QSpinBox]] = []
        self._result_label = QLabel(f"{RESULT_LABEL_PREFIX}: —")
        self._result_label.setWordWrap(True)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Build widgets and layout."""
        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(360, 420)

        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)

        title = QLabel("Enter a 4×4 grid (0 = blank)")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root_layout.addWidget(title)

        grid_container = QWidget()
        grid_layout = QGridLayout(grid_container)
        grid_layout.setSpacing(6)

        cell_font = QFont()
        cell_font.setPointSize(14)

        for row in range(GRID_SIZE):
            row_boxes: list[QSpinBox] = []
            for col in range(GRID_SIZE):
                spin_box = QSpinBox()
                spin_box.setFont(cell_font)
                spin_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
                spin_box.setMinimum(CELL_MIN_VALUE)
                spin_box.setMaximum(CELL_MAX_VALUE)
                spin_box.setSpecialValueText(BLANK_CELL_DISPLAY)
                spin_box.setMinimumWidth(56)
                grid_layout.addWidget(spin_box, row, col)
                row_boxes.append(spin_box)
            self._spin_boxes.append(row_boxes)

        root_layout.addWidget(grid_container)

        button_row = QHBoxLayout()
        validate_button = QPushButton(VALIDATE_BUTTON_LABEL)
        validate_button.clicked.connect(self._on_validate_clicked)
        clear_button = QPushButton(CLEAR_BUTTON_LABEL)
        clear_button.clicked.connect(self._on_clear_clicked)
        button_row.addWidget(validate_button)
        button_row.addWidget(clear_button)
        root_layout.addLayout(button_row)

        self._result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root_layout.addWidget(self._result_label)

    def _on_clear_clicked(self) -> None:
        """Reset all cells to blank and clear the result message."""
        for row in self._spin_boxes:
            for cell in row:
                cell.setValue(CELL_MIN_VALUE)
        self._show_neutral_result("—")

    def _on_validate_clicked(self) -> None:
        """Read the grid, validate via Boundary, and display the contract result."""
        grid = read_grid_from_spin_boxes(self._spin_boxes)
        logger.debug("Validating grid from GUI: %s", grid)

        try:
            result = self._validator.validate_grid(grid)
        except NotImplementedError:
            self._show_info_result(PENDING_VALIDATION_MESSAGE)
            return

        if result is None:
            self._show_success_result(PENDING_VALIDATION_MESSAGE)
            return

        self._show_error_result(result)

    def _show_neutral_result(self, text: str) -> None:
        """Display a neutral result line."""
        self._result_label.setText(f"{RESULT_LABEL_PREFIX}: {text}")
        self._result_label.setStyleSheet("")

    def _show_error_result(self, response: ValidationErrorResponse) -> None:
        """Display a validation failure using the Boundary contract fields."""
        self._result_label.setText(
            f"{RESULT_LABEL_PREFIX}: [{response.code}] {response.message}"
        )
        self._result_label.setStyleSheet("color: #c0392b; font-weight: bold;")

    def _show_success_result(self, message: str) -> None:
        """Display a non-error outcome."""
        self._result_label.setText(f"{RESULT_LABEL_PREFIX}: {message}")
        self._result_label.setStyleSheet("color: #27ae60; font-weight: bold;")

    def _show_info_result(self, message: str) -> None:
        """Display an informational outcome (e.g. pending implementation)."""
        self._result_label.setText(f"{RESULT_LABEL_PREFIX}: {message}")
        self._result_label.setStyleSheet("color: #2980b9;")
