#!/bin/sh
# Local parity for the Python quality gates. Docker is not required:
# the tools live in the project virtualenv.
set -eu

ROOT="$(CDPATH='' cd -- "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"

uv sync --frozen --group dev
uv run ruff check src tests
uv run ruff format --check src tests
uv run mypy -p pymjolnir -p tests
uv run pylint src
uv run coverage run -m pytest -q
uv run coverage report
uv run bandit -c pyproject.toml -r src -q
uv run interrogate --fail-under 95 src
uv run python - <<'PY'
import json
import subprocess
import sys

cc = json.loads(subprocess.check_output(["radon", "cc", "-j", "-s", "src"], text=True))
scores: list[int] = []

def walk(node: object) -> None:
    if isinstance(node, dict):
        complexity = node.get("complexity")
        if isinstance(complexity, int):
            scores.append(complexity)
        for child in node.values():
            walk(child)
    elif isinstance(node, list):
        for child in node:
            walk(child)

walk(cc)
if not scores:
    sys.exit("radon found no blocks")
worst = max(scores)
average = sum(scores) / len(scores)
if worst > 8 or average > 5:
    sys.exit(f"cyclomatic complexity worst={worst} avg={average:.2f}")

mi = json.loads(subprocess.check_output(["radon", "mi", "-j", "src"], text=True))
indexes: list[float] = []

def walk_mi(node: object) -> None:
    if isinstance(node, dict):
        value = node.get("mi")
        if isinstance(value, (int, float)):
            indexes.append(float(value))
        for child in node.values():
            walk_mi(child)
    elif isinstance(node, list):
        for child in node:
            walk_mi(child)

walk_mi(mi)
if not indexes:
    sys.exit("radon found no maintainability scores")
lowest = min(indexes)
mean = sum(indexes) / len(indexes)
if lowest < 40 or mean < 60:
    sys.exit(f"maintainability lowest={lowest:.2f} avg={mean:.2f}")
PY
uv run pip-audit
sh scripts/check-submodule-pins.sh
sh scripts/check-threshold-drift.sh
