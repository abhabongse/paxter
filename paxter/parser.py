"""
Recursive descent parser for Paxter experimental language.
"""
from typing import List, Match, NamedTuple, Pattern

from paxter.data import BaseFragment, FragmentList, Node, PaxterMacro, PaxterPhrase, \
    Text
from paxter.exceptions import PaxterSyntaxError
from paxter.lexers import Lexer


class ParseResult(NamedTuple):
    next_pos: int
    node: Node


class Parser:
    """
    Implements recursive descent parser for Paxter experimental language.

    The constructor for this class should _not_ be called directly;
    instead, use class method `Parser.run` instead.

    Args:
        body: Input text body
        switch: A single symbol character which enables (i.e. switches to)
            Paxter macro, Paxter function, or Paxter phrase
    """
    body: str
    lexer: Lexer
    parsed_tree: FragmentList

    @classmethod
    def run(cls, *args, **kwargs) -> FragmentList:
        """
        Use this class method to perform parsing on input text.
        """
        instance = cls(*args, **kwargs)
        return instance.parsed_tree

    def __init__(self, body: str, switch: str = '@'):
        self.body = body
        self.lexer = Lexer(switch)
        self.parsed_tree = self.parse_global_fragments()

    def parse_global_fragments(self) -> FragmentList:
        """
        Parse global fragments until the end of input text body.
        """
        end_pos, node = self.parse_fragments_inner(
            0, r'\A', r'\Z', self.lexer.global_break_re,
        )
        if end_pos != len(self.body):
            raise RuntimeError("unexpected error; input text body not fully consumed")
        return node

    def parse_nested_fragments(self, next_pos: int, left_pattern: str) -> ParseResult:
        """
        Parse fragments inside Paxter expression function until reaching the right
        (i.e. closing) pattern based on the given left (i.e. opening) pattern.
        """
        right_pattern = self.lexer.flip_pattern(left_pattern)
        break_re = self.lexer.fragment_break_re(right_pattern)
        return self.parse_fragments_inner(
            next_pos, left_pattern, right_pattern, break_re,
        )

    def parse_fragments_inner(
            self, next_pos: int, left_pattern: str, right_pattern: str,
            break_re: Pattern[str],
    ) -> ParseResult:
        """
        Parse input text body for the scope of fragment nodes.

        It uses the given `break_re` regular expression to non-greedily
        match some text followed by either the switch symbol character
        or the given right (i.e. closing) pattern.

        - If switch symbol character is encountered,
          it calls other methods in order to parse the Paxter expressions,
          and then the process repeats from again from the beginning.
        - Otherwise, if the right (i.e. closing) pattern has been found,
          the parsing of the current scope terminates immediately.
        """
        start_pos = next_pos
        children: List[BaseFragment] = []

        while True:
            # Tries to match the break pattern
            break_matchobj = break_re.match(self.body, next_pos)
            if break_matchobj is None:
                self._cannot_match_right_pattern(next_pos, left_pattern, right_pattern)

            # Append non-empty text node to children list
            text_node = self.lexer.extract_text_node(break_matchobj)
            if text_node.string:
                children.append(text_node)

            # Dispatch parsing between the switch symbol character
            # and the right (i.e. closing) pattern
            break_char = break_matchobj.group('break')
            if break_char == self.lexer.switch:
                next_pos, result_node = self.parse_switch_symbol(text_node.end_pos)
                children.append(result_node)
            else:
                return ParseResult(
                    next_pos=break_matchobj.end(),
                    node=FragmentList(start_pos, text_node.end_pos, children),
                )

    def parse_switch_symbol(self, next_pos: int) -> ParseResult:
        """
        Attempts to parse all kinds of Paxter expressions.
        """
        if self.lexer.paxter_macro_prefix_re.match(self.body, next_pos):
            return self.parse_paxter_macro_pattern(next_pos)
        if self.lexer.paxter_func_prefix_re.match(self.body, next_pos):
            return self.parse_paxter_func_pattern(next_pos)
        if self.lexer.paxter_phrase_prefix_re.match(self.body, next_pos):
            return self.parse_paxter_phrase_pattern(next_pos)
        if self.lexer.paxter_string_prefix_re.match(self.body, next_pos):
            return self.parse_paxter_string_pattern(next_pos)
        raise PaxterSyntaxError(
            f"invalid expression after symbol {self.lexer.switch!r} at {{next_pos}}",
            index_params={'next_pos': next_pos},
        )

    def parse_paxter_macro_pattern(self, next_pos: int) -> ParseResult:
        """
        Parses Paxter macro.
        """
        start_pos = next_pos

        # Parse switch symbol character and identifier
        prefix_matchobj = self.lexer.paxter_macro_prefix_re.match(self.body, next_pos)
        if prefix_matchobj is None:
            raise RuntimeError("something went horribly wrong")
        id_node = self.lexer.extract_id_node(prefix_matchobj)
        next_pos = prefix_matchobj.end()

        # Parse the left (i.e. opening) pattern
        left_brace_matchobj = self.lexer.left_brace_re.match(self.body, next_pos)
        if left_brace_matchobj is None:
            self._improper_left_pattern(next_pos)

        # Extract text node based on the found left (i.e. opening) pattern
        # and use it to create a PaxterMacro node
        end_pos, text_node = self.parse_text_inner(left_brace_matchobj)
        return ParseResult(
            next_pos=end_pos,
            node=PaxterMacro(start_pos, end_pos, id_node, text_node),
        )

    def parse_paxter_phrase_pattern(self, next_pos: int) -> ParseResult:
        """
        Parses Paxter phrase.
        """
        start_pos = next_pos

        # Parse the left (i.e. opening) pattern
        left_brace_matchobj = self.lexer.paxter_phrase_prefix_re.match(
            self.body, next_pos,
        )
        if left_brace_matchobj is None:
            raise RuntimeError("something went horribly wrong")

        # Extract text node based on the found left (i.e. opening) pattern
        # and use it to create a PaxterPhrase node
        end_pos, text_node = self.parse_text_inner(left_brace_matchobj)
        return ParseResult(
            next_pos=end_pos,
            node=PaxterPhrase(start_pos, end_pos, text_node),
        )

    def parse_paxter_string_pattern(self, next_pos: int) -> ParseResult:
        """
        Parses Paxter string literal.
        """
        start_pos = next_pos

        # Parses the left (i.e. opening) pattern
        left_quote_matchobj = self.lexer.paxter_string_prefix_re.match(
            self.body, next_pos,
        )
        if left_quote_matchobj is None:
            raise RuntimeError("something went horribly wrong")

        # Extract text node based on the found left (i.e. opening) pattern
        # and fix the starting and ending positions before returning.
        end_pos, text_node = self.parse_text_inner(left_quote_matchobj)
        return ParseResult(
            next_pos=end_pos,
            node=Text(start_pos, end_pos, text_node.string),
        )

    def parse_text_inner(self, left_matchobj: Match[str]) -> ParseResult:
        """
        Parse input text body for the scope of text node.

        It extracts the left (i.e. opening) pattern from the given match object
        and use it to compute the break pattern of the text node.
        """
        left_pattern = left_matchobj.group('left')
        right_pattern = self.lexer.flip_pattern(left_pattern)
        break_re = self.lexer.text_break_re(right_pattern)
        next_pos = left_matchobj.end()

        # Parse for the right (i.e. closing) pattern
        text_matchobj = break_re.match(self.body, next_pos)
        if text_matchobj is None:
            self._cannot_match_right_pattern(next_pos, left_pattern, right_pattern)

        # Construct text node
        text_node = self.lexer.extract_text_node(text_matchobj)
        end_pos = text_matchobj.end()
        return ParseResult(next_pos=end_pos, node=text_node)

    def parse_paxter_func_pattern(self, next_pos: int) -> ParseResult:
        raise NotImplementedError

        # # Parse @-symbol and identifier
        # prefix_mobj = AT_EXPR_FUNC_PREFIX_RE.match(self.input_text, start_pos)
        # if prefix_mobj is None:
        #     raise RuntimeError("something went wrong")
        #
        # id_node = self.extract_id_node(prefix_mobj)
        # next_pos = prefix_mobj.end()
        #
        # # TODO: implement options
        #
        # # Parse left (opening) pattern
        # left_pattern_mobj = LEFT_RE.match(self.input_text, next_pos)
        # if left_pattern_mobj is None:
        #     # Assume @id -> @!{id}
        #     raw_node = RawText(id_node.start, id_node.end, id_node.name)
        #     id_node = Identifier(id_node.start, id_node.start, "!")
        #     return ParseResult(
        #         end_pos=next_pos,
        #         node=AtExprMacro(start_pos, next_pos, id_node, raw_node),
        #     )
        #
        # # Extract left (opening) pattern
        # left_pattern = left_pattern_mobj.group()
        # next_pos = left_pattern_mobj.end()
        #
        # # Construct @-expression function node
        # id_node = self.extract_id_node(prefix_mobj)
        # end_pos, fragments_node = self.parse_nested_fragments(next_pos, left_pattern)
        # return ParseResult(
        #     end_pos=end_pos,
        #     node=AtExprFunc(start_pos, end_pos, id_node, fragments_node, {}),
        # )

    @staticmethod
    def _cannot_match_right_pattern(
            next_pos: int, left_pattern: str, right_pattern: str,
    ):
        raise PaxterSyntaxError(
            f"cannot find matched closing pattern {right_pattern!r}"
            f"to the opening pattern {left_pattern!r} at {{next_pos}}",
            index_params={'next_pos': next_pos},
        )

    @staticmethod
    def _improper_left_pattern(next_pos: int):
        raise PaxterSyntaxError(
            "improper opening pattern at {next_pos}",
            index_params={'next_pos': next_pos},
        )
