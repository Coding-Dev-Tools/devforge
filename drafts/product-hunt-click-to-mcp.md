# Product Hunt Launch Plan — click-to-mcp

## Product

**Name:** click-to-mcp
**Tagline:** Turn any Python CLI into an MCP server in 30 seconds
**Category:** Developer Tools / Open Source
**URL:** https://github.com/Coding-Dev-Tools/click-to-mcp
**Website:** https://coding-dev-tools.github.io/devforge.dev/docs.html#click-to-mcp

## Why Product Hunt?

- MCP (Model Context Protocol) is the fastest-growing AI tooling standard (66M FastMCP downloads)
- Zero competitors exist for "CLI to MCP" conversion — wide open niche
- click-to-mcp has 5 releases (v0.1.0 → v0.4.0) with streamable HTTP transport
- PH audience is early adopters who would actually use this

## Launch Timing

**Best day:** Tuesday or Wednesday (highest PH traffic)
**Best time:** 12:01 AM PST (maximizes time on front page)
**Avoid:** Weekends, US holidays, major Apple/Google launch days

## Pre-Launch Checklist

- [ ] Ensure GitHub README has clear 30-second demo (gif/video)
- [ ] Add "Featured on Product Hunt" badge to README
- [ ] Create a 60-second demo video showing:
  1. A simple Click CLI (`@click.command() def hello(name): ...`)
  2. Running `click-to-mcp convert hello`
  3. Registering the MCP server with Claude Desktop
  4. Using the tool from Claude's chat
- [ ] Prepare 5 "first comments" from team/advisors answering:
  - "What MCP servers do you use?" → click-to-mcp
  - "I wish my CLI tools were available to AI agents" → this solves that
  - "How does this compare to FastMCP?" → FastMCP requires code changes; click-to-mcp wraps existing CLIs with zero code changes
- [ ] Create maker profile on PH with photo and bio
- [ ] Line up 10+ upvoters (friends, colleagues, Discord communities)

## Product Hunt Listing

**Title:** click-to-mcp — Turn any Python CLI into an MCP server in 30 seconds

**Short description (60 chars):**
Auto-wrap Click/Typer CLIs as MCP servers for AI agents

**Full description:**

**The Problem:**
You have dozens of Python CLI tools. Your AI agent (Claude, GPT, etc.) can't use any of them — because they're CLIs, not MCP servers.

**The Solution:**
click-to-mcp automatically wraps any Click or Typer CLI as a Model Context Protocol (MCP) server. Zero code changes. One command.

```bash
pip install click-to-mcp
click-to-mcp convert my-cli-tool
```

Your CLI is now available as an MCP tool that any AI agent can call.

**Key Features:**
- **Zero code changes** — wraps existing Click/Typer CLIs automatically
- **Multiple transports** — stdio, HTTP+SSE, and streamable HTTP
- **5 releases** — actively maintained, production-ready
- **Works with Claude Desktop, Cursor, and any MCP client**
- **Open source** — Apache 2.0 license

**Why MCP?**
MCP is how AI agents interact with external tools. 66M+ FastMCP downloads prove the demand. But every MCP server requires writing new code. click-to-mcp lets you reuse the CLIs you already have.

**Who is this for?**
- CLI tool authors who want AI agents to use their tools
- DevOps teams who want AI agents to run their CLIs
- Anyone building MCP servers who'd rather wrap than rewrite

**Links:**
- GitHub: https://github.com/Coding-Dev-Tools/click-to-mcp
- Docs: https://coding-dev-tools.github.io/devforge.dev/docs.html#click-to-mcp
- Tutorial: https://coding-dev-tools.github.io/devforge.dev/blog/click-to-mcp-intro.html

**Topics:** developer-tools, open-source, ai, mcp, python

## Comment Strategy

**First comment (maker comment):**
"Hey PH! I built click-to-mcp because I was frustrated rewriting my CLIs as MCP servers. With 66M+ FastMCP downloads, there's clearly huge demand for MCP tooling — but no easy way to bridge existing CLIs to MCP. This tool does it with zero code changes. Would love your feedback!"

**Reply templates for common questions:**

Q: "How does this compare to FastMCP?"
A: "FastMCP is great for building new MCP servers from scratch. click-to-mcp is for wrapping CLIs you already have — no code changes needed. They're complementary: use FastMCP for new tools, click-to-mcp for existing ones."

Q: "What MCP clients does it work with?"
A: "Any MCP-compliant client: Claude Desktop, Cursor, Continue, Cline, etc. We support stdio (for Claude Desktop) and HTTP+SSE/streamable HTTP (for web-based clients)."

Q: "Is it production-ready?"
A: "We have 5 releases with full test coverage. The stdio transport is the most battle-tested. HTTP transports are newer but functional. We recommend starting with stdio for production use."

Q: "What CLIs does it support?"
A: "Any Click or Typer CLI. That covers the majority of Python CLI tools. If your CLI uses argparse or another framework, you'd need to port it to Click first (which is usually straightforward)."

## Post-Launch

- [ ] Add PH badge to README
- [ ] Tweet the launch with PH link
- [ ] Post to r/Python and r/MCP subreddits
- [ ] Update website with PH badge
- [ ] Track star count for 7 days post-launch
