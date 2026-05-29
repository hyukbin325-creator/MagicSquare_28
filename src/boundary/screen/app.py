"""PyQt application entry point for the MagicSquare Boundary GUI."""

from __future__ import annotations

import logging
import sys

from PyQt6.QtWidgets import QApplication

from src.boundary.screen.main_window import MainWindow

logger = logging.getLogger(__name__)


def main() -> int:
    """Launch the MagicSquare GUI and run the Qt event loop.

    Returns:
        Process exit code from the Qt event loop.
    """
    logging.basicConfig(level=logging.INFO)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    logger.info("MagicSquare GUI started")
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
