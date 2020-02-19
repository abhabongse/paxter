"""
Recursive descent parser for Paxter experimental language.
"""
import functools
import re
from typing import List, Match, Optional, Pattern

from paxter.data import AtExpression, BaseNode, Fragments, Identifier, RawString

DELIMITED_LONE_ID_RE = (
    re.compile(r'@\|(?P<identifier>[A-Za-z_][A-Za-z0-9_]*)\|', flags=re.DOTALL)
)
NORMAL_AT_PREFIX_RE = (
    re.compile(r'@(?P<identifier>[A-Za-z_][A-Za-z0-9_]*)?', flags=re.DOTALL)
)
GLOBAL_CLOSING_STOP_RE = (
    re.compile(r'(?P<raw>.*?)(?P<stop_char>@|\Z)', flags=re.DOTALL)
)
SCOPE_OPENING_RE = re.compile(r'[#<]*{', flags=re.DOTALL)
OPENING_TO_CLOSING_TRANS = str.maketrans("#<{", "#>}")


def opening_to_closing(opening_pattern: str) -> str:
    """
    Converts scope opening pattern into closing pattern
    (such as `'<##<{'` into `'}>##>'`).
    """
    return opening_pattern.translate(OPENING_TO_CLOSING_TRANS)[::-1]


@functools.lru_cache(maxsize=None)
def compile_closing_stop_re(closing_pattern: str) -> Pattern[str]:
    """
    Compiles regular expression to match some raw strings
    followed by @-symbol or the given scope closing pattern.
    """
    escaped_closing_pattern = re.escape(closing_pattern)
    return re.compile(rf'(?P<raw>.*?)(?P<stop_char>@|{escaped_closing_pattern})',
                      flags=re.DOTALL)


class Paxter:
    """
    Recursive descent parser for Paxter experimental language.

    The constructor for this class should _not_ be called directly.
    Instead, use class method `Paxter.parse` instead.
    """
    input_string: str
    curr_pos: int
    parsed_tree: Fragments

    def __init__(self, input_string: str):
        self.input_string = input_string
        self.curr_pos = 0
        self.parsed_tree = self.parse_global_fragments()

    @classmethod
    def parse(cls, input_string: str) -> Fragments:
        """
        Use this class method to perform parsing on input string.
        """
        parsed_obj = cls(input_string)
        return parsed_obj.parsed_tree

    def parse_global_fragments(self) -> Fragments:
        """
        Parse global fragments until the end of string.
        """
        node = self.parse_fragments_inner(r"\A", r"\Z", GLOBAL_CLOSING_STOP_RE)
        assert self.curr_pos == len(self.input_string), (
            f"input string not fully consumed; stopped at pos {self.curr_pos}"
        )
        return node

    def parse_at_expr_fragments(self, opening_pattern: str) -> Fragments:
        """
        Parse fragments inside @-expressions until reaching the end of scope
        based on the given scope opening pattern.
        """
        closing_pattern = opening_to_closing(opening_pattern)
        closing_stop_re = compile_closing_stop_re(closing_pattern)
        return self.parse_fragments_inner(
            opening_pattern, closing_pattern, closing_stop_re,
        )

    def parse_fragments_inner(
            self,
            opening_pattern: str,
            closing_pattern: str,
            closing_stop_re: Pattern[str]
    ) -> Fragments:
        """
        Parse input string within the fragments scope.

        It uses the given `closing_stop_re` to match some raw strings
        followed by @-symbol or the scope closing pattern.
        If @-symbol is encountered, then it calls other methods
        in order to parse @-expressions,
        and the process repeats from the beginning again.
        Otherwise, if closing pattern has been found,
        the parsing of the current fragments terminates immediately.
        """
        start_pos = self.curr_pos
        children: List[BaseNode] = []
        while True:
            # Tries to match the @-symbol or the scope closing
            matchobj = closing_stop_re.match(self.input_string, self.curr_pos)
            if matchobj is None:
                raise SyntaxError(
                    f"cannot find matched scope closing {closing_pattern!r} "
                    f"to the scope opening {opening_pattern!r} "
                    f"at pos {start_pos}"
                )

            # Append non-empty raw string to children list
            raw_node = self.extract_raw_node(matchobj)
            if raw_node.string:
                children.append(raw_node)

            # Dispatch job between @-symbol and scope closing
            stop_char = matchobj.group('stop_char')
            if stop_char == '@':
                self.curr_pos = raw_node.end
                children.append(self.parse_at_expr())
            else:
                self.curr_pos = matchobj.end()
                return Fragments(start_pos, raw_node.end, children)

    def parse_at_expr(self) -> AtExpression:
        """
        Attempt to parse different kinds of @-expressions.
        """
        node = (self.parse_delimited_lone_identifier()
                or self.parse_at_expr_recursive_fragments())
        if node is None:
            raise SyntaxError(f"unrecognized @-expression at pos {self.curr_pos}")
        return node

    def parse_delimited_lone_identifier(self) -> Optional[AtExpression]:
        """
        Parse the delimited lone identifier from the @-expression
        which has the form of `@|identifier|`.
        """
        prefix_matchobj = DELIMITED_LONE_ID_RE.match(self.input_string, self.curr_pos)
        if prefix_matchobj is None:
            return None

        start, self.curr_pos = prefix_matchobj.span()
        id_node = self.extract_id_node(prefix_matchobj)

        return AtExpression(start, self.curr_pos, id_node, {}, None)

    def parse_at_expr_recursive_fragments(self) -> Optional[AtExpression]:
        """
        Parse the normal version of @-expression with recursive fragments.
        """
        prefix_matchobj = NORMAL_AT_PREFIX_RE.match(self.input_string, self.curr_pos)
        if prefix_matchobj is None:
            return None

        start, self.curr_pos = prefix_matchobj.span()
        id_node = self.extract_id_node(prefix_matchobj)

        open_pattern = self.extract_scope_opening()
        fragments_node = self.parse_at_expr_fragments(open_pattern)

        return AtExpression(start, self.curr_pos, id_node, {}, fragments_node)

    def extract_scope_opening(self) -> str:
        """
        Find the scope opening of the current @-expression.
        """
        matchobj = SCOPE_OPENING_RE.match(self.input_string, self.curr_pos)
        if matchobj is None:
            raise SyntaxError(f"improper scope opening at pos {self.curr_pos}")

        self.curr_pos = matchobj.end()
        return matchobj.group()

    @staticmethod
    def extract_raw_node(matchobj: Match) -> RawString:
        """
        Construct RawString node based on the given match object
        with group named **raw**.
        """
        text = matchobj.group('raw')
        start, end = matchobj.span('raw')
        return RawString(start, end, text)

    @staticmethod
    def extract_id_node(matchobj: Match) -> Identifier:
        """
        Construct Identifier node based on the given match object
        with group named **identifier**.
        """
        name = matchobj.group('identifier')
        start, end = matchobj.span('identifier')
        return Identifier(start, end, name)
