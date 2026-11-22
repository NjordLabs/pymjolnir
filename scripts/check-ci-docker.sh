#!/bin/sh
# Run the quality gates inside the published ci-python image.
# The image has no uv. The checkout is mounted read-only and
# dependencies are installed only inside the container.
# Tag in the digest comment: ghcr.io/pirlruc/ci-python:3.3.0 (linux/amd64).
# The image is private. Log in first: docker login ghcr.io
set -eu

ROOT="$(CDPATH='' cd -- "$(dirname "$0")/.." && pwd)"
IMAGE="${PYMJOLNIR_CI_IMAGE:-ghcr.io/pirlruc/ci-python@sha256:894d5ae1d9bd55d68262f4ed65cd6f57d7186038d7e8e8668dba443ee0ebfbbd}"

if ! command -v docker >/dev/null 2>&1; then
    echo "docker is required" >&2
    exit 1
fi
if ! docker image inspect "${IMAGE}" >/dev/null 2>&1; then
    echo "==> Pulling ${IMAGE}"
    docker pull "${IMAGE}"
fi

echo "==> Quality gates in ${IMAGE}"
docker run --rm \
    -v "${ROOT}:/work:ro" \
    -w /work \
    --user root \
    "${IMAGE}" \
    sh -c '
set -eu
mkdir -p /tmp/pkg /tmp/deps /tmp/mypy /tmp/pycache /tmp/ruff
cp pyproject.toml README.md LICENSE /tmp/pkg/
cp -a src /tmp/pkg/src
python -m pip install -q --no-cache-dir --target /tmp/deps /tmp/pkg
export PYTHONPATH=/tmp/deps
export COVERAGE_FILE=/tmp/.coverage
export MYPY_CACHE_DIR=/tmp/mypy
export PYTHONPYCACHEPREFIX=/tmp/pycache
export RUFF_CACHE_DIR=/tmp/ruff
export PYTEST_ADDOPTS="-o cache_dir=/tmp/pytest"
ruff check src tests
ruff format --check src tests
mypy -p pymjolnir -p tests
pylint src
coverage run -m pytest -q
coverage report
bandit -c pyproject.toml -r src -q
interrogate --fail-under 95 src
sh scripts/check-submodule-pins.sh
sh scripts/check-threshold-drift.sh
'
