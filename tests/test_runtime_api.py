import pytest
import httpx
from langchain_core.messages import AIMessage

from deepflow_runtime.runtime_api import create_app, extract_text


def test_extract_text_returns_latest_ai_message():
    messages = [
        AIMessage(content="first"),
        AIMessage(content=[{"type": "text", "text": "second"}]),
    ]

    assert extract_text(messages) == "second"


@pytest.mark.anyio
async def test_invoke_returns_503_without_model_credentials():
    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/invoke", json={"prompt": "hello", "thread_id": "t1"})

    assert response.status_code == 503
