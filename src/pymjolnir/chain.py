"""Pass a request along handlers until one accepts it."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Outcome[R]:
    """Whether a handler accepted a request, and the value it produced."""

    handled: bool
    value: R | None = None


class Handler[T, R](Protocol):
    """One step in a chain."""

    def try_handle(self, request: T) -> Outcome[R]:
        """Accept ``request`` or leave it for the next handler.

        Args:
            request: Value moving along the chain.

        Returns:
            An outcome whose ``handled`` flag is true when this step is done.
        """
        ...


class Chain[T, R]:
    """Try handlers in order. The first handled outcome wins."""

    def __init__(self, handlers: Sequence[Handler[T, R]]) -> None:
        """Copy the handler sequence.

        Args:
            handlers: Handlers in the order they should see a request.
        """
        self._handlers = tuple(handlers)

    def handle(self, request: T) -> Outcome[R]:
        """Run handlers until one handles ``request``.

        Args:
            request: Value passed to each handler.

        Returns:
            The first handled outcome, or an unhandled outcome.
        """
        for handler in self._handlers:
            outcome = handler.try_handle(request)
            if outcome.handled:
                return outcome
        return Outcome(handled=False)
