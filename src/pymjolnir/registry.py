"""Keyed creators. One registry owns one product type."""

from __future__ import annotations

import threading
from collections.abc import Callable


class DuplicateKeyError(KeyError):
    """A creator is already registered for this key."""


class UnknownKeyError(KeyError):
    """No creator is registered for this key."""


class Registry[T]:
    """Create products from a key. Duplicate keys are rejected."""

    def __init__(self) -> None:
        """Start with no creators."""
        self._creators: dict[str, Callable[..., T]] = {}
        self._lock = threading.Lock()

    def register(self, key: str, creator: Callable[..., T]) -> None:
        """Store ``creator`` under ``key``.

        Args:
            key: Non-empty name used by :meth:`create`.
            creator: Called with the arguments passed to :meth:`create`.

        Raises:
            ValueError: ``key`` is empty.
            DuplicateKeyError: ``key`` is already registered.
        """
        if key == "":
            raise ValueError("key must not be empty")
        with self._lock:
            if key in self._creators:
                raise DuplicateKeyError(key)
            self._creators[key] = creator

    def create(self, key: str, *args: object, **kwargs: object) -> T:
        """Build the product registered at ``key``.

        Args:
            key: Name passed to :meth:`register`.
            args: Positional arguments for the creator.
            kwargs: Keyword arguments for the creator.

        Returns:
            The object the creator returned.

        Raises:
            UnknownKeyError: ``key`` is not registered.
        """
        with self._lock:
            try:
                creator = self._creators[key]
            except KeyError as exc:
                raise UnknownKeyError(key) from exc
        return creator(*args, **kwargs)

    def keys(self) -> tuple[str, ...]:
        """Return the registered keys in insertion order."""
        with self._lock:
            return tuple(self._creators)
