#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"
exec uv run deepflow mcp --transport streamable-http --host "${DEEPFLOW_MCP_HOST:-127.0.0.1}" --port "${DEEPFLOW_MCP_PORT:-8012}"
