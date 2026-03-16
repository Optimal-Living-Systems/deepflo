"""FastAPI runtime for DeepFlow."""

from __future__ import annotations

from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any

from fastapi import FastAPI, HTTPException
from langchain_core.messages import AIMessage, BaseMessage
from pydantic import BaseModel, Field

from deepflow_runtime.agent import build_runtime_agent
from deepflow_runtime.config import DeepFlowSettings, get_settings
from deepflow_runtime.sqlite_compat import AsyncCompatibleSqliteSaver, open_checkpointer


class InvokeRequest(BaseModel):
    """Invocation payload for the DeepFlow runtime."""

    prompt: str = Field(min_length=1)
    thread_id: str = Field(default="deepflow-default")


class InvokeResponse(BaseModel):
    """Response payload for the DeepFlow runtime."""

    thread_id: str
    output_text: str
    message_count: int


@dataclass
class RuntimeService:
    """Manages the lifecycle of the DeepFlow runtime graph."""

    settings: DeepFlowSettings
    checkpointer: AsyncCompatibleSqliteSaver | None = None
    checkpointer_cm: Any | None = None
    agent: Any | None = None
    startup_error: str | None = None

    async def start(self) -> None:
        """Start the runtime and compile the graph."""
        self.settings.ensure_directories()
        self.checkpointer_cm = open_checkpointer(str(self.settings.sqlite_path))
        self.checkpointer = self.checkpointer_cm.__enter__()
        try:
            self.agent = build_runtime_agent(self.settings, checkpointer=self.checkpointer)
            self.startup_error = None
        except RuntimeError as exc:
            self.agent = None
            self.startup_error = str(exc)

    async def stop(self) -> None:
        """Stop the runtime and release the database handle."""
        if self.checkpointer_cm is not None:
            self.checkpointer_cm.__exit__(None, None, None)
        self.checkpointer = None
        self.checkpointer_cm = None
        self.agent = None
        self.startup_error = None

    async def invoke(self, request: InvokeRequest) -> InvokeResponse:
        """Run the graph for one user request."""
        if self.agent is None:
            if self.checkpointer is None:
                raise RuntimeError("RuntimeService.start() must be called before invoke().")
            self.agent = build_runtime_agent(self.settings, checkpointer=self.checkpointer)
            self.startup_error = None
        result = await self.agent.ainvoke(
            {"messages": [("user", request.prompt)]},
            config={"configurable": {"thread_id": request.thread_id}},
        )
        messages = result.get("messages", [])
        return InvokeResponse(
            thread_id=request.thread_id,
            output_text=extract_text(messages),
            message_count=len(messages),
        )


def extract_text(messages: list[Any]) -> str:
    """Extract the last assistant text from a LangGraph message list."""
    for message in reversed(messages):
        if isinstance(message, AIMessage):
            return _message_to_text(message)
        if isinstance(message, BaseMessage) and getattr(message, "type", "") == "ai":
            return _message_to_text(message)
    return ""


def _message_to_text(message: BaseMessage) -> str:
    """Convert a message content payload into plain text."""
    content = message.content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text", "")))
            else:
                parts.append(str(item))
        return "\n".join(part for part in parts if part)
    return str(content)


def create_app(settings: DeepFlowSettings | None = None) -> FastAPI:
    """Create the DeepFlow FastAPI app."""
    runtime_settings = settings or get_settings()
    service = RuntimeService(runtime_settings)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        await service.start()
        try:
            yield
        finally:
            await service.stop()

    app = FastAPI(title="DeepFlow Runtime", version="0.1.0", lifespan=lifespan)
    app.state.service = service

    @app.get("/health")
    async def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "provider_status": runtime_settings.provider_status(),
            "workspace_dir": str(runtime_settings.workspace_dir),
            "sqlite_path": str(runtime_settings.sqlite_path),
            "startup_error": service.startup_error,
        }

    @app.post("/invoke", response_model=InvokeResponse)
    async def invoke(request: InvokeRequest) -> InvokeResponse:
        try:
            return await service.invoke(request)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    return app
