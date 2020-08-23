"""
Regular expression based lexers for Paxter language.
"""
import re
from typing import Dict, Pattern

from paxter.parse.charset import IDENTIFIER_PATTERN, OPERATOR_PATTERN, SYMBOL_PATTERN

__all__ = ['LEXER']


class Lexer:
    """
    Collection of compiled regular expressions to parse Paxter language.
    """
    _compiled_non_rec_breaks = Dict[str, Pattern[str]]
    _compiled_rec_breaks = Dict[str, Pattern[str]]

    ws_re = re.compile(r'\s*')
    at_re = re.compile(r'@')
    lbar_re = re.compile(r'(?P<left>#*\|)')
    lbrace_re = re.compile(r'(?P<left>#*{)')
    lquote_re = re.compile(r'(?P<left>#*")')
    lbracket_re = re.compile(r'\[')
    rbracket_re = re.compile(r']')
    id_re = re.compile(rf'(?P<id>{IDENTIFIER_PATTERN})')
    symbol_re = re.compile(rf'(?P<symbol>{SYMBOL_PATTERN})')
    op_re = re.compile(rf'(?P<op>{OPERATOR_PATTERN})')
    num_re = re.compile(r'(?P<num>-?(?:[1-9][0-9]*|0)(?:\.[0-9]+)?'
                        r'(?:[Ee][+-]?[0-9]+)?)')
    global_break_re = re.compile(r'(?P<inner>(?s:.)*?)(?P<break>@|\Z)')

    def __init__(self):
        self._compiled_non_rec_breaks = {}
        self._compiled_rec_breaks = {}

    def non_rec_break_re(self, right_pattern: str) -> Pattern[str]:
        """
        Compiles a regular expression lexer to non-greedily match some text
        which is then followed by the given right enclosing pattern.
        """
        right_pattern = re.escape(right_pattern)
        if right_pattern not in self._compiled_non_rec_breaks:
            self._compiled_non_rec_breaks[right_pattern] = re.compile(
                r'(?P<inner>(?s:.)*?)'
                rf'(?P<break>{right_pattern})',
            )
        return self._compiled_non_rec_breaks[right_pattern]

    def rec_break_re(self, right_pattern: str) -> Pattern[str]:
        """
        Compiles a regular expression lexer to non-greedily match some text
        which is then followed by either the @-command switch symbol
        or the given enclosing right pattern.
        """
        right_pattern = re.escape(right_pattern)
        if right_pattern not in self._compiled_rec_breaks:
            self._compiled_rec_breaks[right_pattern] = re.compile(
                r'(?P<inner>(?s:.)*?)'
                rf'(?P<break>@|{right_pattern})',
            )
        return self._compiled_rec_breaks[right_pattern]


# Instance of lexer class
LEXER = Lexer()
