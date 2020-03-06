"""
Exceptions specific to Paxter language utilities
"""
from typing import Dict, Optional

__all__ = ['PaxterBaseException', 'PaxterSyntaxError', 'PaxterConfigError']

PositionMap = Dict[str, int]


class PaxterBaseException(Exception):
    """
    Base exception related to Paxter language utilities.
    """
    message: str

    def __init__(self, message: str):
        self.message = message


class PaxterSyntaxError(PaxterBaseException):
    """
    Exception for syntax error raised while parsing input text.
    Positional index parameters indicates a mapping from position name
    to its indexing inside the input text.
    """
    message: str
    body: str
    positions: PositionMap

    def __init__(
            self, message: str,
            body: str, positions: Optional[PositionMap] = None,
    ):
        self.message = message
        self.body = body
        self.positions = positions or {}


class PaxterConfigError(PaxterBaseException):
    """
    Exception for configuration error.
    """
