"""One instance per decorated class, guarded by a lock."""

from __future__ import annotations

import threading
from collections.abc import Callable


class Singleton[T]:
    """Callable wrapper that builds ``cls`` at most once."""

    def __init__(self, cls: Callable[..., T]) -> None:
        """Store the wrapped callable.

        Args:
            cls: Class or callable to construct.
        """
        self._cls = cls
        self._lock = threading.Lock()
        self._instance: T | None = None

    def __call__(self, *args: object, **kwargs: object) -> T:
        """Return the existing instance, or build it.

        Arguments after the first call are ignored.

        Args:
            args: Positional arguments for the first construction.
            kwargs: Keyword arguments for the first construction.

        Returns:
            The single instance.
        """
        with self._lock:
            if self._instance is None:
                self._instance = self._cls(*args, **kwargs)
            return self._instance

    def reset(self) -> None:
        """Drop the instance so the next call constructs again."""
        with self._lock:
            self._instance = None


def singleton[T](cls: Callable[..., T]) -> Singleton[T]:
    """Decorate ``cls`` so callers share one instance.

    Args:
        cls: Class or callable to wrap.

    Returns:
        A :class:`Singleton` for ``cls``.
    """
    return Singleton(cls)
