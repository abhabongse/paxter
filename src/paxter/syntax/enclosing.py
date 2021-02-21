"""
Utility class for textual enclosing (left and right) patterns
which surrounds a particular scope of string data.
It is used in the following scenarios:

- Brace pattern for :class:`FragmentSeq <paxter.syntax.data.FragmentSeq>` nodes
- Quoted pattern for :class:`Text <paxter.syntax.data.Text>` nodes
- Bar pattern for the phrase of :class:`Command <paxter.syntax.data.Command>` nodes
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Pattern

from paxter.syntax.lexers import _LEXER

__all__ = ['EnclosingPattern', 'GlobalEnclosingPattern']

ALLOWED_LEFT_PATTERN_RE = re.compile(r'(?:#*[|{"])?')
LEFT_TO_RIGHT_TRANS = str.maketrans(r'#|{"', r'#|}"')


@dataclass
class EnclosingPattern:
    """
    Information regarding the enclosing (left and right) patterns
    for a particular scope of string data.
    """
    #: The left (i.e. opening) pattern enclosing the scope
    left: str

    #: The right (i.e. closing) pattern enclosing the scope
    right: str = None

    def __post_init__(self):
        if self.right is None:
            self.right = self.flip_pattern(self.left)

    def __bool__(self):
        return bool(self.left)

    @staticmethod
    def flip_pattern(left: str) -> str:
        """
        Flips the given left pattern into the corresponding right pattern.

        For example, the opened pattern `"<##<{"`
        should be flipped into the closed pattern `"}>##>".
        """
        if not ALLOWED_LEFT_PATTERN_RE.fullmatch(left):
            raise RuntimeError("something went horribly wrong")  # pragma: no cover
        return left.translate(LEFT_TO_RIGHT_TRANS)[::-1]

    @property
    def non_rec_break_re(self) -> Pattern[str]:
        """
        Compiles a regular expression lexer to non-greedily match some text
        which is then followed by the given enclosing right pattern.
        """
        return _LEXER.non_rec_break_re(self.right)

    @property
    def rec_break_re(self) -> Pattern[str]:
        """
        Compiles a regular expression lexer to non-greedily match some text
        which is then followed by either the @-command switch symbol
        or the given enclosing right pattern.
        """
        return _LEXER.rec_break_re(self.right)


@dataclass
class GlobalEnclosingPattern(EnclosingPattern):
    """
    Specialized scope pattern just for global-level fragment sequence.
    """
    left: str = field(default=None, init=False, repr=False)
    right: str = field(default=None, init=False, repr=False)

    def __post_init__(self):
        pass

    @property
    def non_rec_break_re(self) -> Pattern[str]:
        raise AttributeError

    @property
    def rec_break_re(self) -> Pattern[str]:
        return _LEXER.global_break_re
