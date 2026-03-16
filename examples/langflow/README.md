# Langflow Examples

These example flows are generated from the current Langflow environment and the checked-in DeepFlow custom component.

## Files

- `deepflow_chat_bridge.json`
  - `Chat Input -> DeepFlow Runtime -> Chat Output`
- `deepflow_text_bridge.json`
  - `Text Input -> DeepFlow Runtime -> Chat Output`
- `deepflow_mcp_server_config.json`
  - Streamable HTTP MCP server config for DeepFlow
- `deepflow_run_flow_recipe.md`
  - Recommended `Run Flow` orchestration pattern

## Regenerate

Run this from the Langflow environment:

```bash
cd /path/to/langflow
uv run python /path/to/deepflow/scripts/generate_langflow_examples.py
```

## Import into Langflow

1. Start the DeepFlow runtime
2. Start Langflow with:

```bash
/path/to/deepflow/scripts/start_langflow.sh
```

3. Import one of the JSON files in this directory
4. Run the flow

## Run Flow orchestration

Use these bridge flows as subflows for Langflow's `Run Flow` component.

Recommended pattern:

1. Import `deepflow_text_bridge.json`
2. Save it as a reusable subflow
3. In another Langflow flow, add a `Run Flow` component
4. Select `DeepFlow Text Bridge`
5. Use `Run Flow` to orchestrate DeepFlow as one specialist inside a larger Langflow workflow

The exact `Run Flow` configuration depends on the flow IDs in your Langflow workspace, so the wrapper/orchestrator flow is documented rather than hard-coded in JSON.

## MCP Tools

Use `deepflow_mcp_server_config.json` as the reference server config for Langflow `MCP Tools`.
