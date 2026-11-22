"""One instance per key."""

from __future__ import annotations

import threading
from collections.abc import Callable


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

    def get(self, key: str) -> T:
        """Return the cached value for ``key``, creating it when needed.

        Args:
            key: Cache key. An empty key is rejected.

        Returns:
            The cached product.

        Raises:
            ValueError: ``key`` is empty.
        """
        if key == "":
            raise ValueError("key must not be empty")
        with self._lock:
            try:
                return self._items[key]
            except KeyError:
                created = self._factory(key)
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
