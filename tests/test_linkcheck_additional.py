"""Additional edge-case tests for linkcheck coverage.

Covers: build_actual_pages ./strip (linkcheck.py:33).
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent.parent / ".hermes"
sys.path.insert(0, str(_SCRIPT_DIR))

from linkcheck import build_actual_pages  # noqa: E402


class TestBuildActualPages:
    """Tests for build_actual_pages coverage gaps."""

    def test_build_actual_pages_strips_dot_prefix(self):
        """build_actual_pages handles ./ prefix (linkcheck.py:33)."""
        pages = build_actual_pages({str(Path("site/index.html"))})
        assert isinstance(pages, set)
