"""
Exception classes specific to Paxter language ecosystem.
"""
from __future__ import annotations


class PaxterBaseException(Exception):
    """
    Base exception specific to Paxter language toolchain.
    """
    #: Error message
    message: str

    def __init__(self, message: str):
        self.message = message


class PaxterConfigError(PaxterBaseException):
    """
    Exceptions for configuration error.
    """
    pass


class PaxterSyntaxError(PaxterBaseException):
    """
    Exceptions for syntax error raised while parsing source text.
    """
    pass


class PaxterProcessError(PaxterBaseException):
    """
    Exceptions for other errors.
    """
    pass
