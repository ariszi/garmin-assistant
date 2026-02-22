# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## What this is
A personal MCP server wrapping two Garmin libraries:
- **garmin_mcp** — live Garmin Connect API (95+ tools). Upstream: https://github.com/Taxuspt/garmin_mcp
- **GarminDB** — local SQLite database of historical Garmin data. Upstream: https://github.com/tcgoetz/GarminDB

## Running
Start the MCP server:
```bash
uv run python main.py
```

## Updating upstream libraries
```bash
uv sync --upgrade
```

## Auth
- garmin_mcp tokens: stored at ~/.garminconnect (run `uv run garmin-mcp-auth` to re-authenticate)
- GarminDB config: ~/.GarminDb/GarminConnectConfig.json

## Sync local database
```bash
uv run garmindb_cli.py --all --download --import --analyze --latest
```

## Architecture
`main.py` creates a single FastMCP app, then:
1. Calls `init_api()` from garmin_mcp to get a Garmin Connect client
2. Imports each garmin_mcp module, calls `configure(client)` + `register_tools(app)` on each
3. Adds custom GarminDB tools using `@app.tool()` decorators directly

All print/logging goes to stderr — stdout is reserved for MCP JSON-RPC protocol.

## Adding new tools
Add `@app.tool()` decorated async functions in `main.py` inside `setup_garmindb_tools()` or a new setup function.
