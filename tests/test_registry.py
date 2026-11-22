"""Registry behaviour."""

from __future__ import annotations

import threading

import pytest

from pymjolnir import DuplicateKeyError, Registry, UnknownKeyError


def test_create_uses_the_registered_callable() -> None:
    """A registered creator receives the arguments from create."""
    registry: Registry[tuple[int, str]] = Registry()
    registry.register("pair", lambda left, right: (left, right))
    assert registry.create("pair", 1, right="a") == (1, "a")
    assert registry.keys() == ("pair",)


def test_duplicate_and_unknown_keys() -> None:
    """Registration rejects a second creator and a missing key."""
    registry: Registry[int] = Registry()
    registry.register("n", lambda: 1)
    with pytest.raises(DuplicateKeyError):
        registry.register("n", lambda: 2)
    with pytest.raises(UnknownKeyError):
        registry.create("missing")


def test_empty_key_is_rejected() -> None:
    """An empty key is not a valid registration."""
    registry: Registry[int] = Registry()
    with pytest.raises(ValueError, match="empty"):
        registry.register("", lambda: 1)


def test_concurrent_register_and_create() -> None:
    """Creators registered from several threads stay distinct."""
    registry: Registry[int] = Registry()
    barrier = threading.Barrier(8)

    def add(index: int) -> None:
        barrier.wait()
        registry.register(str(index), lambda value=index: value)

    threads = [threading.Thread(target=add, args=(index,)) for index in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert set(registry.keys()) == {str(index) for index in range(8)}
    assert registry.create("3") == 3
