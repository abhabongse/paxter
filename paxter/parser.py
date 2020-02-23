"""
Recursive descent parser for Paxter experimental language.
"""
import functools
import re
from typing import List, Match, NamedTuple, Pattern

from paxter.data import (
    AtExprFunc, AtExprMacro, BaseNode, Fragments, Identifier, RawText,
)


class ParseResult(NamedTuple):
    end_pos: int
    node: BaseNode


#  _____ _ _
# |  ___| (_)_ __  _ __   ___ _ __ ___
# | |_  | | | '_ \| '_ \ / _ \ '__/ __|
# |  _| | | | |_) | |_) |  __/ |  \__ \
# |_|   |_|_| .__/| .__/ \___|_|  |___/
#           |_|   |_|

LEFT_TO_RIGHT_TRANS = str.maketrans("#<{", "#>}")


def left_to_right(left_pattern: str) -> str:
    """
    Converts the left (opening) pattern into right (closing) pattern
    (such as `"<##<{"` into `"}>##>"`).
    """
    return left_pattern.translate(LEFT_TO_RIGHT_TRANS)[::-1]


#  _____     _              _
# |_   _|__ | | _____ _ __ (_)_______ _ __ ___
#   | |/ _ \| |/ / _ \ '_ \| |_  / _ \ '__/ __|
#   | | (_) |   <  __/ | | | |/ /  __/ |  \__ \
#   |_|\___/|_|\_\___|_| |_|_/___\___|_|  |___/
#

AT_EXPR_MACRO_PREFIX_RE = (
    re.compile(r'@(?P<identifier>(?:[A-Za-z_][A-Za-z0-9_]*)?!)', flags=re.DOTALL)
)
AT_EXPR_FUNC_PREFIX_RE = (
    re.compile(r'@(?P<identifier>[A-Za-z_][A-Za-z0-9_]*)', flags=re.DOTALL)
)
GLOBAL_BREAK_RE = re.compile(rf'(?P<raw>.*?)(?P<break>@|\Z)', flags=re.DOTALL)
LEFT_RE = re.compile(r'[#<]*{', flags=re.DOTALL)


@functools.lru_cache(maxsize=None)
def compile_fragment_break_re(right_pattern: str) -> Pattern[str]:
    """
    Compiles regular expression to match some raw strings
    followed by @-symbol or the given right (closing) pattern.
    """
    escaped_right_pattern = re.escape(right_pattern)
    return re.compile(rf'(?P<raw>.*?)(?P<break>@|{escaped_right_pattern})',
                      flags=re.DOTALL)


@functools.lru_cache(maxsize=None)
def compile_raw_text_break_re(right_pattern: str) -> Pattern[str]:
    """
    Compiles regular expression to match some raw strings
    followed by the given right (closing) pattern.
    """
    escaped_right_pattern = re.escape(right_pattern)
    return re.compile(rf'(?P<raw>.*?)(?P<break>{escaped_right_pattern})',
                      flags=re.DOTALL)


#  ____
# |  _ \ __ _ _ __ ___  ___ _ __
# | |_) / _` | '__/ __|/ _ \ '__|
# |  __/ (_| | |  \__ \  __/ |
# |_|   \__,_|_|  |___/\___|_|
#

