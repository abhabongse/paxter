"""
Regular expression based lexers for Paxter language.
"""
import re
from typing import Dict, Pattern

from paxter.core.charset import IDENTIFIER_PATTERN, OPERATOR_PATTERN, SYMBOL_PATTERN

__all__ = ['LEXER']


class Lexer:
    """
    Collection of compiled regular expressions to parse Paxter language.
    """
    _compiled_non_rec_breaks = Dict[str, Pattern[str]]
    _compiled_rec_breaks = Dict[str, Pattern[str]]

    global_break_re = re.compile(r'(?P<inner>(?s:.)*?)(?P<break>@|\Z)')
    at_re = re.compile(r'@')
    id_re = re.compile(rf'(?P<id>{IDENTIFIER_PATTERN})')
    left_bar_re = re.compile(r'(?P<left>#*\|)')
    left_bracket_re = re.compile(r'\[')
    left_brace_re = re.compile(r'(?P<left>#*{)')
    left_quote_re = re.compile(r'(?P<left>#*")')
    symbol_re = re.compile(rf'(?P<symbol>{SYMBOL_PATTERN})')
    option_token_re = re.compile(
        r'\s*(?:'
        rf'(?P<id>{IDENTIFIER_PATTERN})|'
        rf'(?P<op>{OPERATOR_PATTERN})|'
        r'(?P<num>-?(?:[1-9][0-9]*|0)(?:\.[0-9]+)?(?:[Ee][+-]?[0-9]+)?)|'
        r'(?P<char>[@()\[\]{}])'
        r')',
    )

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
