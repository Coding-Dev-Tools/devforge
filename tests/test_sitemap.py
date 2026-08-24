"""Regression tests: sitemap.xml must exactly cover the site's real pages.

Every non-404 HTML file in the repo must have a <loc> entry, and every
<loc> must resolve to a real page (index.html is represented as "/").
"""

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITEMAP = REPO / "sitemap.xml"
BASE = "https://coding-dev-tools.github.io/devforge/"
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def _actual_pages():
    pages = set()
    for root, dirs, files in os.walk(REPO):
        rel_root = Path(root).relative_to(REPO)
        dirs[:] = [d for d in dirs if d not in (".git", "drafts", ".hermes", "tests")]
        for fn in files:
            if fn.endswith(".html") and fn != "404.html":
                p = str(rel_root / fn).replace(os.sep, "/")
                pages.add(BASE if p == "index.html" else BASE + p)
    return pages


def _sitemap_urls():
    tree = ET.parse(SITEMAP)
    return {e.text for e in tree.getroot().iter(NS + "loc")}


def test_sitemap_parses():
    ET.parse(SITEMAP)


def test_sitemap_covers_every_page():
    missing = _actual_pages() - _sitemap_urls()
    assert not missing, f"pages missing from sitemap.xml: {sorted(missing)}"


def test_sitemap_has_no_stale_urls():
    stale = _sitemap_urls() - _actual_pages()
    assert not stale, f"stale sitemap.xml URLs with no page: {sorted(stale)}"


def test_no_duplicate_locs():
    urls = re.findall(r"<loc>(.*?)</loc>", SITEMAP.read_text(encoding="utf-8"))
    assert len(urls) == len(set(urls))
