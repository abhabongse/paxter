"""
Recursive descent parser for Paxter experimental syntax.

TODO: add string literal of the form: "@\"" ESCAPED_STRING "\""
```
start: fragments
fragments: fragment*
fragment:
    | STRING
    | "@|" IDENTIFIER "|"
    | "@!" wrapped_raw_string
    | "@" IDENTIFIER "!" wrapped_raw_string
    | "@" IDENTIFIER wrapped_fragments
    | "@" IDENTIFIER  // greedy
wrapped_raw_string:
    | "#" wrapped_raw_string "#"
    | "<" wrapped_raw_string ">"
    | "{" RAW_STRING "}"  // non-greedy
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

from paxter.data import AtMacroExpr, AtNormalExpr, Fragments, Identifier, Node, \
    RawString

DELIMITED_AT_ID_RE = re.compile(
    r'@\|(?P<identifier>[A-Za-z_][A-Za-z0-9_]*)\|',
    flags=re.DOTALL,
)
AT_MACRO_PREFIX_RE = re.compile(
    r'@(?P<identifier>[A-Za-z_][A-Za-z0-9_]*)?!',
    flags=re.DOTALL,
)
AT_NORMAL_PREFIX_RE = re.compile(
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
    curr_pos: int
    result: Fragments

    def __init__(self, content: str):
        self.content = content
        self.curr_pos = 0
        self.result = self.parse_fragments('')
        assert self.curr_pos == len(self.content)

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
        # Compute scope closing stop pattern from opening pattern
        if opening_pattern:
            closing_pattern = opening_to_closing(opening_pattern)
            closing_stop_re = fragments_closing_stop_re(closing_pattern)
        else:
            assert self.curr_pos == 0, "expected global fragments parsing"
            closing_pattern = ''
            closing_stop_re = GLOBAL_FRAGMENTS_CLOSING_STOP_RE

        start_pos = self.curr_pos
        children = []

        while True:
            # Find the next scope closing or the @-symbol
            matchobj = closing_stop_re.match(self.content, self.curr_pos)
            if matchobj is None:
                raise SyntaxError(
                    f"cannot find matched scope closing {closing_pattern!r} "
                    f"to the scope opening {opening_pattern!r} "
                    f"at pos {start_pos}"
                )

            # Append non-empty raw string to result list
            raw_node = self.extract_raw_node(matchobj)
            if raw_node.text:
                children.append(raw_node)

            # Dispatch job between scope closing and @-symbol
            stop_char = matchobj.group('stop_char')
            stop_char_start = matchobj.start('stop_char')
            if stop_char == '@':
                self.curr_pos = stop_char_start
                children.append(self.parse_at_expression())
            else:
                self.curr_pos = matchobj.end()
                break

        return Fragments(start_pos, stop_char_start, children)

    def parse_at_expression(self) -> Node:
        """
        Attempt to dispatch and parse different kinds of @-expressions.
        """
        result = (self.parse_delimited_at_identifier()
                  or self.parse_at_macro_expression()
                  or self.parse_at_normal_expression())
        if result is None:
            raise SyntaxError(f"unrecognized at-expr at pos {self.curr_pos}")
        return result

    def parse_delimited_at_identifier(self) -> Optional[Identifier]:
        """
        Parse the delimited lone identifier from the @-expression
        which has the form of '@|identifier|'.
        """
        prefix_matchobj = DELIMITED_AT_ID_RE.match(self.content, self.curr_pos)
        if prefix_matchobj is None:
            return None

        id_node = self.extract_id_node(prefix_matchobj)
        self.curr_pos = prefix_matchobj.end()

        return id_node

    def parse_at_macro_expression(self) -> Optional[AtMacroExpr]:
        """
        Parse the macro version of @-expression.
        """
        start_pos = self.curr_pos
        prefix_matchobj = AT_MACRO_PREFIX_RE.match(self.content, self.curr_pos)
        if prefix_matchobj is None:
            return None

        id_node = self.extract_id_node(prefix_matchobj)
        self.curr_pos = prefix_matchobj.end()

        opening_pattern = self.extract_scope_opening()
        closing_pattern = opening_to_closing(opening_pattern)
        closing_stop_re = rawstring_closing_stop_re(closing_pattern)

        raw_matchobj = closing_stop_re.match(self.content, self.curr_pos)
        if raw_matchobj is None:
            raise SyntaxError(
                f"cannot find matched scope closing {closing_pattern!r} "
                f"to the scope opening {opening_pattern!r} "
                f"at pos {self.curr_pos}"
            )

        raw_node = self.extract_raw_node(raw_matchobj)
        return AtMacroExpr(start_pos, self.curr_pos, id_node, raw_node)

    def parse_at_normal_expression(self) -> Optional[AtNormalExpr]:
        """
        Parse the standard version of @-expression with recursive fragments.
        """
        start_pos = self.curr_pos
        prefix_matchobj = AT_NORMAL_PREFIX_RE.match(self.content, self.curr_pos)
        if prefix_matchobj is None:
            return None

        id_node = self.extract_id_node(prefix_matchobj)
        self.curr_pos = prefix_matchobj.end()

        opening_pattern = self.extract_scope_opening()
        fragments = self.parse_fragments(opening_pattern)

        return AtNormalExpr(start_pos, self.curr_pos, id_node, fragments)

    def extract_scope_opening(self) -> str:
        """
        Find the scope opening of the current @-expression.
        """
        matchobj = SCOPE_OPENING_RE.match(self.content, self.curr_pos)
        if matchobj is None:
            raise SyntaxError(f"improper scope opening at pos {self.curr_pos}")

        self.curr_pos = matchobj.end()
        return matchobj.group()

    @staticmethod
    def extract_raw_node(matchobj: Match) -> RawString:
        """
        Construct RawString node based on the given match object
        with group named 'raw'.
        """
        text = matchobj.group('raw')
        start, end = matchobj.span('raw')
        return RawString(start, end, text)

    @staticmethod
    def extract_id_node(matchobj: Match) -> Identifier:
        """
        Construct Identifier node based on the given match object
        with group named 'identifier'
        """
        name = matchobj.group('identifier')
        start, end = matchobj.span('identifier')
        return Identifier(start, end, name)
