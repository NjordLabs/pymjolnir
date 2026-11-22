# AI agent handoff — pymjolnir

## Identity

| Field | Value |
|-------|-------|
| Package | `pymjolnir` |
| Python | 3.13 |
| Pins | guardrails `1.15.0` (`2d4bb70`), scaffold `1.12.0` (`9c443ea`), pydevops `3.8.0` (`8151d94`) |

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
```

## Known pitfalls

- Quality jobs pull private `ci-python` and `ci-lint`. The NjordLabs repository needs `GHCR_READ_TOKEN` and `container_username: pirlruc`.
- Submodule jobs need `GUARDRAILS_READ_TOKEN`. Dependabot submodule updates need `DEPENDABOT_GITHUB_TOKEN`.
- PyPI Trusted Publishing is configured outside the repository.

## Suggested next work

- PyPI publish stays open. `v0.1.0` is the GitHub Release.

## Recent history

- 2026-11-22: Transferred to NjordLabs. Adopted the scaffold. Added the four patterns.
- docs(readme): install the v0.1.0 release wheel
- Pull request 52 merged. Annotated tag `v0.1.0` is the release.

*Last updated: 2026-11-22.*
