"""
Error classes specific to Paxter language ecosystem.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from paxter.parsing.charloc import CharLoc

__all__ = [
    'PaxterBaseException',
    'PaxterConfigError', 'PaxterSyntaxError', 'PaxterRenderError',
]


class PaxterBaseException(Exception):
    """
    Base exception specific to Paxter language ecosystem.
    Positional index parameters indicates a mapping from position name
    to its indexing inside the input text.
    """
    #: Error message
    message: str
    #: A mapping from position name to :class:`LineCol` position data
    positions: dict[str, CharLoc]

    def __init__(self, message: str, **positions: CharLoc):
        self.positions = positions
        self.message = self.render(message, self.positions)
        self.args = (self.message,)  # this will make error stack more readable

    @staticmethod
    def render(message: str, positions: dict[str, CharLoc]) -> str:
        """
        Substitutes the position placeholder within the message
        with the provided positions data.
        """
        return message % {
            name: line_col.rendered
            for name, line_col in positions.items()
        }


class PaxterConfigError(PaxterBaseException):
    """
    Exception for configuration error.
    """
    pass


class PaxterSyntaxError(PaxterBaseException):
    """
    Exception for syntax error raised while parsing input text in Paxter language.
    """
    pass


class PaxterRenderError(PaxterBaseException):
    """
    Exception for parsed tree transformation error.
    """
    pass
