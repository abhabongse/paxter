"""
Exceptions specific to Paxter language ecosystem.
"""
from typing import NamedTuple

__all__ = [
    'PaxterBaseException',
    'PaxterConfigError', 'PaxterSyntaxError', 'PaxterTransformError',
]


class LineCol(NamedTuple):
    line: int
    col: int


class PaxterBaseException(Exception):
    """
    Base exception specific to Paxter language ecosystem.
    """
    pass


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

    @staticmethod
    def pos_to_line_col(input_text: str, pos: int) -> LineCol:
        """
        Based on the given input text, translates the string-global
        0-indexed position into 1-indexed tuple pair of (line, col).
        """
        line = input_text.count('\n', 0, pos) + 1
        try:
            col = pos - input_text.rindex('\n', 0, pos)
        except ValueError:
            col = pos + 1
        return LineCol(line, col)


class PaxterTransformError(PaxterBaseException):
    """
    Exception for parsed tree transformation error.
    """
    pass
