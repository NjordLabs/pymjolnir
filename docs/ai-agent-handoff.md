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

- Tag `v0.1.0` after the pull request merges. Quality on pull request 52 is green. The default-branch ruleset rejects the merge because the commits are unsigned.

## Recent history

- 2026-11-22: Transferred to NjordLabs. Adopted the scaffold. Added the four patterns. Quality is green at `96563f7`. The merge is blocked on verified commit signatures.
- docs(readme): tell callers to install the git tag once v0.1.0 exists

*Last updated: 2026-11-22.*
