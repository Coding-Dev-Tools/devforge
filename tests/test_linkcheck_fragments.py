"""Check real links, fragments, assets and Pages project-relative URLs."""

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".hermes"))
from linkcheck import PageLinks, SITE_URL, check_links, document_base_url


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


def test_root_base_changes_nested_stylesheet_resolution(tmp_path):
    blog = tmp_path / "blog"
    blog.mkdir()
    (blog / "post.html").write_text('<base href="/devforge/"><link href="blog.css" rel="stylesheet">')
    (blog / "blog.css").write_text("body {}")
    # A browser requests /devforge/blog.css, not /devforge/blog/blog.css.
    assert check_links(str(tmp_path)) == 1
    (tmp_path / "blog.css").write_text("body {}")
    assert check_links(str(tmp_path)) == 0


def test_first_base_href_wins_and_is_not_a_resource_link(tmp_path):
    (tmp_path / "blog").mkdir()
    (tmp_path / "assets").mkdir()
    (tmp_path / "blog/post.html").write_text(
        '<base target="_blank"><base href="../assets/">'
        '<base href="/devforge/missing/"><a href="target.html#ok">target</a>'
    )
    (tmp_path / "assets/target.html").write_text('<h1 id="ok">Heading</h1>')
    # There is no assets/index.html. The base href itself does not fetch one.
    assert check_links(str(tmp_path)) == 0


def test_fragment_uses_base_target_instead_of_source_page(tmp_path):
    (tmp_path / "blog").mkdir()
    (tmp_path / "blog/post.html").write_text(
        '<base href="../target.html"><h1 id="section">Source</h1><a href="#section">target</a>'
    )
    (tmp_path / "target.html").write_text("No target anchor")
    assert check_links(str(tmp_path)) == 1
    (tmp_path / "target.html").write_text('<h1 id="section">Target</h1>')
    assert check_links(str(tmp_path)) == 0


def test_external_base_makes_relative_urls_external(tmp_path):
    (tmp_path / "index.html").write_text(
        '<base href="https://example.com/assets/"><a href="missing.html">external</a>'
        '<a href="https://coding-dev-tools.github.io/devforge/target.html#ok">local</a>'
    )
    (tmp_path / "target.html").write_text('<h1 id="ok">Target</h1>')
    assert check_links(str(tmp_path)) == 0


@pytest.mark.parametrize("href", ["", "data:text/html,example", "javascript:alert(1)", "http://[invalid"])
def test_empty_or_disallowed_first_base_falls_back_without_using_second_base(href):
    parser = PageLinks()
    parser.feed(f'<base href="{href}"><base href="/devforge/ignored/">')
    document_url = SITE_URL + "blog/post.html"
    assert document_base_url(parser, document_url) == document_url


def test_escaped_base_example_does_not_change_document_base():
    parser = PageLinks()
    parser.feed('<code>&lt;base href="/devforge/"&gt;</code>')
    document_url = SITE_URL + "blog/post.html"
    assert document_base_url(parser, document_url) == document_url
