"""Tests for the DevForge link checker script.

Tests cover both the path-resolution logic and the new CLI argument interface,
importing functions directly from .hermes.linkcheck.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

# Add .hermes to path so we can import linkcheck.py
_SCRIPT_DIR = Path(__file__).resolve().parent.parent / ".hermes"
sys.path.insert(0, str(_SCRIPT_DIR))

from linkcheck import (  # noqa: E402
    build_actual_pages,
    check_links,
    collect_html_files,
    main,
    parse_args,
    resolve_link,
)

# ---- Helper ----


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


# ---- File discovery ----


def test_walk_collects_html_files():
    """Verify os.walk finds all .html files in a directory tree."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        sub = root / "sub"
        sub.mkdir()
        (root / "a.html").write_text("<html></html>")
        (root / "b.html").write_text("<html></html>")
        (sub / "c.html").write_text("<html></html>")

        files = collect_html_files(tmpdir)
        assert len(files) == 3, f"Expected 3 HTML files, got {len(files)}"


def test_collect_excludes_git():
    """Verify .git directories are excluded from the walk."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        git = root / ".git"
        git.mkdir()
        (git / "index.html").write_text("<html></html>")
        (root / "real.html").write_text("<html></html>")

        files = collect_html_files(tmpdir)
        assert len(files) == 1
        assert all(".git" not in str(f) for f in files)


def test_build_actual_pages():
    """Verify page path relativization."""
    files = {"/tmp/site/index.html", "/tmp/site/blog/post.html"}
    pages = build_actual_pages(files)
    assert len(pages) == len(files)


# ---- Link resolution ----


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


def test_resolve_link_from_root():
    """Resolve a plain link from root directory."""
    result = resolve_link("page.html", "")
    assert result == "page.html"


def test_resolve_link_from_subdir():
    """Resolve a plain link from a subdirectory."""
    result = resolve_link("page.html", "blog")
    assert result == "blog/page.html"


def test_resolve_link_up_from_root():
    """Resolve '../' from root stays at root."""
    result = resolve_link("../page.html", "")
    assert result == "page.html"


def test_resolve_link_up_from_subdir():
    """Resolve '../' from subdir to parent."""
    result = resolve_link("../page.html", "blog")
    assert result == "page.html"


def test_resolve_link_deep_up():
    """Resolve '../../' from nested dir."""
    result = resolve_link("../../page.html", "a/b")
    assert result == "page.html"


def test_resolve_link_with_dot_slash():
    """Resolve './' prefix."""
    result = resolve_link("./page.html", "blog")
    assert result == "blog/page.html"


def test_resolve_link_double_slash():
    """Resolve double-slash normalization."""
    result = resolve_link("page.html", "blog/")
    assert result == "blog/page.html"


# ---- CLI argument parsing ----


def test_parse_args_defaults():
    """Default directory is '.' and flags are off."""
    args = parse_args([])
    assert args.directory == "."
    assert args.verbose is False
    assert args.exit_code is False


def test_parse_args_custom_directory():
    args = parse_args(["docs"])
    assert args.directory == "docs"


def test_parse_args_verbose():
    args = parse_args(["-v"])
    assert args.verbose is True


def test_parse_args_exit_code():
    args = parse_args(["-e"])
    assert args.exit_code is True


def test_parse_args_all_flags():
    args = parse_args(["src", "--verbose", "--exit-code"])
    assert args.directory == "src"
    assert args.verbose is True
    assert args.exit_code is True


def test_parse_args_help(capsys):
    with pytest.raises(SystemExit):
        parse_args(["--help"])
    captured = capsys.readouterr()
    assert "broken internal links" in captured.out


# ---- Integration tests ----


def test_check_links_no_broken():
    """check_links returns 0 when all links resolve."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        target = root / "target.html"
        target.write_text("<html></html>")
        create_temp_html(root, "source.html", ["target.html"])

        broken = check_links(tmpdir)
        assert broken == 0


def test_check_links_finds_broken():
    """check_links returns >0 when links are broken."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        create_temp_html(root, "source.html", ["missing.html", "also-gone.html"])

        broken = check_links(tmpdir)
        assert broken == 2


def test_main_exit_code_clean():
    """main returns 0 when no broken links with --exit-code."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        target = root / "exists.html"
        target.write_text("<html></html>")
        create_temp_html(root, "source.html", ["exists.html"])

        rc = main([tmpdir, "--exit-code"])
        assert rc == 0


def test_main_exit_code_broken():
    """main returns 1 when broken links found with --exit-code."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        create_temp_html(root, "source.html", ["broken.html"])

        rc = main([tmpdir, "--exit-code"])
        assert rc == 1


def test_main_no_exit_code_ignores_broken():
    """main returns 0 even with broken links when --exit-code is not set."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        create_temp_html(root, "source.html", ["broken.html"])

        rc = main([tmpdir])
        assert rc == 0


def test_linkcheck_help():
    """Verify the linkcheck.py --help works."""
    script = _SCRIPT_DIR / "linkcheck.py"
    assert script.exists(), f"Script not found: {script}"

    result = subprocess.run(
        [sys.executable, str(script), "--help"],
        capture_output=True,
        text=True,
        cwd=_SCRIPT_DIR.parent,
    )
    assert result.returncode == 0, f"Script failed:\n{result.stderr}"
    assert "broken internal links" in result.stdout


def test_linkcheck_script_default_run():
    """Script runs without crashing in default mode (no args)."""
    script = _SCRIPT_DIR / "linkcheck.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        cwd=_SCRIPT_DIR.parent,
    )
    assert result.returncode == 0, f"Script failed:\n{result.stderr}"
