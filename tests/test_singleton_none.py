"""A singleton factory may return None."""

from __future__ import annotations

from pymjolnir import Singleton


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
