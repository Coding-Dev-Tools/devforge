# DevForge — Agent System Reference

## Identity
- **Name:** DevForge CLI Tool Suite Landing Page
- **Purpose:** Landing page, documentation, pricing, alternatives, and blog for the DevForge CLI tool suite (11 developer tools)
- **Paperclip Company:** Coding-Dev-Tools
- **Tier:** 3 (Documentation/Static)

## Architecture
```
Static HTML/CSS site (no framework) → GitHub Pages deployment
Live: https://coding-dev-tools.github.io/devforge/
```

## Key Files
| File | Purpose |
|------|---------|
| `index.html` | Home page — hero, stats, feature cards, CTA |
| `pricing.html` | Free / Pro / Team / Enterprise tiers |
| `alternatives.html` | 11 comparison tables vs competitors |
| `blog.html` | 60+ articles and tutorials |
| `docs.html` | Tool documentation hub |
| `quickstart.html` | Get started in 60 seconds |
| `about.html` | The story |
| `.github/dependabot.yml` | Weekly dependency updates (pip + GitHub Actions) |
| `.hermes/linkcheck.py` | Internal link validator with CLI |
| `tests/test_linkcheck*.py` | Link checker test suite |
| `pyproject.toml` | Python project config (ruff, pytest) |

## Tools Featured (Revenue Products)
| Tool | Repo | Purpose |
|------|------|---------|
| API Contract Guardian | api-contract-guardian | Breakpoint testing for API contracts |
| SchemaForge | schemaforge | Bidirectional schema conversion (11 formats) |
| DeadCode | deadcode | Detect & remove dead code in React/Next.js |
| APIGhost | apighost | Mock API servers from OpenAPI specs |
| Envault | envault | Encrypt & sync .env secrets |
| DeployDiff | deploydiff | Preview infrastructure cost before deploy |
| ConfigDrift | configdrift | Catch config drift before production |
| json2sql | json2sql | JSON to SQL in one command |
| DataMorph | datamorph | Convert between CSV, JSON, YAML, Parquet, Avro, Protobuf |
| click-to-mcp | click-to-mcp | Turn any Python CLI into an MCP server |
| APIAuth | apiauth | Manage API keys, tokens, JWTs with rotation |

## CI/CD
- **Current:** None (missing `.github/workflows/`)
- **Needed:** GitHub Actions for:
  - Link checking (`.hermes/linkcheck.py --exit-code`)
  - HTML validation
  - Deploy to GitHub Pages on push to main
  - Dependabot already configured (`.github/dependabot.yml`)

## Testing
- Run link checker: `python -m pytest tests/ -v`
- Run link checker script directly: `python .hermes/linkcheck.py --exit-code`
- Tests: 18 tests in `tests/test_linkcheck.py`, 2 additional test files

## Environment
- No runtime environment needed (static site)
- Python 3.10+ for link checker and tests

## Constraints
- Pure HTML/CSS — no framework, no build step
- GitHub Pages deployment from `gh-pages` branch
- 60+ blog articles in HTML (not markdown)
- Atom RSS feed at `/feed.xml`

## Known Issues (from fixer-queue)
- Missing AGENTS.md ✓ (this file)
- Missing CI/CD workflows
- Missing version file (though version in pyproject.toml)

## Revenue Context
DevForge is the landing page for 11 CLI tools under Coding-Dev-Tools subsidiary. Revenue comes from the individual tools (SaaS, CLI sales, enterprise). This page drives discovery and trust.

## Autonomous Agent Notes
- Tier 3 repo — low priority for autonomous fixes
- Main value: adding CI/CD to catch broken links on PR
- Link checker already exists and tested — just needs workflow