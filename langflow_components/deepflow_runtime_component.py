"""Langflow component that talks to the DeepFlow runtime."""

from __future__ import annotations

import os

import httpx

from lfx.custom.custom_component.component import Component
from lfx.inputs.inputs import IntInput, MessageTextInput, StrInput
from lfx.schema.data import Data
from lfx.template.field.base import Output


class DeepFlowRuntimeComponent(Component):
    display_name = "DeepFlow Runtime"
    description = "Call the external DeepFlow Deep Agents runtime over HTTP."
    icon = "Bot"

    inputs = [
        StrInput(
            name="runtime_url",
            display_name="Runtime URL",
            value=os.getenv("DEEPFLOW_RUNTIME_URL", "http://127.0.0.1:8011"),
            info="Base URL of the DeepFlow runtime.",
        ),
        MessageTextInput(
            name="prompt",
            display_name="Prompt",
            info="Prompt to send to the DeepFlow runtime.",
            tool_mode=True,
        ),
        StrInput(
            name="thread_id",
            display_name="Thread ID",
            value="langflow-thread",
            info="Conversation thread identifier used by DeepFlow.",
            advanced=True,
        ),
        IntInput(
            name="timeout_seconds",
            display_name="Timeout Seconds",
            value=120,
            info="HTTP timeout for the runtime call.",
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="Response", name="response", method="run_deepflow"),
    ]

    def run_deepflow(self) -> Data:
        url = self.runtime_url.rstrip("/") + "/invoke"
        payload = {"prompt": self.prompt, "thread_id": self.thread_id}
        try:
            with httpx.Client(timeout=float(self.timeout_seconds)) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
            result = response.json()
        except httpx.HTTPStatusError as exc:
            result = {
                "error": f"DeepFlow runtime returned {exc.response.status_code}",
                "detail": exc.response.text,
            }
        except httpx.HTTPError as exc:
            result = {
                "error": "DeepFlow runtime request failed",
                "detail": str(exc),
            }
        data = Data(
            text=result.get("output_text", result.get("detail", result.get("error", ""))),
            data=result,
        )
        self.status = data
        return data
