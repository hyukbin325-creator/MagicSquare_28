"""Allow ``python -m src.boundary.screen`` to launch the GUI."""

import sys

from src.boundary.screen.app import main

sys.exit(main())
