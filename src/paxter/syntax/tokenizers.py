"""
Tokenizer implementation for Paxter surface syntax.
"""
from __future__ import annotations

import re
import sys
import unicodedata

from paxter.exceptions import PaxterConfigError

_ID_START_CATEGORIES = ['Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl']
_ID_CONT_CATEGORIES = _ID_START_CATEGORIES + ['Mn', 'Mc', 'Nd', 'Pc']
_CMD_SYMB_CATEGORIES = ['Ps', 'Pe', 'Pi', 'Pf', 'Pd', 'Po', 'Sc', 'Sk', 'Sm', 'So']
_OP_CATEGORIES = ['Pd', 'Po', 'Sc', 'Sk', 'Sm', 'So']
_RESERVED_CHARS = '[]{}"`#'

ID_START_CHARS = ''.join(
    c for c in map(chr, range(sys.maxunicode + 1))
    if unicodedata.category(c) in _ID_START_CATEGORIES or c == '_'
)
ID_CONT_CHARS = ''.join(
    c for c in map(chr, range(sys.maxunicode + 1))
    if unicodedata.category(c) in _ID_CONT_CATEGORIES or c == '_'
)
CMD_SYMB_CHARS = ''.join(
    c for c in map(chr, range(sys.maxunicode + 1))
    if unicodedata.category(c) in _CMD_SYMB_CATEGORIES
)
OP_CHARS = ''.join(
    c for c in map(chr, range(sys.maxunicode + 1))
    if unicodedata.category(c) in _OP_CATEGORIES and c not in _RESERVED_CHARS
)


class Tokenizer:
    """
    Tokenizer utility class for Paxter surface syntax.
    """
    switch: str
    switch_re = re.Pattern[str]
    ws_re = re.Pattern[str]
    lbrace_re = re.Pattern[str]
    lquote_re = re.Pattern[str]
    lgrave_re = re.Pattern[str]
    lbracket_re = re.Pattern[str]
    rbracket_re = re.Pattern[str]
    id_re = re.Pattern[str]
    cmd_symb_re = re.Pattern[str]
    op_re = re.Pattern[str]
    num_re = re.Pattern[str]

    _compiled_non_rec_breaks: dict[str, re.Pattern[str]]
    _compiled_rec_breaks: dict[str, re.Pattern[str]]

    def __init__(self, switch: str = '@'):
        self.switch = switch
        self.switch_re = re.compile(re.escape(switch))
        self.ws_re = re.compile(r'\s*')
        self.lbrace_re = re.compile(r'#*{')
        self.lquote_re = re.compile(r'#*"')
        self.lgrave_re = re.compile(r'#*`')
        self.lbracket_re = re.compile(r'\[')
        self.rbracket_re = re.compile(r']')
        self.id_re = re.compile(rf'[{re.escape(ID_START_CHARS)}][{re.escape(ID_CONT_CHARS)}]*')
        self.cmd_symb_re = re.compile(rf'[{re.escape(CMD_SYMB_CHARS)}]')
        self.op_re = re.compile(rf'[{re.escape(self._filtered_operator_chars(switch))}]+')
        self.num_re = re.compile(r'-?(?:[1-9][0-9]*|0)(?:\.[0-9]+)?(?:[Ee][+-]?[0-9]+)?')

    def non_rec_break_re(self, right_pattern: str) -> re.Pattern[str]:
        """
        Compiles and caches a regular expression tokenizer to non-greedily match
        some text which is immediately followed by the given right pattern.
        """
        right_pattern = re.escape(right_pattern)
        if right_pattern not in self._compiled_non_rec_breaks:
            self._compiled_non_rec_breaks[right_pattern] = re.compile(
                rf'(?P<inner>(?s:.)*?)(?P<break>{right_pattern})',
            )
        return self._compiled_non_rec_breaks[right_pattern]

    def rec_break_re(self, right_pattern: str) -> re.Pattern[str]:
        """
        Compiles and caches a regular expression tokenizer to non-greedily match
        some text which is immediately followed by either the switch symbol
        or the given right pattern.
        """
        right_pattern = re.escape(right_pattern)
        if right_pattern not in self._compiled_rec_breaks:
            self._compiled_rec_breaks[right_pattern] = re.compile(
                rf'(?P<inner>(?s:.)*?)(?P<break>{re.escape(self.switch)}|{right_pattern})',
            )
        return self._compiled_rec_breaks[right_pattern]

    @classmethod
    def _filtered_operator_chars(cls, switch: str):
        if switch not in OP_CHARS:
            raise PaxterConfigError(f"unallowed switch character: {switch}")
        return ''.join(c for c in OP_CHARS if c != switch)

    def __repr__(self):
        return f'<Tokenizer switch={self.switch!r}>'
