from pathlib import Path


def print_banner():
    with (Path(__file__).resolve().parents[2] / "assets" / "ascii" / "deepflow_banner.txt").open(
        encoding="utf-8"
    ) as f:
        print(f.read())
