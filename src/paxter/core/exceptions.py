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
        self.message = message  # pragma: no cover


class PaxterSyntaxError(PaxterBaseException):
    """
    Exception for syntax error raised while parsing input text.
    Positional index parameters indicates a mapping from position name
    to its indexing inside the input text.
    """
    template: str
    body: str
    positions: PositionMap

    def __init__(
            self, template: str,
            body: str, positions: Optional[PositionMap] = None,
    ):
        self.template = template
        self.body = body
        self.positions = positions or {}
        self.args = (self.render(),)

    def render(self):
        formatted_pos = {}
        for key, pos in self.positions.items():
            line = self.body.count('\n', 0, pos) + 1
            try:
                col = pos - self.body.rindex('\n', 0, pos)
            except ValueError:  # pragma: no cover
                col = pos + 1
            formatted_pos[key] = f"line {line} col {col}"
        return self.template.format(**formatted_pos)


class PaxterConfigError(PaxterBaseException):
    """
    Exception for configuration error.
    """
