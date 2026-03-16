"""CLI banner support for DeepFlow."""

from __future__ import annotations

from pathlib import Path


def print_banner() -> None:
    """Print the shared DeepFlow ASCII banner."""
    banner_path = Path(__file__).resolve().parents[3] / "assets" / "ascii" / "deepflow_banner.txt"
    print(banner_path.read_text(encoding="utf-8"))
