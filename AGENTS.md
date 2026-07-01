# DevForge — Landing Page & Blog

## Overview
DevForge is the marketing site for the Coding-Dev-Tools CLI suite. Pure HTML/CSS, hosted on GitHub Pages. 60+ blog articles, pricing, docs, and alternatives pages.

## Agent Instructions
- **CI**: Run `pytest tests/` to validate link integrity before deploying
- **Deploy**: Push to `main` triggers GitHub Pages auto-deploy
- **Content**: Blog posts are static HTML under `blog/` — edit directly
- **Tools**: Link checker lives at `.hermes/linkcheck.py`
- **Owner**: Coding-Dev-Tools / Revenue Holdings

## Key Paths
| Path | Purpose |
|------|---------|
| `blog/` | Blog articles (HTML) |
| `tests/` | Pytest link-check tests |
| `.hermes/linkcheck.py` | Link checker script |
| `.github/dependabot.yml` | Dependency updates |
