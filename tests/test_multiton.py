"""Multiton behaviour."""

from __future__ import annotations

import threading

import pytest

from pymjolnir import Multiton


def test_multiton_caches_per_key() -> None:
    """The same key returns the same object, and reset drops it."""
    built: list[str] = []

    def factory(key: str) -> str:
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
        with lock:
            counts[key] += 1
        return key

    cache: Multiton[str] = Multiton(factory)
    barrier = threading.Barrier(10)

    def take(key: str) -> None:
        barrier.wait()
        assert cache.get(key) == key

    keys = ["a", "b"] * 5
    threads = [threading.Thread(target=take, args=(key,)) for key in keys]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert counts == {"a": 1, "b": 1}
