"""Singleton behaviour."""

from __future__ import annotations

import threading

import pytest

from pymjolnir import Singleton, singleton


def test_singleton_caches_none() -> None:
    """A factory that returns None is still cached."""
    calls = 0

    def factory() -> None:
        """Count constructions and return None."""
        nonlocal calls
        calls += 1

    wrapped = Singleton(factory)
    assert wrapped() is None
    assert wrapped() is None
    assert calls == 1


def test_singleton_reuses_the_first_instance() -> None:
    """The second call ignores new constructor arguments."""

    class Counter:
        """Counts constructions."""

        def __init__(self, value: int) -> None:
            """Store the constructor argument."""
            self.value = value

    wrapped = singleton(Counter)
    first = wrapped(1)
    second = wrapped(2)
    assert first is second
    assert second.value == 1
    wrapped.reset()
    third = wrapped(3)
    assert third is not first
    assert third.value == 3


def test_concurrent_singleton_builds_once() -> None:
    """Threads share the instance created by the first caller."""
    built = 0
    lock = threading.Lock()

    @singleton
    class Once:
        """Records how many times it is constructed."""

        def __init__(self) -> None:
            """Count this construction."""
            nonlocal built
            with lock:
                built += 1

    barrier = threading.Barrier(12)
    found: list[Once] = []

    def take() -> None:
        """Wait, then construct the singleton."""
        barrier.wait()
        found.append(Once())

    threads = [threading.Thread(target=take) for _ in range(12)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert built == 1
    assert all(item is found[0] for item in found)


def test_reentrant_singleton_raises_and_then_caches() -> None:
    """A factory that calls the wrapper again raises, and a later call caches."""
    state = {"reenter": True}
    slots: list[Singleton[Box]] = []

    class Box:
        """Constructs once the re-entrant call is turned off."""

        def __init__(self) -> None:
            """Call the wrapper again while the flag is set."""
            if state["reenter"]:
                slots[0]()
            self.ready = True

    slots.append(singleton(Box))
    wrapped = slots[0]
    with pytest.raises(RuntimeError, match="re-entered"):
        wrapped()
    state["reenter"] = False
    first = wrapped()
    second = wrapped()
    assert first is second
    assert first.ready is True


def test_failed_singleton_constructor_is_not_cached() -> None:
    """A constructor that raises leaves the wrapper empty for the next call."""
    state = {"fail": True}

    class Box:
        """Fails once, then succeeds."""

        def __init__(self) -> None:
            """Raise while the flag is set."""
            if state["fail"]:
                raise ValueError("boom")
            self.ready = True

    wrapped = singleton(Box)
    with pytest.raises(ValueError, match="boom"):
        wrapped()
    state["fail"] = False
    first = wrapped()
    second = wrapped()
    assert first is second
    assert first.ready is True
