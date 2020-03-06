"""
Lexers based on regular expression for Paxter language
"""
import functools
import json
import re
import unicodedata
from typing import Dict, Match, Pattern

from paxter.core.data import Identifier, KeyValue, Literal, Text
from paxter.core.exceptions import PaxterConfigError
from paxter.core.unicode import ID_CONT_CHARS, ID_PATTERN

__all__ = ['Lexer']

ALLOWED_SWITCH_RE = re.compile(rf'[^\s{ID_CONT_CHARS}#<>{{}}]')
ALLOWED_LEFT_PATTERN_RE = re.compile(r'[#<]*[{"]')
LEFT_TO_RIGHT_TRANS = str.maketrans(r'#<{"', r'#>}"')


@functools.lru_cache(maxsize=None)
class Lexer:
    """
    Lexer helper class for Paxter experimental language.

    Attributes:
        switch: A single symbol character which enables
            Paxter macro, Paxter function, or Paxter phrase
        compiled_fragment_breaks: A dictionary mapping of each left pattern
            to its compiled fragment break regular expression
        compiled_macro_breaks: A dictionary mapping of each left pattern
            to its compiled macro break regular expressions
    """
    switch: str
    compiled_fragment_breaks: Dict[str, Pattern[str]]
    compiled_macro_breaks: Dict[str, Pattern[str]]

    left_brace_re = re.compile(r'(?P<left>[#<]*{)')
    left_sq_bracket_re = re.compile(r'\[')
    option_re = re.compile(
        # At most one of str_value, num_value, id_value will be populated
        rf'\s*(?P<id_key>{ID_PATTERN})(?:\s*=\s*(?:'
        r'(?P<str_value>"(?:[^\\]*|\\["\\/bfnrt]|\\u[0-9A-Fa-f]{4})*")'
        r'|(?P<num_value>-?(?:[1-9][0-9]*|0)(?:\.[0-9]+)?(?:[Ee][+-]?[0-9]+)?)'
        rf'|(?P<id_value>{ID_PATTERN})'
        r')|(?!\s*=))',
    )
    comma_or_option_break_re = re.compile(r'\s*(?P<break>[,\]])')
    option_break_re = re.compile(r'\s*(?P<break>\])')

    def __init__(self, switch: str):
        if len(switch) != 1:
            raise PaxterConfigError(f"switch character must be single: {switch!r}")
        if not ALLOWED_SWITCH_RE.fullmatch(switch):
            char_name = unicodedata.name(switch)
            raise PaxterConfigError(f"switch character not allowed: "
                                    f"{switch!r} ({char_name})")
        switch = re.escape(switch)

        self.switch = switch
        self.compiled_fragment_breaks = {}
        self.compiled_macro_breaks = {}

        # Compile common regular expression based on variable switch
        self.paxter_macro_prefix_re = re.compile(rf'{switch}(?P<id>(?:{ID_PATTERN})?!)')
        self.paxter_func_prefix_re = re.compile(rf'{switch}(?P<id>{ID_PATTERN})')
        self.paxter_phrase_prefix_re = re.compile(rf'{switch}(?P<left>[#<]*{{)')
        self.paxter_string_prefix_re = re.compile(rf'{switch}(?P<left>[#<]*")')
        self.global_break_re = re.compile(
            rf'(?P<text>.*?)(?P<break>{self.switch}|\Z)',
            flags=re.DOTALL,
        )

    def fragment_break_re(self, right_pattern: str) -> Pattern[str]:
        """
        Compiles a regular expression lexer to non-greedily match some text,
        then followed by either a switch symbol character
        or the given right (i.e. closing) pattern.
        """
        right_pattern = re.escape(right_pattern)
        if right_pattern not in self.compiled_fragment_breaks:
            self.compiled_fragment_breaks[right_pattern] = re.compile(
                rf'(?P<text>.*?)(?P<break>{self.switch}|{right_pattern})',
                flags=re.DOTALL,
            )
        return self.compiled_fragment_breaks[right_pattern]

    def text_break_re(self, right_pattern: str) -> Pattern[str]:
        """
        Compiles a regular expression lexer to non-greedily match some text,
        then followed by the given right (i.e. closing) pattern.
        """
        right_pattern = re.escape(right_pattern)
        if right_pattern not in self.compiled_macro_breaks:
            self.compiled_macro_breaks[right_pattern] = re.compile(
                rf'(?P<text>.*?)(?P<break>{right_pattern})',
                flags=re.DOTALL,
            )
        return self.compiled_macro_breaks[right_pattern]

    @staticmethod
    def flip_pattern(left_pattern: str) -> str:
        """
        Flips the given left (i.e. opening) pattern into its corresponding
        right (i.e. closing) pattern (such as `"<##<{"` into `"}>##>"`).
        """
        if not ALLOWED_LEFT_PATTERN_RE.fullmatch(left_pattern):
            raise RuntimeError("something went horribly wrong")
        return left_pattern.translate(LEFT_TO_RIGHT_TRANS)[::-1]

    @staticmethod
    def extract_text_node(matchobj: Match[str]) -> Text:
        """
        Extracts Text node from the given match object
        returned from regular expression with `"text"` group.
        """
        return Text(
            start_pos=matchobj.start('text'),
            end_pos=matchobj.end('text'),
            string=matchobj.group('text'),
        )

    @staticmethod
    def extract_id_node(matchobj: Match[str]) -> Identifier:
        """
        Extracts Identifier node from the given match object
        returned from regular expression with `"id"` group.
        """
        return Identifier(
            start_pos=matchobj.start('id'),
            end_pos=matchobj.end('id'),
            name=matchobj.group('id'),
        )

    @staticmethod
    def extract_kv_pair(matchobj: Match[str]) -> KeyValue:
        """
        Extracts KeyValue node from the given match object
        returned from `option_re` regular expression.
        """
        # Extract key based on id_key group
        key = Identifier(
            start_pos=matchobj.start('id_key'),
            end_pos=matchobj.end('id_key'),
            name=matchobj.group('id_key'),
        )

        # Extract value based on at most one group from
        # str_value, num_value, or id_value groups
        if extracted := matchobj.group('str_value'):
            value = Literal(
                start_pos=matchobj.start('str_value'),
                end_pos=matchobj.end('str_value'),
                value=json.loads(extracted),
            )
        elif extracted := matchobj.group('num_value'):
            value = Literal(
                start_pos=matchobj.start('num_value'),
                end_pos=matchobj.end('num_value'),
                value=json.loads(extracted),
            )
        elif extracted := matchobj.group('id_value'):
            value = Identifier(
                start_pos=matchobj.start('id_value'),
                end_pos=matchobj.end('id_value'),
                name=extracted,
            )
        else:
            value = None

        return key, value
