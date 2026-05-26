"""Targeted edge-case tests for linkcheck uncovered code paths.

Covers:
- build_actual_pages with ./ prefix (linkcheck.py:33)
- check_links verbose mode (linkcheck.py:62)
- check_links skipping http/https # hash links (linkcheck.py:81,83)
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent.parent / ".hermes"
sys.path.insert(0, str(_SCRIPT_DIR))

from linkcheck import build_actual_pages, check_links, resolve_link, main


class TestBuildActualPagesEdgeCases:
    """Tests for build_actual_pages edge cases."""

    def test_build_actual_pages_with_dot_prefix(self):
        """build_actual_pages handles ./relpath (linkcheck.py:33)."""
        # On Windows, os.path.relpath might not produce ./ prefix
        # On Unix it does. We test with a path that when relativized
        # starts with ./
        files = {"/tmp/site/index.html", "/tmp/site/blog/post.html"}
        pages = build_actual_pages(files)
        # Paths should be relativized correctly regardless of OS
        assert isinstance(pages, set)
        if os.name == "posix":
            assert all(not p.startswith("./") or p == "./something" for p in pages)


class TestCheckLinksEdgeCases:
    """Tests for check_links uncovered paths."""

    def test_check_links_verbose_prints_count(self, capsys):
        """check_links with verbose=True prints page count (linkcheck.py:62)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "index.html").write_text("<html><body>Hello</body></html>")
            (root / "page.html").write_text(
                '<html><body><a href="index.html">home</a></body></html>'
            )

            broken = check_links(tmpdir, verbose=True)
            assert broken == 0
            captured = capsys.readouterr()
            assert "Actual HTML pages" in captured.out
            assert "Checked" in captured.out

    def test_check_links_skips_external_links(self):
        """check_links skips http/https links (linkcheck.py:81)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "index.html").write_text(
                '<html><body>'
                '<a href="https://example.com/page.html">external</a>'
                '<a href="http://example.org/page.html">external2</a>'
                '</body></html>'
            )
            (root / "other.html").write_text('<html><body>Hi</body></html>')

            # Should not report any broken links since external links are skipped
            broken = check_links(tmpdir)
            assert broken == 0

    def test_check_links_skips_hash_anchors(self):
        """check_links skips #hash links (linkcheck.py:83)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "index.html").write_text(
                '<html><body>'
                '<a href="#section">section</a>'
                '<a href="#top">top</a>'
                '</body></html>'
            )

            broken = check_links(tmpdir)
            assert broken == 0

    def test_check_links_verbose_with_broken(self, capsys):
        """check_links verbose with broken links prints summary (linkcheck.py:62)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "index.html").write_text(
                '<html><body>'
                '<a href="missing.html">broken</a>'
                '</body></html>'
            )

            broken = check_links(tmpdir, verbose=True)
            assert broken == 1
            captured = capsys.readouterr()
            assert "broken" in captured.out

    def test_check_links_verbose_with_broken(self, capsys):
        """check_links verbose with broken links prints summary (linkcheck.py:62)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "index.html").write_text(
                '<html><body>'
                '<a href="missing.html">broken</a>'
                '</body></html>'
            )
            broken = check_links(tmpdir, verbose=True)
            assert broken == 1
            captured = capsys.readouterr()
            assert "broken" in captured.out


class TestMainEdgeCases:
    """Tests for main entry point."""

    def test_main_cli_invocation(self):
        """main() with empty dir returns 0."""
        with tempfile.TemporaryDirectory() as tmpdir:
            rc = main([tmpdir])
            assert rc == 0
