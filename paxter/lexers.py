"""
Regular expression-based lexers for Paxter language.
"""
import functools
import re
from typing import Dict, Match, Pattern

from paxter.data import Identifier, Text
from paxter.exceptions import PaxterBaseException, PaxterConfigError

ALLOWED_SWITCH_RE = re.compile(r'[^\s\w#<>{}]')
ALLOWED_LEFT_PATTERN_RE = re.compile(r'[#<]*[{"]')
LEFT_TO_RIGHT_TRANS = str.maketrans(r'#<{"', r'#>}"')


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

    def __init__(self, switch: str = '@'):
        if not ALLOWED_SWITCH_RE.fullmatch(switch):
            raise PaxterConfigError(f"switch character not allowed: {switch}")
        self.switch = re.escape(switch)
        self.compiled_fragment_breaks = {}
        self.compiled_macro_breaks = {}

    @functools.cached_property
    def paxter_macro_prefix_re(self) -> Pattern[str]:
        return re.compile(rf'{self.switch}(?P<id>\w*!)', flags=re.DOTALL)

    @functools.cached_property
    def paxter_func_prefix_re(self) -> Pattern[str]:
        return re.compile(rf'{self.switch}(?P<id>\w+)', flags=re.DOTALL)

    @functools.cached_property
    def paxter_phrase_prefix_re(self) -> Pattern[str]:
        return re.compile(rf'{self.switch}(?P<left>[#<]*{{)', flags=re.DOTALL)

    @functools.cached_property
    def paxter_string_prefix_re(self) -> Pattern[str]:
        return re.compile(rf'{self.switch}(?P<left>[#<]*")', flags=re.DOTALL)

    @functools.cached_property
    def left_brace_re(self) -> Pattern[str]:
        return re.compile(r'(?P<left>[#<]*{)', flags=re.DOTALL)

    @functools.cached_property
    def global_break_re(self) -> Pattern[str]:
        return re.compile(rf'(?P<text>.*?)(?P<break>{self.switch}|\Z)', flags=re.DOTALL)

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

    def macro_break_re(self, right_pattern: str) -> Pattern[str]:
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
