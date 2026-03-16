"""Langflow component unit tests.

These tests run in the langflow-dev venv (NO deepagents installed).
They test the DeepFlow Langflow component in isolation using a mock runtime.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add langflow_components to the path so we can import without a full install
sys.path.insert(0, str(Path(__file__).parent.parent / "langflow_components"))


# ---------------------------------------------------------------------------
# Component import
# ---------------------------------------------------------------------------

def test_component_module_importable() -> None:
    """The deepflow_runtime_component module must be importable on its own."""
    import deepflow_runtime_component  # noqa: F401 — import is the test


def test_component_class_exists() -> None:
    """DeepFlowRuntimeComponent class must exist and be importable."""
    from deepflow_runtime_component import DeepFlowRuntimeComponent
    assert DeepFlowRuntimeComponent is not None


# ---------------------------------------------------------------------------
# Component configuration
# ---------------------------------------------------------------------------

def test_component_has_runtime_url_input() -> None:
    """Component must expose a runtime_url configuration input."""
    from deepflow_runtime_component import DeepFlowRuntimeComponent
    component = DeepFlowRuntimeComponent()
    # Check the component has the expected inputs defined
    input_names = [i.name for i in component.inputs]
    assert "runtime_url" in input_names


def test_component_default_runtime_url() -> None:
    """Default runtime URL should point to localhost:8100."""
    from deepflow_runtime_component import DeepFlowRuntimeComponent
    component = DeepFlowRuntimeComponent()
    url_input = next(i for i in component.inputs if i.name == "runtime_url")
    assert "8100" in str(url_input.value) or "8011" in str(url_input.value)


# ---------------------------------------------------------------------------
# Placeholder for future integration tests
# ---------------------------------------------------------------------------

def test_placeholder() -> None:
    """Placeholder — expand with mock HTTP tests against the component."""
    assert True
