"""
Recursive descent parser for Paxter experimental syntax.

```
start: fragments
fragments: fragment*
fragment:
    | STRING
    | "@|" IDENTIFIER "|"
    | "@!" wrapped_raw_string
    | "@" IDENTIFIER "!" wrapped_raw_string
    | "@" IDENTIFIER wrapped_options wrapped_fragments  // not implemented
    | "@" IDENTIFIER wrapped_fragments
    | "@" IDENTIFIER  // greedy
wrapped_raw_string:
    | "#" wrapped_raw_string "#"
    | "<" wrapped_raw_string ">"
    | "{" RAW_STRING "}"  // non-greedy
wrapped_options:
    | "#" wrapped_options "#"
    | "<" wrapped_options ">"
    | "[" fragments "]
wrapped_fragments:
    | "#" wrapped_fragments "#"
    | "<" wrapped_fragments ">"
    | "{" fragments "}"

STRING: /[^@]+/
RAW_STRING: /.*/
IDENTIFIER: /[A-Za-z_][A-Za-z0-9_]*/
```
"""
import functools
import re
from typing import Optional, Pattern
from typing.re import Match

from paxter.data import AtFragments, Fragments, Identifier, Node, RawString

DELIMITED_ID_RE = re.compile(
    r'@\|(?P<identifier>[A-Za-z_][A-Za-z0-9_]*)\|',
    flags=re.DOTALL,
)
MACRO_AT_PREFIX_RE = re.compile(
    r'@(?P<identifier>[A-Za-z_][A-Za-z0-9_]*)?!',
    flags=re.DOTALL,
)
STANDARD_AT_PREFIX_RE = re.compile(
    r'@(?P<identifier>[A-Za-z_][A-Za-z0-9_]*)',
    flags=re.DOTALL,
)
GLOBAL_FRAGMENTS_CLOSING_STOP_RE = re.compile(
    r'(?P<raw>.*?)(?P<stop_char>@|\Z)',
    flags=re.DOTALL,
)
SCOPE_OPENING_RE = re.compile(
    r'[#<]*{',
    flags=re.DOTALL,
)
OPENING_TO_CLOSING_TRANS = str.maketrans("#<{", "#>}")


def opening_to_closing(opening_pattern: str) -> str:
    """
    Converts left brace pattern into right brace pattern
    (such as '<##<{' into '}>##>').
    """
    return opening_pattern.translate(OPENING_TO_CLOSING_TRANS)[::-1]


@functools.lru_cache(maxsize=None)
def rawstring_closing_stop_re(closing_pattern: str) -> Pattern[str]:
    """
    Converts left brace pattern into right brace pattern
    (such as '<##<{' into '}>##>')
    that works inside rawstring parsing.
    """
    escaped_closing_pattern = re.escape(closing_pattern)
    return re.compile(
        rf'(?P<raw>.*?){escaped_closing_pattern}',
        flags=re.DOTALL,
    )


@functools.lru_cache(maxsize=None)
def fragments_closing_stop_re(closing_pattern: str) -> Pattern[str]:
    """
    Converts left brace pattern into right brace pattern
    (such as '<##<{' into '}>##>')
    that works inside fragments parsing.
    """
    escaped_closing_pattern = re.escape(closing_pattern)
    return re.compile(
        rf'(?P<raw>.*?)(?P<stop_char>@|{escaped_closing_pattern})',
        flags=re.DOTALL,
    )


class Paxter:
    """
    Parser class for Paxter experimental language.

    The constructor of this class is not intended to be called directly.
    Instead use class method `Paxter.parse` instead.
    """
    content: str
    current_pos: int
    result: Fragments

    def __init__(self, content: str):
        self.content = content
        self.current_pos = 0
        self.result = self.parse_fragments('^')
        assert self.current_pos == len(self.content)

    @classmethod
    def parse(cls, content: str) -> Fragments:
        """
        Use this class method to perform parsing on input string.
        """
        parsed_obj = cls(content)
        return parsed_obj.result

    def parse_fragments(self, opening_pattern: str) -> Fragments:
        """
        Parse content string within the fragment scope
        specified by the opening pattern, starting at the given pos.

        This method will attempt to find a matching closing pattern
        which signifies the end of fragments parsing.

        Please note that this function is also reused for
        global fragments parsing (with special empty opening pattern).
        """
        if opening_pattern == '^':
            assert self.current_pos == 0, "expected global fragments parsing"
            closing_pattern = '$'
            closing_stop_re = GLOBAL_FRAGMENTS_CLOSING_STOP_RE
        else:
            closing_pattern = opening_to_closing(opening_pattern)
            closing_stop_re = fragments_closing_stop_re(closing_pattern)

        start_pos = self.current_pos
        fragments = []

        while True:
            matchobj = closing_stop_re.match(self.content, self.current_pos)
            if not matchobj:
                raise SyntaxError(
                    f"cannot find matched scope closing {closing_pattern!r} "
                    f"to the scope opening {opening_pattern!r} "
                    f"at pos {start_pos}"
                )

            raw, stop_char = matchobj.group('raw', 'stop_char')
            raw_start, raw_end = matchobj.span('raw')

            if raw:
                fragments.append(RawString(raw_start, raw_end, raw))
            if stop_char == '@':
                self.current_pos = raw_end
                fragments.append(self.parse_at_expr())
            else:
                self.current_pos = matchobj.end()
                break

        return Fragments(start_pos, raw_end, fragments)

    def parse_at_expr(self) -> Node:
        """
        Attempt to parse different @-expressions.
        """
        result = (self.parse_delimited_identifier()
                  or self.parse_at_fragments())
        if result is None:
            raise SyntaxError(f"unrecognized at-expr at pos {self.current_pos}")
        return result

    def parse_delimited_identifier(self) -> Optional[Identifier]:
        """
        Parse delimited identifier of the pattern '@|identifier|'.
        """
        matchobj = DELIMITED_ID_RE.match(self.content, self.current_pos)
        if matchobj is None:
            return None

        id_node = self.extract_id_node(matchobj)
        self.current_pos = matchobj.end()

        return id_node

    def parse_at_fragments(self) -> Optional[AtFragments]:
        """
        Parse standard at-expression with recursive fragments.
        """
        start_pos = self.current_pos
        matchobj = STANDARD_AT_PREFIX_RE.match(self.content, self.current_pos)
        if matchobj is None:
            return None

        id_node = self.extract_id_node(matchobj)
        self.current_pos = matchobj.end()

        scope_opening = self.parse_scope_opening()
        fragments = self.parse_fragments(scope_opening)

        return AtFragments(start_pos, self.current_pos, id_node, fragments)

    def extract_id_node(self, id_prefix_matchobj: Match) -> Identifier:
        """
        Build Identifier node from the given match object.
        Compatible with DELIMITED_ID_RE, MACRO_AT_PREFIX_RE, and STANDARD_AT_PREFIX_RE.
        """
        name = id_prefix_matchobj.group('identifier')
        start, end = id_prefix_matchobj.span('identifier')
        return Identifier(start, end, name)

    def parse_scope_opening(self) -> str:
        """
        Parse scope opening from the given position.
        """
        matchobj = SCOPE_OPENING_RE.match(self.content, self.current_pos)
        if matchobj is None:
            raise SyntaxError(f"improper scope opening at pos {self.current_pos}")

        self.current_pos = matchobj.end()
        return matchobj.group()
