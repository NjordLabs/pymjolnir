# Changelog

All notable changes to this project will be documented in this file.

Release notes are updated with [Commitizen](https://github.com/commitizen-tools/commitizen)
(`cz bump`).

## Unreleased

### Fixed

- A singleton factory that returns `None` is cached. The call guard is one module.

## 0.1.1

### Fixed

- Singleton and multiton raise `RuntimeError` when a factory calls the same wrapper again on the same thread. A constructor that fails is not cached.

### Changed

- The quality workflow tests Python 3.13 and 3.14.
- The pylint floor is 4.0.9.

### Added

- `scripts/check-ci-docker.sh` runs the quality gates in the published `ci-python` image.

## 0.1.0

### Added

- Registry, singleton, multiton, and chain of responsibility.
- Guardrails and github-scaffold submodules, and callers for the Python quality workflows.
- Project template: packaging, tooling, and release workflows.
