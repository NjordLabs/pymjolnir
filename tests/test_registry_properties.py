"""Property tests for registry keys."""

from __future__ import annotations

import pytest

pytest.importorskip("hypothesis")
from hypothesis import given  # noqa: E402
from hypothesis import strategies as st  # noqa: E402

from pymjolnir import DuplicateKeyError, Registry  # noqa: E402


@given(st.text(min_size=1, max_size=40))
def test_register_then_create_returns_the_key(key: str) -> None:
    """A registered key creates the value the creator returns."""
    registry: Registry[str] = Registry()
    registry.register(key, lambda: key)
    assert registry.create(key) == key


@given(st.text(min_size=1, max_size=20))
def test_duplicate_key_is_rejected(key: str) -> None:
    """Registering one key twice raises."""
    registry: Registry[int] = Registry()
    registry.register(key, lambda: 1)
    with pytest.raises(DuplicateKeyError):
        registry.register(key, lambda: 2)
