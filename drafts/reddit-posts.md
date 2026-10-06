# Reddit Post Drafts — DevForge

## r/Python

**Title:** I built a CLI that converts between 11 ORM schema formats (Prisma, SQLAlchemy, Django, TypeORM, Drizzle, GraphQL, etc.)

**Body:**

Hey r/Python,

Tired of rewriting Django models to SQLAlchemy? Or Prisma schemas to Drizzle? I built SchemaForge — a CLI that converts between 11 schema formats with zero-loss roundtripping.

```bash
pip install git+https://github.com/Coding-Dev-Tools/schemaforge.git

# Django → SQLAlchemy
schemaforge convert models.py --from django --to sqlalchemy

# SQL DDL → Prisma
schemaforge convert schema.sql --from sql-ddl --to prisma

# SQLAlchemy → Drizzle (TypeScript)
schemaforge convert models.py --from sqlalchemy --to drizzle
```

Supported formats: SQL DDL, Prisma, Drizzle, TypeORM, Django, SQLAlchemy, GraphQL SDL, JSON Schema, OpenAPI 3.0, Protobuf, Avro — that's 110 direction pairs.

It preserves relationships, indexes, defaults, and constraints. 270+ tests passing.

There's also a VS Code extension (v1.7.0) with live preview, quick convert (Ctrl+Alt+S), and format detection.

GitHub: https://github.com/Coding-Dev-Tools/schemaforge
Docs: https://coding-dev-tools.github.io/devforge/docs.html#schemaforge

Also: we have another tool called click-to-mcp that wraps any Click/Typer CLI as an MCP server — useful if you want AI agents to call your Python CLIs.

GitHub: https://github.com/Coding-Dev-Tools/click-to-mcp

Both are Apache 2.0. Feedback welcome!

---

## r/cli

**Title:** click-to-mcp — wrap any Click/Typer CLI as an MCP server (AI agents can now use your CLIs)

**Body:**

Hey r/cli,

Built a tool that auto-wraps Python CLIs as MCP (Model Context Protocol) servers. Zero code changes needed.

```bash
pip install git+https://github.com/Coding-Dev-Tools/click-to-mcp.git
click-to-mcp convert my-cli-tool
```

Now your CLI is available as an MCP tool that Claude Desktop, Cursor, or any MCP client can call.

Why: MCP is how AI agents interact with tools. 66M+ FastMCP downloads. But every MCP server requires writing new code. click-to-mcp lets you reuse CLIs you already have.

Supports:
- stdio transport (for Claude Desktop)
- HTTP+SSE transport
- Streamable HTTP transport
- Click and Typer CLIs

5 releases, actively maintained.

GitHub: https://github.com/Coding-Dev-Tools/click-to-mcp

---

## r/webdev

**Title:** DeadCode — find unused exports, dead routes, and orphaned CSS in React/Next.js projects

**Body:**

Hey r/webdev,

Built a CLI that detects dead code in React and Next.js projects:

- Unused exports (functions/components that nothing imports)
- Dead API routes (endpoints with no callers)
- Orphaned CSS classes (styles with no matching elements)

```bash
pip install git+https://github.com/Coding-Dev-Tools/deadcode.git
deadcode scan ./src
```

It does static analysis — no runtime overhead. Useful for:
- Cleaning up before a refactor
- Reducing bundle size (treeshaking helps, but removing the code entirely is better)
- Auditing large codebases you inherited

Works with JavaScript and TypeScript. Open source (Apache 2.0).

GitHub: https://github.com/Coding-Dev-Tools/deadcode
Docs: https://coding-dev-tools.github.io/devforge/docs.html#deadcode

---

## r/devops

**Title:** 4 open-source CLIs for CI/CD pipelines: API contract testing, infra cost preview, config drift detection, and env sync

**Body:**

Hey r/devops,

Sharing 4 CLI tools we built for CI/CD workflows:

**1. API Contract Guardian** — catch breaking OpenAPI changes in CI
```bash
pip install git+https://github.com/Coding-Dev-Tools/api-contract-guardian.git
api-contract-guardian diff old.yaml new.yaml --check-breaking
```
Add to GitHub Actions: breaks the build if a PR introduces breaking API changes.

**2. DeployDiff** — preview infra cost before deploying
```bash
pip install git+https://github.com/Coding-Dev-Tools/deploydiff.git
deploydiff preview terraform/ --provider aws
```
Shows estimated monthly cost changes and blast radius before you apply.

**3. ConfigDrift** — detect config drift between environments
```bash
pip install git+https://github.com/Coding-Dev-Tools/configdrift.git
configdrift diff dev/ staging/ prod/ --format yaml
```
Catches when staging and prod configs diverge silently.

**4. Envault** — sync and rotate .env files
```bash
pip install git+https://github.com/Coding-Dev-Tools/envault.git
envault sync .env.production --from .env.staging
```
Diff, sync, and rotate env variables across environments.

All are open source (Apache 2.0), pip installable, with CI/CD workflow examples in the READMEs.

GitHub org: https://github.com/Coding-Dev-Tools
Docs: https://coding-dev-tools.github.io/devforge/docs.html
