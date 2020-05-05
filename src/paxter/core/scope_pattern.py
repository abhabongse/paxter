"""
Utility class for opened and closed pattern of the same scope:
brace pattern for `FragmentList`, quoted pattern for `Text`,
and bar pattern for `PaxterPhrase`.
"""
import re
from dataclasses import dataclass
from typing import Pattern

from paxter.core.lexers import LEXER

__all__ = ['ScopePattern', 'EMPTY_SCOPE_PATTERN', 'GLOBAL_SCOPE_PATTERN']

ALLOWED_OPENED_PATTERN_RE = re.compile(r'[#<]*[{"|]')
OPENED_TO_CLOSED_TRANS = str.maketrans(r'#<{"|', r'#>}"|')


@dataclass
class ScopePattern:
    """
    Data regarding the opened pattern and the closed pattern
    of one particular scope.
    """
    #: The opening pattern enclosing the scope
    opening: str
    #: The closing pattern enclosing the scope
    closing: str = None

    def __post_init__(self):
        if self.closing is None:
            self.closing = self.flip_pattern(self.opening)

    @staticmethod
    def flip_pattern(opened: str) -> str:
        """
        Flips the given opened (i.e. left) pattern
        into the corresponding closed (i.e. right) pattern.

        For example, the opened pattern `"<##<{"`
        should be flipped into the closed pattern `"}>##>".
        """
        if not ALLOWED_OPENED_PATTERN_RE.fullmatch(opened):
            raise RuntimeError("something went horribly wrong")  # pragma: no cover
        return opened.translate(OPENED_TO_CLOSED_TRANS)[::-1]

    @property
    def non_rec_break_re(self) -> Pattern[str]:
        """
        Compiles a regular expression lexer to non-greedily match some text
        which is then followed by the given closed (i.e. right) pattern.
        """
        return LEXER.non_rec_break_re(self.closing)

    @property
    def rec_break_re(self) -> Pattern[str]:
        """
        Compiles a regular expression lexer to non-greedily match some text
        which is then followed by either the @-command switch symbol
        or the given closed (i.e. right) pattern.
        """
        return LEXER.rec_break_re(self.closing)


class GlobalScopePattern(ScopePattern):
    """
    Specialized scope pattern just for global-level fragment list.
    """

    def __init__(self):
        super().__init__(opening='', closing='')

    @property
    def non_rec_break_re(self) -> Pattern[str]:
        """
        Compiles a regular expression lexer to non-greedily match some text
        which is then followed by the given closed (i.e. right) pattern.
        """
        raise AttributeError

    @property
    def rec_break_re(self) -> Pattern[str]:
        """
        Compiles a regular expression lexer to non-greedily match some text
        which is then followed by either the @-command switch symbol
        or the given closed (i.e. right) pattern.
        """
        return LEXER.global_break_re


EMPTY_SCOPE_PATTERN = ScopePattern(opening='', closing='')
GLOBAL_SCOPE_PATTERN = GlobalScopePattern()
