"""
Lexers based on regular expression for Paxter language
"""
import functools
import re
from typing import Dict, Match, Pattern

from paxter.core.data import Identifier, Text
from paxter.core.exceptions import PaxterConfigError

__all__ = ['Lexer']

ALLOWED_SWITCH_RE = re.compile(r'[^\s\w#<>{}]')
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
    left_square_bracket_re = re.compile(r'\[')
    option_re = re.compile(
        # At most one of str_value, num_value, id_value will be populated
        r'\s*(?P<key>\w+)(?:\s*=\s*(?:'
        r'(?P<str_value>"(?:[^\\]*|\\["\\/bfnrt]|\\u[0-9A-Fa-f]{4})*")'
        r'|(?P<num_value>-?(?:[1-9][0-9]*|0)(?:\.[0-9]+)?(?:[Ee][+-]?[0-9]+)?)'
        r'|(?P<id_value>\w+)'
        r')|(?!\s*=))',
    )
    comma_or_option_break_re = re.compile(r'\s*(?P<break>[,\]])')
    option_break_re = re.compile(r'\s*(?P<break>\])')

    def __init__(self, switch: str):
        if not ALLOWED_SWITCH_RE.fullmatch(switch):
            raise PaxterConfigError(f"switch character not allowed: {switch}")
        switch = re.escape(switch)

        self.switch = switch
        self.compiled_fragment_breaks = {}
        self.compiled_macro_breaks = {}

        # Compile common regular expression based on variable switch
        self.paxter_macro_prefix_re = re.compile(rf'{switch}(?P<id>\w*!)')
        self.paxter_func_prefix_re = re.compile(rf'{switch}(?P<id>\w+)')
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
        string = matchobj.group('text')
        start_pos, end_pos = matchobj.span('text')
        return Text(start_pos, end_pos, string)

    @staticmethod
    def extract_id_node(matchobj: Match[str]) -> Identifier:
        """
        Extracts Identifier node from the given match object
        returned from regular expression with `"id"` group.
        """
        name = matchobj.group('id')
        start_pos, end_pos = matchobj.span('id')
        return Identifier(start_pos, end_pos, name)
