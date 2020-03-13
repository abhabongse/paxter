"""
Exceptions specific to Paxter language utilities
"""
from typing import Dict, Optional, Tuple

__all__ = ['PaxterBaseException', 'PaxterSyntaxError', 'PaxterConfigError',
           'PaxterTransformError']

PositionMap = Dict[str, int]


class PaxterBaseException(Exception):
    """
    Base exception related to Paxter language utilities.
    """
    template: str
    positions: PositionMap

    def __init__(
            self, template: str,
            positions: Optional[PositionMap] = None,
    ):
        self.template = template
        self.positions = positions or {}

    def render(self, body):
        positions = {
            k: f'line {v[0]} col {v[1]}'
            for k, v in self.line_pos_positions(body).items()
        }
        return self.template.format(**positions)

    def line_pos_positions(self, body) -> Dict[str, Tuple[int, int]]:
        """
        Based on the given text body, translates the position map
        from absolute value into tuple pair of 1-indexed (line, col).
        """
        translated = {}
        for key, pos in self.positions.items():
            line = body.count('\n', 0, pos) + 1
            try:
                col = pos - body.rindex('\n', 0, pos)
            except ValueError:  # pragma: no cover
                col = pos + 1
            translated[key] = (line, col)
        return translated


class PaxterSyntaxError(PaxterBaseException):
    """
    Exception for syntax error raised while parsing input text.
    Positional index parameters indicates a mapping from position name
    to its indexing inside the input text.
    """


class PaxterConfigError(PaxterBaseException):
    """
    Exception for configuration error.
    """


class PaxterTransformError(PaxterBaseException):
    """
    Exception for tree transformation error.
    """
