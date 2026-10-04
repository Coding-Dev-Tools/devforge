#!/usr/bin/env python3
"""Copy only the public static site files into a Pages artifact directory."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path, PurePosixPath


ALLOWLIST = Path(".github/pages-allowlist.txt")
REQUIRED_SITE_FILES = {
    ".nojekyll",
    "404.html",
    "about.html",
    "alternatives.html",
    "blog.html",
    "blog/blog.css",
    "click-to-mcp-og.svg",
    "docs.html",
    "feed.xml",
    "index.html",
    "og-image.svg",
    "pricing.html",
    "quickstart.html",
    "releases.html",
    "robots.txt",
    "sitemap.xml",
    "start-here.html",
}


def read_patterns(source: Path) -> list[str]:
    lines = (source / ALLOWLIST).read_text(encoding="utf-8").splitlines()
    patterns = []
    for line in lines:
        pattern = line.strip()
        if not pattern or pattern.startswith("#"):
            continue
        path = PurePosixPath(pattern)
        if path.is_absolute() or ".." in path.parts or "**" in pattern or "\\" in pattern:
            raise ValueError(f"Unsafe Pages allowlist pattern: {pattern}")
        patterns.append(pattern)
    if not patterns:
        raise ValueError("Pages allowlist is empty")
    return patterns


def build_pages_artifact(source: Path, output: Path) -> set[str]:
    source = source.resolve(strict=True)
    output = output.resolve()
    if output == source:
        raise ValueError("Output directory must be separate from the repository root")
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"Output directory must be empty: {output}")

    patterns = read_patterns(source)
    selected: dict[str, Path] = {}
    for pattern in patterns:
        for candidate in source.glob(pattern):
            if candidate.is_symlink() or not candidate.is_file():
                continue
            resolved = candidate.resolve(strict=True)
            if source not in resolved.parents:
                raise ValueError(f"Allowlisted file escapes repository root: {candidate}")
            relative = candidate.relative_to(source).as_posix()
            selected[relative] = candidate

    missing = REQUIRED_SITE_FILES - selected.keys()
    if missing:
        raise ValueError(f"Required public site files are missing: {', '.join(sorted(missing))}")

    output.mkdir(parents=True, exist_ok=True)
    for relative, candidate in sorted(selected.items()):
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(candidate, target)
    return set(selected)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Repository checkout root")
    parser.add_argument("--output", type=Path, required=True, help="Empty output directory")
    args = parser.parse_args()
    copied = build_pages_artifact(args.source, args.output)
    print(f"Built Pages artifact with {len(copied)} allowlisted files")


if __name__ == "__main__":
    main()
