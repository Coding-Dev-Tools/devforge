"""Check real links, fragments, assets and Pages project-relative URLs."""

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".hermes"))
from linkcheck import check_links


@pytest.mark.parametrize("link", ["#missing", "target.html#missing", "target.html?q=1#missing"])
def test_missing_fragments_fail(tmp_path, link):
    (tmp_path / "index.html").write_text(f"<a href='{link}'>link</a>")
    (tmp_path / "target.html").write_text('<h1 id="present">Heading</h1>')
    assert check_links(str(tmp_path)) == 1


def test_valid_decoded_fragments_and_legacy_anchors(tmp_path):
    (tmp_path / "index.html").write_text(
        '<h1 id="local">Heading</h1><a href="#local">local</a>'
        '<a href="target.html?x=1&amp;y=2#hello%20world">target</a>'
        '<a href="target.html#legacy">legacy</a><a href="#top">top</a>'
        '<a href="#:~:text=Heading">text fragment</a>'
    )
    (tmp_path / "target.html").write_text('<h1 id="hello world">Heading</h1><a name="legacy"></a>')
    assert check_links(str(tmp_path)) == 0


def test_missing_directory_index_fails(tmp_path):
    (tmp_path / "index.html").write_text('<a href="/devforge/blog/">Blog</a>')
    (tmp_path / "blog").mkdir()
    assert check_links(str(tmp_path)) == 1
    (tmp_path / "blog/index.html").write_text("Blog")
    assert check_links(str(tmp_path)) == 0


def test_same_site_absolute_urls_and_assets_are_checked(tmp_path):
    (tmp_path / "index.html").write_text(
        '<a href="https://coding-dev-tools.github.io/devforge/target.html#ok">target</a>'
        '<img src="missing.svg" alt="missing">'
    )
    (tmp_path / "target.html").write_text('<h1 id="ok">Heading</h1>')
    assert check_links(str(tmp_path)) == 1
    (tmp_path / "missing.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
    assert check_links(str(tmp_path)) == 0


def test_external_links_and_escaped_examples_are_not_local_links(tmp_path):
    (tmp_path / "index.html").write_text(
        '<a href="https://example.com/missing.html">external</a>'
        '<a href="mailto:someone@example.com">email</a>'
        '<a href="//example.com/missing.html">external</a>'
        '<code>&lt;a href="missing.html"&gt;</code>'
    )
    assert check_links(str(tmp_path)) == 0


def test_github_compatibility_wrapper_reports_broken_links(tmp_path):
    (tmp_path / "index.html").write_text('<a href="#missing">broken</a>')
    wrapper = Path(__file__).resolve().parents[1] / ".github/scripts/linkcheck.py"
    result = subprocess.run([sys.executable, str(wrapper), str(tmp_path), "--exit-code"], capture_output=True)
    assert result.returncode == 1
    assert b"missing fragment" in result.stdout
