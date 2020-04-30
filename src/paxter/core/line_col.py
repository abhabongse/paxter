"""
Utility class which converts 0-indexed absolute positional value
into 1-indexed line number and column number.
"""
from dataclasses import InitVar, dataclass, field

__all__ = ['LineCol']


@dataclass
class LineCol:
    """
    The starting or ending position of a token within the input text.
    """
    input_text: InitVar[str]
    pos: InitVar[int]
    line: int = field(init=False)
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
        Renders the line and column integer values into standard string.
        """
        return f"line {self.line} col {self.col}"
