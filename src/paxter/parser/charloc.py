"""
Utility class which converts 0-indexed absolute positional value
of the input text into 1-indexed line number and column number.
"""
from dataclasses import InitVar, dataclass, field

__all__ = ['CharLoc']


@dataclass
class CharLoc:
    """
    The position (starting or ending) of a token within the input text
    useful for line and column information in error messages.
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
        The rendered string containing the line and column integer values.
        """
        return f"line {self.line} col {self.col}"
