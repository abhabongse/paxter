"""
Tokenizer implementation for Paxter surface syntax.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from collections import Container, Iterator
from itertools import chain

from paxter.exceptions import PaxterConfigError

_ID_START_CATEGORIES = ['Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl']
_ID_CONT_CATEGORIES = _ID_START_CATEGORIES + ['Mn', 'Mc', 'Nd', 'Pc']
_CMD_SYMB_CATEGORIES = ['Ps', 'Pe', 'Pi', 'Pf', 'Pd', 'Po', 'Sc', 'Sk', 'Sm', 'So']
_OP_CATEGORIES = ['Pd', 'Po', 'Sc', 'Sk', 'Sm', 'So']
_RESERVED_CHARS = '[]{}"`#'


class Tokenizer:
    """
    Tokenizer utility class for Paxter surface syntax.
    All regexp tokenizers are compiled only when an instance of the Tokenizer
    class is initialized to prevent premature high-cost computation.

    Attributes:
        switch: Switch character which introduces a command
        switch_re: Regexp for switch character
        ws_re: Regexp for whitespaces to ignore between tokens in command's extras
        lbrace_re: Regexp for #-prepended opening curly brace character
        lquote_re: Regexp for #-prepended double quote character
        lgrave_re: Regexp for #-prepended grave accent character
        lbracket_re: Regexp for opening square bracket character
        rbracket_re: Regexp for closing square bracket character
        num_re: Regexp for a JSON-compatible number token
        id_re: Regexp for an identifier token
        op_re: Regexp for an operator token
        cmd_symb_re: Regexp for a command symbol character
    """
    switch: str
    switch_re: re.Pattern[str]
    ws_re: re.Pattern[str]
    lbrace_re: re.Pattern[str]
    lquote_re: re.Pattern[str]
    lgrave_re: re.Pattern[str]
    lbracket_re: re.Pattern[str]
    rbracket_re: re.Pattern[str]
    num_re: re.Pattern[str]
    id_re: re.Pattern[str]
    op_re: re.Pattern[str]
    cmd_symb_re: re.Pattern[str]

    _compiled_non_rec_breaks: dict[str, re.Pattern[str]]
    _compiled_rec_breaks: dict[str, re.Pattern[str]]

    def __init__(self, switch: str = '@'):
        self.switch = switch
        self._init_basic_regexps()
        self._init_id_regexp()
        self._init_cmd_symb_regexp()
        self._init_op_regexp()

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

    def _init_basic_regexps(self):
        self.switch_re = re.compile(re.escape(switch))
        self.ws_re = re.compile(r'\s*')
        self.lbrace_re = re.compile(r'#*{')
        self.lquote_re = re.compile(r'#*"')
        self.lgrave_re = re.compile(r'#*`')
        self.lbracket_re = re.compile(r'\[')
        self.rbracket_re = re.compile(r']')
        self.num_re = re.compile(r'-?(?:[1-9][0-9]*|0)(?:\.[0-9]+)?(?:[Ee][+-]?[0-9]+)?')

    def _init_id_regexp(self):
        id_start_chars = ''.join(chain('_', self.codepoints(_ID_START_CATEGORIES)))
        id_cont_chars = ''.join(chain('_', self.codepoints(_ID_CONT_CATEGORIES)))
        self.id_re = re.compile(rf'[{re.escape(id_start_chars)}][{re.escape(id_cont_chars)}]*')

    def _init_cmd_symb_regexp(self):
        cmd_symb_chars = ''.join(self.codepoints(_CMD_SYMB_CATEGORIES))
        self.cmd_symb_re = re.compile(rf'[{re.escape(cmd_symb_chars)}]')

    def _init_op_regexp(self):
        switch_found = False
        op_char_list = []
        for c in self.codepoints(_OP_CATEGORIES):
            if c in _RESERVED_CHARS:
                continue
            elif c == self.switch:
                switch_found = True
            else:
                op_char_list.append(c)
        if not switch_found:
            raise PaxterConfigError(f"unallowed switch character: {self.switch}")

        op_chars = ''.join(op_char_list)
        self.op_re = re.compile(rf'[{re.escape(op_chars)}]')

    @classmethod
    def codepoints(cls, categories: Container[str]) -> Iterator[str]:
        """
        Produces a sequence of character whose category
        is one from the given container.
        """
        for c in map(chr, range(sys.maxunicode + 1)):
            if unicodedata.category(c) in categories:
                yield c

    def __repr__(self):
        return f'<Tokenizer switch={self.switch!r}>'
