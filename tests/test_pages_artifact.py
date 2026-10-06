from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BUILDER = REPOSITORY_ROOT / "scripts" / "build_pages_artifact.py"


def test_pages_artifact_contains_public_site_assets_only(tmp_path):
    source = tmp_path / "source"
    output = tmp_path / "pages"
    files = {
        ".github/pages-allowlist.txt": "*.html\n*.svg\nfeed.xml\nrobots.txt\nsitemap.xml\n.nojekyll\nblog/*.html\nblog/*.css\n",
        ".nojekyll": "",
        "404.html": "404",
        "about.html": "about",
        "alternatives.html": "alternatives",
        "blog.html": "blog index",
        "blog/blog.css": "body {}",
        "blog/post.html": "post",
        "click-to-mcp-og.svg": "<svg />",
        "docs.html": "docs",
        "feed.xml": "<feed />",
        "index.html": "home",
        "og-image.svg": "<svg />",
        "pricing.html": "pricing",
        "quickstart.html": "quickstart",
        "releases.html": "releases",
        "robots.txt": "User-agent: *",
        "sitemap.xml": "<urlset />",
        "start-here.html": "start",
        "AGENTS.md": "internal instructions",
        ".hermes/linkcheck.py": "internal tool",
        ".github/workflows/ci.yml": "workflow",
        "drafts/newsletter-outreach-email.md": "private draft",
        "tests/test_example.py": "tests",
    }
    for relative, contents in files.items():
        path = source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")

    subprocess.run(
        [sys.executable, str(BUILDER), "--source", str(source), "--output", str(output)],
        check=True,
        cwd=REPOSITORY_ROOT,
    )

    actual_files = {
        path.relative_to(output).as_posix() for path in output.rglob("*") if path.is_file()
    }
    expected_files = {
        relative for relative in files if relative not in {
            "AGENTS.md",
            ".hermes/linkcheck.py",
            ".github/pages-allowlist.txt",
            ".github/workflows/ci.yml",
            "drafts/newsletter-outreach-email.md",
            "tests/test_example.py",
        }
    }
    assert actual_files == expected_files
    assert (output / "blog/post.html").read_text(encoding="utf-8") == "post"
    assert not (output / "drafts").exists()


def test_current_pages_artifact_has_no_broken_links_or_fragments(tmp_path):
    output = tmp_path / "pages"
    subprocess.run(
        [sys.executable, str(BUILDER), "--source", str(REPOSITORY_ROOT), "--output", str(output)],
        check=True,
    )
    checker = REPOSITORY_ROOT / ".hermes/linkcheck.py"
    subprocess.run([sys.executable, str(checker), "--exit-code", str(output)], check=True)
    assert not (output / "drafts/newsletter-outreach-email.md").exists()
