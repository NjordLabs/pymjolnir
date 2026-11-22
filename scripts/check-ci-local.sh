#!/bin/sh
# Local parity for the Python quality gates. Docker is not required:
# the tools live in the project virtualenv.
set -eu

ROOT="$(CDPATH='' cd -- "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"

uv sync --frozen --extra dev
uv run ruff check src tests
uv run ruff format --check src tests
uv run mypy -p pymjolnir -p tests
uv run pylint src
uv run coverage run -m pytest -q
uv run coverage report
uv run bandit -c pyproject.toml -r src -q
uv run interrogate --fail-under 95 src
sh scripts/check-submodule-pins.sh
sh scripts/check-threshold-drift.sh
