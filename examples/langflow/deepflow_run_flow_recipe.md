# DeepFlow Run Flow Recipe

Use this recipe to orchestrate DeepFlow as a specialist subflow in Langflow.

## Recommended pattern

1. Import `deepflow_text_bridge.json`
2. Save it as `DeepFlow Text Bridge`
3. Create a parent flow
4. Add a `Run Flow` component
5. Select `DeepFlow Text Bridge`
6. Pass the task prompt into that subflow
7. Route the returned message into downstream Langflow components

## When to use this pattern

- when DeepFlow is one specialist inside a larger agent graph
- when you want to separate orchestration from deep research execution
- when you want a reusable DeepFlow subflow instead of wiring the runtime node repeatedly

## Alternative pattern

If you want DeepFlow exposed as tools rather than a subflow, use Langflow `MCP Tools` with `deepflow_mcp_server_config.json`.
