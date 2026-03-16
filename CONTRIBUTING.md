# Contributing

This repository is currently in active build-out. Contributions should preserve the split-stack design:

- Langflow stays isolated in its own environment.
- DeepFlow owns the current `deepagents` runtime.
- Integration between them happens over HTTP today.

## Local workflow

```bash
cd /home/joel/deepflow
uv sync --extra dev
uv run pytest
uv run deepflow doctor
```

## Before opening a pull request

1. Update or add docs for any user-visible behavior.
2. Keep `.env`, `data/`, and `workspace/` out of version control.
3. Note whether a change affects:
   - runtime API
   - Langflow component
   - ACP / editor workflow
   - testing and verification
4. If you touch integration behavior, update [docs/status.md](/home/joel/deepflow/docs/status.md).

## Current priorities

- Live testing with a configured model provider
- Langflow example flows
- MCP wrapper around DeepFlow
- PostgreSQL-backed Langflow deployment
- Dockerized full-stack workflow
