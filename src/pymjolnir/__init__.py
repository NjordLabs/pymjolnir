"""Design patterns for Python services.

The registry, singleton, multiton, and chain of responsibility here follow
the same split as the C++ ``mjolnir`` library: one concern, no application
framework.
"""

from pymjolnir.chain import Chain, Handler, Outcome
from pymjolnir.multiton import Multiton
from pymjolnir.registry import DuplicateKeyError, Registry, UnknownKeyError
from pymjolnir.singleton import Singleton, singleton

__all__ = [
    "Chain",
    "DuplicateKeyError",
    "Handler",
    "Multiton",
    "Outcome",
    "Registry",
    "Singleton",
    "UnknownKeyError",
    "singleton",
]
