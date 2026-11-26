"""One instance per decorated class, guarded by a lock."""

from __future__ import annotations

import threading
from collections.abc import Callable
from typing import cast

from pymjolnir._guard import CallGuard

_MISSING = object()


class Singleton[T]:
    """Callable wrapper that builds ``cls`` at most once."""

    def __init__(self, cls: Callable[..., T]) -> None:
        """Store the wrapped callable.

        Args:
            cls: Class or callable to construct.
        """
        self._cls = cls
        self._lock = threading.Lock()
        self._guard = CallGuard()
        self._instance: T | object = _MISSING

    def __call__(self, *args: object, **kwargs: object) -> T:
        """Return the existing instance, or build it.

        Arguments after the first call are ignored. A factory that calls
        this wrapper again on the same thread fails instead of waiting on
        the lock. A constructor that raises is not cached.

        Args:
            args: Positional arguments for the first construction.
            kwargs: Keyword arguments for the first construction.

        Returns:
            The single instance.

        Raises:
            RuntimeError: The factory re-entered this wrapper on the same thread.
        """
        if self._guard.building:
            raise RuntimeError("singleton factory re-entered the same wrapper")
        with self._lock:
            cached = self._instance
            if cached is not _MISSING:
                return cast(T, cached)
            self._guard.building = True
            try:
                created = self._cls(*args, **kwargs)
            finally:
                self._guard.building = False
            self._instance = created
            return created

    def reset(self) -> None:
        """Drop the instance so the next call constructs again."""
        with self._lock:
            self._instance = _MISSING


def singleton[T](cls: Callable[..., T]) -> Singleton[T]:
    """Decorate ``cls`` so callers share one instance.

    Args:
        cls: Class or callable to wrap.

    Returns:
        A :class:`Singleton` for ``cls``.
    """
    return Singleton(cls)
