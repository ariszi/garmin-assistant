# TODO — Garmin Assistant

Task tracker for this project. The server can update + push this file
(`/opt/stacks/garmin-mcp` on the homeserver). Newest work at the bottom of each list.

## 🔜 Deployment (homeserver — remote SSE MCP)

- [ ] One-time Garmin login on the server (creates reusable tokens):
      `cd /opt/stacks/garmin-mcp/repo && ~/.local/bin/uv run garmin-mcp-auth --token-path /opt/stacks/garmin-mcp/tokens`
- [ ] Provide a Tailscale auth key for the `garmin` node, fill `.env`, start the stack
- [ ] Verify the SSE endpoint `https://garmin.chinchilla-company.ts.net/sse` serves the tools
- [ ] Register on the Mac: `claude mcp add --transport sse garmin https://garmin.chinchilla-company.ts.net/sse`
- [ ] Tailscale admin → disable key-expiry on the `garmin` node

## 🔜 Code / features

- [ ] Bake SSE transport into the repo itself (currently an external `server_sse.py`
      wrapper on the server runs `app.run(transport="sse")`)
- [ ] Enable the GarminDB local-history tools: provide
      `~/.GarminDb/GarminConnectConfig.json` + run an initial sync (currently skipped on
      startup if unconfigured)
- [ ] Make `sync_garmindb` robust — it shells `uv run garmindb_cli.py` from the cwd;
      use the installed CLI path / proper invocation instead
- [ ] Add a readiness/health check endpoint
- [ ] Document the remote-SSE-on-homeserver deployment in `README` / `CLAUDE.md`

## ✅ Done

- [x] Containerized (Python 3.12 + uv, git deps), built image
- [x] `server_sse.py` wrapper (stdio → SSE) + Tailscale sidecar compose
- [x] Confirmed transport: library supports `stdio`/`sse` only → using SSE
