# AI agent handoff — pymjolnir

## Identity

| Field | Value |
|-------|-------|
| Package | `pymjolnir` |
| Python | 3.13 and 3.14 |
| Pins | guardrails `1.15.0` (`2d4bb70`), scaffold `1.12.0` (`9c443ea`), pydevops (`ce31af67`) |

## Scope

Design patterns only. Logging lives in `mimirlog`. Graph execution lives in `nodeio`.

| Component | Status |
|-----------|--------|
| Registry | Implemented |
| Singleton | Implemented |
| Multiton | Implemented |
| Chain of responsibility | Implemented |

## Commands

```bash
sh scripts/check-ci-local.sh
sh scripts/check-ci-docker.sh
```

`check-ci-docker.sh` runs the same gates in `ghcr.io/pirlruc/ci-python`
(digest-pinned). That image has no `uv`, so the script installs this
package inside the container and leaves the checkout read-only. The
image is private.

## Known pitfalls

- Quality jobs pull private `ci-python` and `ci-lint`. The NjordLabs repository needs `GHCR_READ_TOKEN` and `container_username: pirlruc`.
- Submodule jobs need `GUARDRAILS_READ_TOKEN`. Dependabot submodule updates need `DEPENDABOT_GITHUB_TOKEN`.
- PyPI Trusted Publishing is configured outside the repository.

## Suggested next work

- PyPI publish (PAT-001-T2) stays open. `v0.1.1` is the GitHub Release:
  https://github.com/NjordLabs/pymjolnir/releases/tag/v0.1.1
  The wheel sha256 is
  `5999ff4b244ee0215c96f1228b042f18ad33699dbbc2964d01abd2103eaf050d`.

## Recent history

- fix(patterns): raise when a factory re-enters the same wrapper
- chore(deps): require pylint 4.0.9 and set 0.1.1
- ci: pin pydevops, skip dependabot secret jobs, add the docker gate
- docs: record 0.1.1 and close the landed pattern tasks
- docs(readme): install the v0.1.1 release wheel
- release: tag v0.1.1

*Last updated: 2026-11-22.*
