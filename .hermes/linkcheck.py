#!/usr/bin/env python3
"""DevForge static-site link checker.

Scans all HTML files under a given directory and reports broken internal links.
Designed for CI use — exits with code 0 if all links are valid, or code 1
if broken links are found (when --exit-code is passed).
"""

import argparse
import os
import re
import sys


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
    actual_pages = build_actual_pages(all_files)

    if verbose:
        print(f"Actual HTML pages: {len(actual_pages)}")

    broken = 0
    checked = 0

    for fp in sorted(all_files):
        with open(fp, encoding="utf-8", errors="replace") as f:
            content = f.read()

        links = re.findall(r'href="([^"]+\.html)"', content)

        source_rel = os.path.relpath(fp, root_dir).replace(os.sep, "/")
        source_dir = os.path.dirname(source_rel)
        if source_dir == ".":
            source_dir = ""

        for link in links:
            checked += 1
            if link.startswith("http://") or link.startswith("https://"):
                continue
            if link.startswith("#"):
                continue

            resolved = resolve_link(link, source_dir)
            target_path = resolved.replace("/", os.sep)

            full_target = os.path.join(root_dir, target_path) if root_dir != "." else target_path
            if not os.path.exists(full_target):
                print(f"  BROKEN: {source_rel} -> {link}")
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
