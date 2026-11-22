"""Chain of responsibility behaviour."""

from __future__ import annotations

from pymjolnir import Chain, Outcome


class Prefix:
    """Handle requests that start with a prefix."""

    def __init__(self, prefix: str) -> None:
        """Store the prefix this handler accepts.

        Args:
            prefix: Required start of the request.
        """
        self._prefix = prefix

    def try_handle(self, request: str) -> Outcome[str]:
        """Accept a request that starts with the prefix.

        Args:
            request: Text to inspect.

        Returns:
            A handled outcome, or an unhandled one.
        """
        if request.startswith(self._prefix):
            return Outcome(handled=True, value=self._prefix)
        return Outcome(handled=False)


def test_chain_stops_at_the_first_handler() -> None:
    """The second handler does not see a request the first one accepted."""
    chain: Chain[str, str] = Chain([Prefix("ab"), Prefix("a")])
    assert chain.handle("abc") == Outcome(handled=True, value="ab")


def test_chain_reports_unhandled() -> None:
    """No handler produces an unhandled outcome."""
    chain: Chain[str, str] = Chain([Prefix("z")])
    assert chain.handle("abc") == Outcome(handled=False, value=None)
    empty: Chain[str, str] = Chain([])
    assert empty.handle("abc").handled is False