class Paxter:
    """
    Recursive descent parser for Paxter experimental language.

    The constructor for this class should _not_ be called directly;
    instead, use class method `Paxter.parse` instead.
    """
    input_text: str
    parsed_tree: Fragments

    def __init__(self, input_text: str):
        self.input_text = input_text
        self.parsed_tree = self.parse_global_fragments()

    @classmethod
    def parse(cls, input_text: str) -> Fragments:
        """
        Use this class method to perform parsing on input text.
        """
        parsed_obj = cls(input_text)
        return parsed_obj.parsed_tree

    def parse_global_fragments(self) -> Fragments:
        """
        Parse global fragments until the end of input text.
        """
        end_pos, node = self.parse_fragments_inner(0, r'\A', r'\Z', GLOBAL_BREAK_RE)
        assert end_pos == len(self.input_text), (
            f"input text not fully consumed; stopped at pos {end_pos}"
        )
        return node

    def parse_nested_fragments(
            self, start_pos: int, left_pattern: str
    ) -> ParseResult:
        """
        Parse fragments inside @-expression function until reaching
        the right (closing) pattern based on the given left (opening) pattern.
        """
        right_pattern = left_to_right(left_pattern)
        break_re = compile_fragment_break_re(right_pattern)
        return self.parse_fragments_inner(
            start_pos, left_pattern, right_pattern, break_re,
        )

    def parse_fragments_inner(
            self, start_pos: int,
            left_pattern: str, right_pattern: str, break_re: Pattern[str],
    ) -> ParseResult:
        """
        Parse input string within the fragments scope.

        It uses the given `break_re` to match some raw strings
        followed by @-symbol or the right (closing) pattern.
        If @-symbol is encountered, then it calls other methods in order to
        parse @-expressions, and the process repeats from the beginning again.
        Otherwise, if right (closing) pattern has been found,
        the parsing of the current fragments terminates immediately.
        """
        curr_pos = start_pos
        children: List[BaseNode] = []
        while True:
            # Tries to match the @-symbol or the right (closing) pattern
            mobj = break_re.match(self.input_text, curr_pos)
            if mobj is None:
                raise SyntaxError(
                    f"cannot find matched closing pattern {right_pattern!r} "
                    f"to the opening pattern {left_pattern!r} "
                    f"at position {start_pos}",
                )

            # Append non-empty raw text to children list
            raw_node = self.extract_raw_node(mobj)
            if raw_node.string:
                children.append(raw_node)

            # Dispatch parsing between @-symbol and right (closing) pattern
            break_char = mobj.group('break')
            if break_char == '@':
                curr_pos, result_node = self.parse_at_expr(raw_node.end)
                children.append(result_node)
            else:
                return ParseResult(
                    end_pos=mobj.end(),
                    node=Fragments(start_pos, raw_node.end, children),
                )

    def parse_at_expr(self, start_pos: int) -> ParseResult:
        """
        Parse different kinds of @-expressions.
        """
        if AT_EXPR_MACRO_PREFIX_RE.match(self.input_text, start_pos):
            return self.parse_at_expr_macro(start_pos)
        elif AT_EXPR_FUNC_PREFIX_RE.match(self.input_text, start_pos):
            return self.parse_at_expr_others(start_pos)
        else:
            raise SyntaxError(
                f"expecting identifier after @-symbol at position {start_pos}",
            )

    def parse_at_expr_macro(self, start_pos: int) -> ParseResult:
        """
        Parse @-expression macro.
        """
        # Parse @-symbol and identifier
        prefix_mobj = AT_EXPR_MACRO_PREFIX_RE.match(self.input_text, start_pos)
        if prefix_mobj is None:
            raise RuntimeError("something went wrong")

        id_node = self.extract_id_node(prefix_mobj)
        next_pos = prefix_mobj.end()

        # Parse left (opening) pattern
        left_pattern_mobj = LEFT_RE.match(self.input_text, next_pos)
        if left_pattern_mobj is None:
            raise SyntaxError(f"improper opening pattern at pos {next_pos}")

        # Extract left (opening) and compute right (closing) pattern
        left_pattern = left_pattern_mobj.group()
        right_pattern = left_to_right(left_pattern)
        break_re = compile_raw_text_break_re(right_pattern)
        next_pos = left_pattern_mobj.end()

        # Parse right (closing) pattern
        raw_mobj = break_re.match(self.input_text, next_pos)
        if raw_mobj is None:
            raise SyntaxError(
                f"cannot find matched closing pattern {right_pattern!r} "
                f"to the opening pattern {left_pattern!r} "
                f"at position {next_pos}",
            )

        # Construct @-expression macro node
        raw_node = self.extract_raw_node(raw_mobj)
        end_pos = raw_mobj.end()
        return ParseResult(
            end_pos=end_pos,
            node=AtExprMacro(start_pos, end_pos, id_node, raw_node),
        )

    def parse_at_expr_others(self, start_pos: int) -> ParseResult:
        """
        Parse @-expression without exclamation mark!
        """
        # Parse @-symbol and identifier
        prefix_mobj = AT_EXPR_FUNC_PREFIX_RE.match(self.input_text, start_pos)
        if prefix_mobj is None:
            raise RuntimeError("something went wrong")

        id_node = self.extract_id_node(prefix_mobj)
        next_pos = prefix_mobj.end()

        # TODO: implement options

        # Parse left (opening) pattern
        left_pattern_mobj = LEFT_RE.match(self.input_text, next_pos)
        if left_pattern_mobj is None:

            # Assume @id -> @!{id}
            raw_node = RawText(id_node.start, id_node.end, id_node.name)
            id_node = Identifier(id_node.start, id_node.start, "!")
            return ParseResult(
                end_pos=next_pos,
                node=AtExprMacro(start_pos,next_pos,id_node,raw_node),
            )

        # Extract left (opening) pattern
        left_pattern = left_pattern_mobj.group()
        next_pos = left_pattern_mobj.end()

        # Construct @-expression function node
        id_node = self.extract_id_node(prefix_mobj)
        end_pos, fragments_node = self.parse_nested_fragments(next_pos, left_pattern)
        return ParseResult(
            end_pos=end_pos,
            node=AtExprFunc(start_pos, end_pos, id_node, fragments_node, {}),
        )

    @staticmethod
    def extract_raw_node(matchobj: Match) -> RawText:
        """
        Construct RawText node based on the given matched object
        with the group named **raw**.
        """
        string = matchobj.group('raw')
        start, end = matchobj.span('raw')
        return RawText(start, end, string)

    @staticmethod
    def extract_id_node(matchobj: Match) -> Identifier:
        """
        Construct Identifier node based on the given matched object
        with the group named **identifier**.
        """
        name = matchobj.group('identifier')
        start, end = matchobj.span('identifier')
        return Identifier(start, end, name)
