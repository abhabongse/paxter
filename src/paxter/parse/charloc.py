"""
Utility class which converts 0-indexed absolute positional value
of the input text into 1-indexed line number and column number.
"""
from __future__ import annotations

from dataclasses import InitVar, dataclass, field

__all__ = ['CharLoc']


@dataclass
class CharLoc:
    """
    Represents the position (starting or ending) of a token
    within the input text as a 1-indexed line and column value
    which is useful in understanding where an error occurs.
    """
    input_text: InitVar[str]
    pos: InitVar[int]

    #: 1-index line number
    line: int = field(init=False)

    #: 1-index column index value
    col: int = field(init=False)

    def __post_init__(self, input_text: str, pos: int):
        self.line = input_text.count('\n', 0, pos) + 1
        try:
            self.col = pos - input_text.rindex('\n', 0, pos)
        except ValueError:
            self.col = pos + 1

    @property
    def rendered(self) -> str:
        """
        Rendered string containing the information of
        line and column integer values.
        """
        return f"line {self.line} col {self.col}"
