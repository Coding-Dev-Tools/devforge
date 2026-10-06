#!/usr/bin/env python3
"""DevForge static-site link checker.

Scans all HTML files under a given directory and reports broken internal links.
Designed for CI use — exits with code 0 if all links are valid, or code 1
if broken links are found (when --exit-code is passed).
"""

import argparse
import os
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


SITE_URL = "https://coding-dev-tools.github.io/devforge/"


class PageLinks(HTMLParser):
    """Parse actual HTML links and anchors, excluding escaped code examples."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.anchors = set()
        self.base_href = None

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if tag == "base" and name == "href" and self.base_href is None:
                # The first base with href wins, including an empty href.
                self.base_href = value or ""
            if value is None:
                continue
            # A base URL is a resolution directive, not a fetched resource.
            if tag != "base" and name in {"href", "src"}:
                self.links.append(value)
            if name == "id" or (tag == "a" and name == "name"):
                self.anchors.add(value)


def document_base_url(parser: PageLinks, document_url: str) -> str:
    """Resolve the first HTML base href against the document's own URL."""
    if parser.base_href is None:
        return document_url
    try:
        base_url = urljoin(document_url, parser.base_href.strip(" \t\n\r\f"))
        if urlsplit(base_url).scheme.lower() in {"data", "javascript"}:
            return document_url
        return base_url
    except ValueError:
        # Invalid bases fall back to the document URL, as in browsers.
        return document_url


def collect_html_files(root_dir: str) -> set[str]:
    """Walk root_dir and return set of all .html file paths."""
    files = set()
    for root, dirs, filenames in os.walk(root_dir):
        if ".git" in dirs:
            dirs.remove(".git")
        for f in filenames:
            if f.endswith(".html"):
                files.add(os.path.join(root, f))
    return files


def build_actual_pages(all_files: set[str]) -> set[str]:
    """Convert absolute-ish file paths to site-relative paths."""
    actual = set()
    for fp in all_files:
        rel = os.path.relpath(fp, ".").replace(os.sep, "/")
        if rel.startswith("./"):
            rel = rel[2:]
        actual.add(rel)
    return actual


def resolve_link(link: str, source_dir: str) -> str:
    """Resolve a relative href to an absolute site-relative path."""
    if link.startswith("http://") or link.startswith("https://") or link.startswith("#"):
        return link
    if link.startswith("/"):
        return link.lstrip("/")

    if source_dir:
        path = source_dir + "/" + link
    else:
        path = link

    normalized = os.path.normpath(path).replace(os.sep, "/")

    # Cap at site root: strip any leading ../ that goes above root
    while normalized.startswith("../"):
        normalized = normalized[3:]
        if normalized.startswith("/"):
            normalized = normalized[1:]

    return normalized


def check_links(root_dir: str, verbose: bool = False) -> int:
    """Scan HTML files under root_dir and report broken links.

    Returns the number of broken links found.
    """
    all_files = collect_html_files(root_dir)
    root = Path(root_dir).resolve()
    pages = {}
    for fp in all_files:
        parser = PageLinks()
        parser.feed(Path(fp).read_text(encoding="utf-8-sig", errors="replace"))
        pages[Path(fp).resolve().relative_to(root).as_posix()] = parser

    if verbose:
        print(f"Actual HTML pages: {len(pages)}")

    broken = 0
    checked = 0

    site = urlsplit(SITE_URL)
    for source_rel, parser in sorted(pages.items()):
        base_url = document_base_url(parser, SITE_URL + source_rel)
        for link in parser.links:
            target = urlsplit(urljoin(base_url, link))
            # Other projects on the same host are external to this artifact.
            if target.scheme not in {"http", "https"} or target.netloc != site.netloc:
                continue
            if not target.path.startswith(site.path):
                continue
            checked += 1
            relative = unquote(target.path[len(site.path):])
            if not relative or relative.endswith("/"):
                relative += "index.html"
            full_target = (root / relative).resolve()
            if root not in full_target.parents or not full_target.is_file():
                print(f"  BROKEN: {source_rel} -> {link} (missing file)")
                broken += 1
                continue

            # Empty fragments and #top use the browser's built-in document top.
            # Text fragments may have an ordinary anchor before :~:text=.
            fragment = unquote(target.fragment.split(":~:", 1)[0])
            if not fragment or fragment.lower() == "top":
                continue
            if full_target.suffix.lower() not in {".html", ".htm", ".svg"}:
                continue
            target_parser = pages.get(relative)
            if target_parser is None:
                target_parser = PageLinks()
                target_parser.feed(full_target.read_text(encoding="utf-8-sig", errors="replace"))
            if fragment not in target_parser.anchors:
                print(f"  BROKEN: {source_rel} -> {link} (missing fragment)")
                broken += 1

    if verbose or broken > 0:
        print(f"\nChecked {checked} links, found {broken} broken")

    return broken


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Check for broken internal links in DevForge static HTML files.",
        epilog="Example: python linkcheck.py --exit-code --verbose",
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Root directory to scan for HTML files (default: %(default)s)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print page count summary and status messages",
    )
    parser.add_argument(
        "-e", "--exit-code",
        action="store_true",
        help="Exit with code 1 if any broken links are found (for CI use)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Entry point with optional argv injection (for testing)."""
    args = parse_args(argv)
    broken = check_links(args.directory, verbose=args.verbose)
    if args.exit_code and broken > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
