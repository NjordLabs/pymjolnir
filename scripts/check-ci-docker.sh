#!/bin/sh
# Run the quality gates inside the published ci-python image.
# The image has no uv. The wheel is built on the host and installed
# in the container with --require-hashes. The checkout stays read-only.
# Tag in the digest comment: ghcr.io/pirlruc/ci-python:3.10.1 (linux/amd64).
# The image is private. Log in first: docker login ghcr.io
set -eu

ROOT="$(CDPATH='' cd -- "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"
IMAGE="${PYMJOLNIR_CI_IMAGE:-ghcr.io/pirlruc/ci-python@sha256:8bdd74a184074a58c75473da06fce79d890ef2ddb230011ddf70ebfb7b10778d}"

if ! command -v docker >/dev/null 2>&1; then
    echo "docker is required" >&2
    exit 1
fi
if ! docker image inspect "${IMAGE}" >/dev/null 2>&1; then
    echo "==> Pulling ${IMAGE}"
    docker pull "${IMAGE}"
fi

WHEEL_DIR="$(mktemp -d)"
trap 'rm -rf "${WHEEL_DIR}"' EXIT
uv build --wheel --out-dir "${WHEEL_DIR}" >/dev/null
wheel="$(find "${WHEEL_DIR}" -name '*.whl' -printf '%f\n')"
hash="$(sha256sum "${WHEEL_DIR}/${wheel}" | awk '{print $1}')"
printf 'pymjolnir @ file:///wheels/%s --hash=sha256:%s\n' "${wheel}" "${hash}" \
    >"${WHEEL_DIR}/requirements.txt"
uv export --frozen --no-dev --no-emit-project --no-header --hashes \
    >>"${WHEEL_DIR}/requirements.txt"

echo "==> Quality gates in ${IMAGE}"
docker run --rm \
    -v "${ROOT}:/work:ro" \
    -v "${WHEEL_DIR}:/wheels:ro" \
    -w /work \
    --user root \
    "${IMAGE}" \
    sh -c '
set -eu
mkdir -p /tmp/deps /tmp/mypy /tmp/pycache /tmp/ruff
python -m pip install -q --no-cache-dir --require-hashes --target /tmp/deps -r /wheels/requirements.txt
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
