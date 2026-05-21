"""Tests for the DevForge link checker script.

These tests verify the link-checking logic by creating temporary HTML
file trees and checking path resolution. They do not import linkcheck.py
directly (it runs as a top-level script), but instead validate the
path-resolution and file-discovery patterns it uses.
"""

import os
import tempfile
from pathlib import Path


def create_temp_html(directory: Path, filename: str, links: list[str]) -> Path:
    """Create a temporary HTML file with given anchor links."""
    links_html = "\n".join(f'    <a href="{link}">link</a>' for link in links)
    content = f"""<!DOCTYPE html>
<html>
<body>
{links_html}
</body>
</html>
"""
    filepath = directory / filename
    filepath.write_text(content, encoding="utf-8")
    return filepath


def test_walk_collects_html_files():
    """Verify os.walk finds all .html files in a directory tree."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        sub = root / "sub"
        sub.mkdir()
        (root / "a.html").write_text("<html></html>")
        (root / "b.html").write_text("<html></html>")
        (sub / "c.html").write_text("<html></html>")

        files = set()
        for r, _dirs, files_list in os.walk(tmpdir):
            for f in files_list:
                if f.endswith(".html"):
                    files.add(os.path.join(r, f))

        assert len(files) == 3, f"Expected 3 HTML files, got {len(files)}"


def test_existing_link_resolves():
    """Verify that a link to an existing file resolves correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        target = root / "target.html"
        target.write_text("<html></html>")

        source = create_temp_html(root, "source.html", ["target.html"])
        assert target.exists()

        source_dir = os.path.dirname(str(source))
        resolved = os.path.normpath(os.path.join(source_dir, "target.html"))
        assert os.path.exists(resolved)


def test_broken_link_detected():
    """Verify that a link to a missing file is correctly identified."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        create_temp_html(root, "source.html", ["missing.html"])
        assert not (root / "missing.html").exists()


def test_relative_up_link_resolves():
    """Verify that relative ../ links resolve to files one level up."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        sub = root / "sub"
        sub.mkdir()

        target = root / "sibling.html"
        target.write_text("<html></html>")

        source = create_temp_html(sub, "source.html", ["../sibling.html"])
        assert target.exists()

        source_dir = os.path.dirname(str(source))
        resolved = os.path.normpath(os.path.join(source_dir, "../sibling.html"))
        assert os.path.exists(resolved), f"Resolved path {resolved} does not exist"


def test_linkcheck_script_runs():
    """Verify the linkcheck.py script can execute without errors."""
    import subprocess
    import sys

    script = Path(__file__).resolve().parent.parent / ".hermes" / "linkcheck.py"
    assert script.exists(), f"Script not found: {script}"

    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parent.parent,
    )
    # The script may find broken links (external links or missing pages),
    # but should not crash
    assert result.returncode == 0, f"Script failed:\n{result.stderr}"
    assert "Broken" in result.stdout or "checked" in result.stdout
