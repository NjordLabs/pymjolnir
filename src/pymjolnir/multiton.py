"""One instance per key."""

from __future__ import annotations

import threading
from collections.abc import Callable

from pymjolnir._guard import CallGuard


class Multiton[T]:
    """Build and cache one value per key."""

    def __init__(self, factory: Callable[[str], T]) -> None:
        """Store the factory used for a missing key.

        Args:
            factory: Called with the key the first time it is requested.
        """
        self._factory = factory
        self._items: dict[str, T] = {}
        self._lock = threading.Lock()
        self._guard = CallGuard()

    def get(self, key: str) -> T:
        """Return the cached value for ``key``, creating it when needed.

        A factory that calls this multiton again on the same thread fails
        instead of waiting on the lock. A factory that raises is not cached.

        Args:
            key: Cache key. An empty key is rejected.

        Returns:
            The cached product.

        Raises:
            ValueError: ``key`` is empty.
            RuntimeError: The factory re-entered this multiton on the same thread.
        """
        if key == "":
            raise ValueError("key must not be empty")
        if self._guard.building:
            raise RuntimeError("multiton factory re-entered the same wrapper")
        with self._lock:
            try:
                return self._items[key]
            except KeyError:
                self._guard.building = True
                try:
                    created = self._factory(key)
                finally:
                    self._guard.building = False
                self._items[key] = created
                return created

    def reset(self, key: str | None = None) -> None:
        """Drop one key, or every key when ``key`` is omitted.

        Args:
            key: Key to drop. ``None`` drops every cached value.
        """
        with self._lock:
            if key is None:
                self._items.clear()
                return
            self._items.pop(key, None)
