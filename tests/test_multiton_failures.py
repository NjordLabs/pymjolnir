"""Multiton factories that re-enter or fail."""

from __future__ import annotations

import pytest

from pymjolnir import Multiton


def test_reentrant_multiton_raises_and_then_caches() -> None:
    """A factory that calls the multiton again raises, and a later get caches."""
    state = {"reenter": True}

    class Box:
        """Holds the key the factory was asked for."""

        def __init__(self, key: str) -> None:
            """Store ``key``."""
            self.key = key

    def factory(key: str) -> Box:
        """Re-enter once, then build a box."""
        if state["reenter"]:
            cache.get(key)
        return Box(key)

    cache: Multiton[Box] = Multiton(factory)
    with pytest.raises(RuntimeError, match="re-entered"):
        cache.get("a")
    state["reenter"] = False
    first = cache.get("a")
    second = cache.get("a")
    assert first is second
    assert first.key == "a"


def test_failed_multiton_factory_is_not_cached() -> None:
    """A factory that raises does not occupy the key."""
    state = {"fail": True, "calls": 0}

    class Box:
        """Holds the key the factory was asked for."""

        def __init__(self, key: str) -> None:
            """Store ``key``."""
            self.key = key

    def factory(key: str) -> Box:
        """Fail once, then build a box."""
        state["calls"] += 1
        if state["fail"]:
            raise ValueError("boom")
        return Box(key)

    cache: Multiton[Box] = Multiton(factory)
    with pytest.raises(ValueError, match="boom"):
        cache.get("a")
    state["fail"] = False
    first = cache.get("a")
    second = cache.get("a")
    assert first is second
    assert state["calls"] == 2
