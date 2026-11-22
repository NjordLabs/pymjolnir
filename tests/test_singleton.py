"""Singleton behaviour."""

from __future__ import annotations

import threading

from pymjolnir import singleton


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
