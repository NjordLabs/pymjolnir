"""Per-thread flag that rejects a re-entrant factory."""

from __future__ import annotations

import threading


class CallGuard(threading.local):
    """Flag set while a factory for this wrapper is running."""

    def __init__(self) -> None:
        """Start outside a factory call."""
        super().__init__()
        self.building = False
