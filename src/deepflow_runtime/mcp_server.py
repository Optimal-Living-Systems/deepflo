"""MCP server for DeepFlow."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp.server.fastmcp import Context, FastMCP

from deepflow_runtime.config import get_settings
from deepflow_runtime.runtime_api import InvokeRequest, RuntimeService

SERVER_INSTRUCTIONS = (
    "DeepFlow MCP exposes the DeepFlow runtime as MCP tools. "
    "Use it for research-grade Deep Agents access from IDEs and Langflow MCP clients. "
    "Prefer `deepflow_research` for prompt execution and `deepflow_status` for diagnostics."
)

mcp = FastMCP(
    "DeepFlow",
    instructions=SERVER_INSTRUCTIONS,
    stateless_http=True,
    json_response=True,
)

_service: RuntimeService | None = None
_service_lock: asyncio.Lock | None = None


def _service_guard() -> asyncio.Lock:
    global _service_lock
    if _service_lock is None:
        _service_lock = asyncio.Lock()
    return _service_lock


async def get_runtime_service() -> RuntimeService:
    """Return a started singleton runtime service for MCP tool calls."""
    global _service
    if _service is not None:
        return _service
    async with _service_guard():
        if _service is None:
            service = RuntimeService(get_settings())
            await service.start()
            _service = service
    return _service


@mcp.tool()
async def deepflow_research(
    prompt: str,
    thread_id: str = "deepflow-mcp",
    ctx: Context | None = None,
) -> dict[str, Any]:
    """Run one prompt through the DeepFlow runtime and return structured output."""
    if ctx is not None:
        await ctx.info(f"Invoking DeepFlow on thread '{thread_id}'")
    service = await get_runtime_service()
    response = await service.invoke(InvokeRequest(prompt=prompt, thread_id=thread_id))
    payload = response.model_dump()
    if ctx is not None:
        await ctx.info(f"DeepFlow completed with {payload['message_count']} messages")
    return payload


@mcp.tool()
async def deepflow_status() -> dict[str, Any]:
    """Return runtime configuration and provider status for DeepFlow."""
    settings = get_settings()
    service = await get_runtime_service()
    return {
        "status": "ok",
        "model": settings.model or "auto",
        "provider_status": settings.provider_status(),
        "workspace_dir": str(settings.workspace_dir),
        "sqlite_path": str(settings.sqlite_path),
        "startup_error": service.startup_error,
    }


@mcp.resource("deepflow://health")
async def deepflow_health_resource() -> str:
    """Return a compact health summary for clients that browse resources."""
    payload = await deepflow_status()
    return (
        f"status={payload['status']}\n"
        f"model={payload['model']}\n"
        f"startup_error={payload['startup_error']}\n"
        f"provider_status={payload['provider_status']}"
    )


@mcp.prompt()
def research_prompt(topic: str) -> str:
    """Create a DeepFlow-oriented research prompt."""
    return (
        "Research the following topic and produce a concise, source-aware summary "
        f"with clear next steps: {topic}"
    )


def run_mcp_server(*, transport: str, host: str, port: int) -> None:
    """Run the FastMCP server on the requested transport."""
    if transport not in {"stdio", "streamable-http"}:
        msg = "transport must be 'stdio' or 'streamable-http'"
        raise ValueError(msg)
    mcp.settings.host = host
    mcp.settings.port = port
    mcp.run(transport=transport)
