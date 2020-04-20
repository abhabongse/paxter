"""
Exceptions specific to Paxter language ecosystem.
"""
from typing import Dict, NamedTuple, Optional

__all__ = [
    'PaxterBaseException',
    'PaxterConfigError', 'PaxterSyntaxError', 'PaxterTransformError',
]

PositionMap = Dict[str, int]


class LineCol(NamedTuple):
    line: int
    col: int


class PaxterBaseException(Exception):
    """
    Base exception specific to Paxter language ecosystem.
    """
    msg_template: str
    positions: PositionMap

    def __init__(self, msg_template: str, positions: Optional[PositionMap] = None):
        self.msg_template = msg_template
        self.positions = positions or {}

    def render(self, body: str) -> str:
        """
        Render the message with populated (line, col)
        """
        positions = {
            k: f'line {v.line} col {v.col}'
            for k, v in self.translate_positions(body).items()
        }
        return self.msg_template.format(**positions)

    def translate_positions(self, body: str) -> Dict[str, LineCol]:
        """
        Based on the given text body, translates the position map
        from the absolute value into tuple pair of 1-indexed (line, col).
        """
        translated = {}
        for key, pos in self.positions.items():
            line = body.count('\n', 0, pos) + 1
            try:
                col = pos - body.rindex('\n', 0, pos)
            except ValueError:  # pragma: no cover
                col = pos + 1
            translated[key] = LineCol(line, col)
        return translated


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


class PaxterTransformError(PaxterBaseException):
    """
    Exception for parsed tree transformation error.
    """
    pass
