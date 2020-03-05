"""
Collection of exceptions for Paxter language utilities.
"""
from typing import Dict, Optional

__all__ = ['PaxterBaseException', 'PaxterSyntaxError', 'PaxterConfigError']


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
    index_params: Dict[str, int]

    def __init__(self, message: str, index_params: Optional[Dict[str, int]] = None):
        self.message = message
        self.index_params = index_params or {}


class PaxterConfigError(PaxterBaseException):
    """
    Exception for configuration error.
    """
    pass
