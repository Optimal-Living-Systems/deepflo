"""Generate Langflow example flow assets for DeepFlow."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "examples" / "langflow"
COMPONENTS_DIR = REPO_ROOT / "langflow_components"

sys.path.insert(0, str(COMPONENTS_DIR))

from deepflow_runtime_component import DeepFlowRuntimeComponent  # noqa: E402
from lfx.components.input_output import ChatInput, ChatOutput, TextInputComponent  # noqa: E402
from lfx.graph import Graph  # noqa: E402


def build_chat_bridge_flow() -> dict:
    """Build a chat-oriented DeepFlow bridge flow."""
    chat_input = ChatInput().set(should_store_message=False)
    bridge = DeepFlowRuntimeComponent().set(
        runtime_url="http://127.0.0.1:8011",
        thread_id="deepflow-chat-bridge",
        timeout_seconds=120,
        prompt=chat_input.message_response,
    )
    chat_output = ChatOutput().set(input_value=bridge.run_deepflow)
    graph = Graph(start=chat_input, end=chat_output)
    return graph.dump(
        name="DeepFlow Chat Bridge",
        description="ChatInput -> DeepFlow Runtime -> ChatOutput",
    )


def build_text_bridge_flow() -> dict:
    """Build a text-in DeepFlow bridge flow with chat output."""
    text_input = TextInputComponent().set(input_value="Research the latest LangGraph release notes.")
    bridge = DeepFlowRuntimeComponent().set(
        runtime_url="http://127.0.0.1:8011",
        thread_id="deepflow-text-bridge",
        timeout_seconds=120,
        prompt=text_input.text_response,
    )
    chat_output = ChatOutput().set(
        input_value=bridge.run_deepflow,
        should_store_message=False,
    )
    graph = Graph(start=text_input, end=chat_output)
    return graph.dump(
        name="DeepFlow Text Bridge",
        description="TextInput -> DeepFlow Runtime -> ChatOutput",
    )


def write_flow(filename: str, payload: dict) -> None:
    """Write one flow payload to disk."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    path.write_text(json.dumps(payload, indent=2))


def main() -> None:
    """Generate all checked-in Langflow example assets."""
    write_flow("deepflow_chat_bridge.json", build_chat_bridge_flow())
    write_flow("deepflow_text_bridge.json", build_text_bridge_flow())


if __name__ == "__main__":
    main()
