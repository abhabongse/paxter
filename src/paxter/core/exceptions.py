"""
Exceptions specific to Paxter language ecosystem.
"""
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from paxter.core.line_col import LineCol

__all__ = [
    'PaxterBaseException',
    'PaxterConfigError', 'PaxterSyntaxError', 'PaxterRenderError',
]


class PaxterBaseException(Exception):
    """
    Base exception specific to Paxter language ecosystem.
    """
    message: str
    positions: Dict[str, 'LineCol']

    def __init__(self, message: str, **positions: 'LineCol'):
        self.positions = positions
        self.message = self.render(message, self.positions)
        self.args = (self.message,)  # this will make error stack more readable

    def render(self, message: str, positions: Dict[str, 'LineCol']) -> str:
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
    Positional index parameters indicates a mapping from position name
    to its indexing inside the input text.
    """
    pass


class PaxterRenderError(PaxterBaseException):
    """
    Exception for parsed tree transformation error.
    """
    pass
