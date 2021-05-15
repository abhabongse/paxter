"""
Utility class to describe the input source text.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SourceText:
    """
    Source text utility class whose instance gets passed around
    during the source text parsing.
    """
    content: str
