# Editor Integration

DeepFlow exposes an ACP server for editor-native coding workflows.

## Launch command

Any ACP-capable editor should be pointed at:

```bash
/absolute/path/to/deepflow/scripts/start_acp.sh
```

This script:
- resolves the DeepFlow repo root dynamically
- starts `uv run deepflow acp`
- uses the same `.env` loading path as the CLI and runtime

## Zed

Zed supports custom ACP agents through `agent_servers` in `settings.json`.

Use [zed-settings.example.json](zed-settings.example.json) as the starting point, then replace `/absolute/path/to/deepflow` with your real checkout path.

Zed debugging tip:
- use `dev: open acp logs` from the Command Palette to inspect ACP traffic

## VS Code

VS Code is the fastest IDE path on this machine because it is already installed and supports MCP.

Use the workspace config at [../.vscode/mcp.json](../.vscode/mcp.json) when the DeepFlow repo is open in VS Code.

That config launches:

```bash
./scripts/start_mcp_stdio.sh
```

Available MCP tools:
- `deepflow_research`
- `deepflow_status`

## Approval modes

DeepFlow ACP exposes three session modes:

- `ask_before_edits`: ask before edits, plans, and shell execution
- `accept_edits`: auto-accept edits, still ask before plans and shell execution
- `accept_everything`: auto-accept all tool calls

## Current state

- ACP server boot is verified
- MCP server startup and tool calls are verified
- Langflow-side MCP client compatibility is verified
- VS Code MCP is the primary validated IDE path for this project
