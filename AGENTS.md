# DevForge Agents

## Overview
Static documentation/release site for the DevForge toolchain. Pages, blog posts, and release artifacts only.

## Quick Commands
- Install/build: `pip install -r requirements.txt && make build`
- Write posts: edit files under `blog/`, keep URLs lowercase with hyphens
- Tests: `pytest || true`

## Constraints
- Do not modify docs under `blog/` content unless fixing broken links
- Keep `_config.yml` and feed assets synced before merging
- Keep PRs small; prefer splitting content and site changes

## CI
- GitHub Pages build on push to `main`
- PR previews: enable GitHub Pages preview workflow if missing
