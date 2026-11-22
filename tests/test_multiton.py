"""Multiton behaviour."""

from __future__ import annotations

import threading

import pytest

from pymjolnir import Multiton


def test_multiton_caches_per_key() -> None:
    """The same key returns the same object, and reset drops it."""
    built: list[str] = []

    def factory(key: str) -> str:
        """Remember each key the cache builds."""
        built.append(key)
        return key

    cache: Multiton[str] = Multiton(factory)
    assert cache.get("a") is not None
    assert cache.get("a") == "a"
    assert built == ["a"]
    cache.reset("a")
    assert cache.get("a") == "a"
    assert built == ["a", "a"]
    cache.reset()
    assert cache.get("b") == "b"


def test_empty_multiton_key() -> None:
    """An empty key is rejected before the factory runs."""
    cache: Multiton[str] = Multiton(lambda key: key)
    with pytest.raises(ValueError, match="empty"):
        cache.get("")


def test_concurrent_multiton_builds_each_key_once() -> None:
    """A key requested by several threads is constructed once."""
    counts: dict[str, int] = {"a": 0, "b": 0}
    lock = threading.Lock()

    def factory(key: str) -> str:
        """Count constructions for one key."""
        with lock:
            counts[key] += 1
        return key

    cache: Multiton[str] = Multiton(factory)
    barrier = threading.Barrier(10)

    def take(key: str) -> None:
        """Wait, then read the cached value."""
        barrier.wait()
        assert cache.get(key) == key

    keys = ["a", "b"] * 5
    threads = [threading.Thread(target=take, args=(key,)) for key in keys]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert counts == {"a": 1, "b": 1}


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
