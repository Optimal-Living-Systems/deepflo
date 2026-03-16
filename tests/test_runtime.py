"""Runtime server unit tests."""

from __future__ import annotations

import httpx
import pytest

from deepflow_runtime.config import DeepFlowSettings
from deepflow_runtime.runtime_api import create_app, extract_text
from langchain_core.messages import AIMessage


# ---------------------------------------------------------------------------
# extract_text helpers (no I/O, always fast)
# ---------------------------------------------------------------------------

def test_extract_text_returns_last_ai_message() -> None:
    """extract_text returns the content of the most recent AIMessage."""
    messages = [
        AIMessage(content="first"),
        AIMessage(content="second"),
    ]
    assert extract_text(messages) == "second"


def test_extract_text_empty_list() -> None:
    """extract_text returns empty string when there are no messages."""
    assert extract_text([]) == ""


def test_extract_text_list_content() -> None:
    """extract_text joins multiple text parts from list-type content."""
    messages = [AIMessage(content=[{"type": "text", "text": "hello"}, {"type": "text", "text": "world"}])]
    assert extract_text(messages) == "hello\nworld"


# ---------------------------------------------------------------------------
# /health — always public, always fast
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_health_returns_ok() -> None:
    """GET /health returns 200 and status ok."""
    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.anyio
async def test_health_public_when_api_key_configured() -> None:
    """GET /health must not require auth even when DEEPFLOW_API_KEY is set."""
    app = create_app(DeepFlowSettings(api_key="secret"))
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/health")
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# /invoke — auth
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_invoke_open_when_no_api_key() -> None:
    """With no DEEPFLOW_API_KEY, /invoke is open (fails on missing model, not auth)."""
    transport = httpx.ASGITransport(app=create_app(DeepFlowSettings(api_key=None)))
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/invoke", json={"prompt": "hello"})
    assert response.status_code == 503  # past auth, no model configured


@pytest.mark.anyio
async def test_invoke_rejects_missing_token() -> None:
    """With DEEPFLOW_API_KEY set, /invoke returns 401 for missing token."""
    app = create_app(DeepFlowSettings(api_key="secret"))
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/invoke", json={"prompt": "hello"})
    assert response.status_code == 401


@pytest.mark.anyio
async def test_invoke_rejects_wrong_token() -> None:
    """With DEEPFLOW_API_KEY set, /invoke returns 401 for wrong token."""
    app = create_app(DeepFlowSettings(api_key="secret"))
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
            "/invoke",
            json={"prompt": "hello"},
            headers={"Authorization": "Bearer wrong"},
        )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_invoke_accepts_correct_token() -> None:
    """Correct Bearer token passes auth and reaches the model layer (503, not 401)."""
    app = create_app(DeepFlowSettings(api_key="secret"))
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
            "/invoke",
            json={"prompt": "hello"},
            headers={"Authorization": "Bearer secret"},
        )
    assert response.status_code == 503


# ---------------------------------------------------------------------------
# Request validation
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_invoke_rejects_empty_prompt() -> None:
    """POST /invoke with an empty prompt returns 422 Unprocessable Entity."""
    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/invoke", json={"prompt": ""})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_invoke_stream_rejects_wrong_token() -> None:
    """POST /invoke/stream returns 401 for wrong token."""
    app = create_app(DeepFlowSettings(api_key="secret"))
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
            "/invoke/stream",
            json={"prompt": "hello"},
            headers={"Authorization": "Bearer bad"},
        )
    assert response.status_code == 401
