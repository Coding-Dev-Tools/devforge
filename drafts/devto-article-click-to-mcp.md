# From CLI to MCP Server in 60 Seconds: A Tutorial

> How to auto-wrap any Python CLI as an MCP server for Claude Code, Cursor, and AI agents — without writing a single line of MCP code.

---

## The Problem

You've got a perfectly good CLI tool. Maybe it's a deployment checker, a database migrator, or an API contract validator. You want AI coding agents like Claude Code or Cursor to be able to use it as an MCP tool.

But converting a CLI to MCP means:
1. Learning the MCP protocol
2. Writing boilerplate server code
3. Mapping every command/option manually
4. Maintaining two code paths

There's a better way.

## Enter click-to-mcp

[click-to-mcp](https://github.com/Coding-Dev-Tools/click-to-mcp) introspects your Click or typer CLI at runtime and auto-generates MCP tools from every command, argument, and option. Zero code changes. Zero annotations. Zero boilerplate.

## Tutorial: Wrap Your CLI in 60 Seconds

### Step 1: Install

**Via pip (GitHub):**
```bash
pip install git+https://github.com/Coding-Dev-Tools/click-to-mcp.git
```

**Via Homebrew (macOS/Linux):**
```bash
brew tap Coding-Dev-Tools/tap
brew install click-to-mcp
```

**Via Scoop (Windows):**
```bash
scoop bucket add Coding-Dev-Tools https://github.com/Coding-Dev-Tools/scoop-bucket
scoop install click-to-mcp
```

For HTTP transport (needed by web-based MCP clients):
```bash
pip install "click-to-mcp[http] @ git+https://github.com/Coding-Dev-Tools/click-to-mcp.git"
```

### Step 2: Discover

See what Click/typer CLIs are available in your environment:

```bash
click-to-mcp discover
```

### Step 3: Serve

```bash
click-to-mcp serve your-cli-name
```

That's it. Your CLI is now an MCP server.

## Real Example: api-contract-guardian

Let's wrap [api-contract-guardian](https://github.com/Coding-Dev-Tools/api-contract-guardian) — an OpenAPI contract testing CLI — as an MCP server.

```bash
# Install the tools
pip install git+https://github.com/Coding-Dev-Tools/api-contract-guardian.git
pip install git+https://github.com/Coding-Dev-Tools/click-to-mcp.git

# Verify discovery
click-to-mcp discover

# Serve
click-to-mcp serve api-contract-guardian
```

### Configure Claude Code

In `.claude/settings.json`:
```json
{
  "mcpServers": {
    "api-contract-guardian": {
      "command": "click-to-mcp",
      "args": ["serve", "api-contract-guardian"]
    }
  }
}
```

Now when you say "validate my API contract" to Claude Code, it automatically calls the `acg_validate` MCP tool with the right arguments.

### Configure Cursor

In `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "api-contract-guardian": {
      "command": "click-to-mcp",
      "args": ["serve", "api-contract-guardian"]
    }
  }
}
```

## What Gets Mapped

| Click Concept | MCP Mapping |
|---|---|
| `@click.command()` | MCP tool |
| `@click.argument()` | Required input property |
| `@click.option()` | Optional input property with default |
| `click.Choice` | JSON Schema `enum` |
| `click.INT/FLOAT` | JSON Schema `integer`/`number` |
| `click.BOOL` / `is_flag` | JSON Schema `boolean` |
| Nested `click.Group` | Prefixed tools (`group_command`) |

## Advanced: HTTP Transport

For web-based MCP clients, use the HTTP+SSE transport:

```bash
click-to-mcp serve-http api-contract-guardian --port 8000
```

This serves the MCP protocol over Server-Sent Events (SSE), compatible with any MCP client that supports HTTP transport.

## Real-World Use Cases

1. **CI Pipeline Integration**: Wrap your testing CLI as MCP, let AI agents run contract tests during code review
2. **Database Operations**: Wrap json2sql as MCP, let AI agents generate and execute SQL migrations
3. **Infrastructure**: Wrap deploydiff as MCP, preview deployment costs from inside your IDE
4. **Configuration Management**: Wrap configdrift as MCP, detect config drift without leaving your editor

## Performance

click-to-mcp runs with minimal overhead because:
- It introspects CLIs at import time, not on every tool call
- The MCP protocol uses efficient JSON-RPC
- stdio transport has near-zero latency

## Limitations

- Currently supports Click and typer CLIs only (argparse support is on the roadmap)
- Dynamic option values (callbacks) are evaluated at startup
- Requires the CLI to be importable in Python

## Conclusion

You don't need to rewrite your CLIs to make them MCP-compatible. click-to-mcp bridges the gap between the CLI tools you already love and the AI-powered development workflow of the future.

Try it today:
```bash
pip install git+https://github.com/Coding-Dev-Tools/click-to-mcp.git
click-to-mcp discover
click-to-mcp serve your-cli
```

**GitHub**: https://github.com/Coding-Dev-Tools/click-to-mcp
**Landing Page**: https://coding-dev-tools.github.io/devforge/

---

*Part of the Revenue Holdings developer tool ecosystem — api-contract-guardian, json2sql, deploydiff, configdrift, and more.*
