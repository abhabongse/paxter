"""
Recursive descent parser for Paxter language
"""
from typing import List, Match, Optional, Pattern, Tuple

from paxter.core.data import (BaseFragment, FragmentList, KeyValue, PaxterFunc,
                              PaxterMacro, PaxterPhrase, Text)
from paxter.core.exceptions import PaxterSyntaxError
from paxter.core.lexers import Lexer

__all__ = ['Parser']


class Parser:
    """
    Implements recursive descent parser for Paxter experimental language.

    Args:
        lexer: Lexer with customized switch symbol character specified.
            If not provided, a default lexer with `@` switch symbol is used.
    """
    lexer: Lexer

    def __init__(self, lexer: Optional[Lexer] = None):
        self.lexer = lexer or Lexer(switch='@')

    def parse(self, body: str) -> FragmentList:
        """
        Parse global fragments until the end of input text body.
        """
        end_pos, node = self.parse_inner_fragments(
            body, 0,
            r'\A', r'\Z', self.lexer.global_break_re,
        )
        if end_pos != len(body):
            raise RuntimeError("unexpected error; input text body not fully consumed")
        return node

    def parse_nested_fragments(
            self, body: str, next_pos: int,
            left_pattern: str,
    ) -> Tuple[int, FragmentList]:
        """
        Parse fragments inside Paxter expression function until reaching the right
        (i.e. closing) pattern based on the given left (i.e. opening) pattern.
        """
        right_pattern = self.lexer.flip_pattern(left_pattern)
        break_re = self.lexer.fragment_break_re(right_pattern)
        return self.parse_inner_fragments(
            body, next_pos,
            left_pattern, right_pattern, break_re,
        )

    def parse_inner_fragments(
            self, body: str, next_pos: int,
            left_pattern: str, right_pattern: str, break_re: Pattern[str],
    ) -> Tuple[int, FragmentList]:
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
            break_matchobj = break_re.match(body, next_pos)
            if break_matchobj is None:
                self._cannot_match_right_pattern(
                    body, next_pos,
                    left_pattern, right_pattern,
                )

            # Append non-empty text node to children list
            text_node = self.lexer.extract_text_node(break_matchobj)
            if text_node.string:
                children.append(text_node)

            # Dispatch parsing between the switch symbol character
            # and the right (i.e. closing) pattern
            break_char = break_matchobj.group('break')
            if break_char == self.lexer.switch:
                next_pos, result_node = self.parse_switch_symbol(
                    body, text_node.end_pos,
                )
                children.append(result_node)
            else:
                end_pos = break_matchobj.end()
                return end_pos, FragmentList(start_pos, text_node.end_pos, children)

    def parse_switch_symbol(
            self, body: str, next_pos: int,
    ) -> Tuple[int, BaseFragment]:
        """
        Attempts to parse all kinds of Paxter expressions.
        """
        if self.lexer.paxter_macro_prefix_re.match(body, next_pos):
            return self.parse_paxter_macro_pattern(body, next_pos)
        if self.lexer.paxter_func_prefix_re.match(body, next_pos):
            return self.parse_paxter_func_pattern(body, next_pos)
        if self.lexer.paxter_phrase_prefix_re.match(body, next_pos):
            return self.parse_paxter_phrase_pattern(body, next_pos)
        if self.lexer.paxter_string_prefix_re.match(body, next_pos):
            return self.parse_paxter_string_pattern(body, next_pos)
        raise PaxterSyntaxError(
            f"invalid expression after symbol {self.lexer.switch!r} at {{next_pos}}",
            body=body, positions={'next_pos': next_pos},
        )

    def parse_paxter_macro_pattern(
            self, body: str, next_pos: int,
    ) -> Tuple[int, PaxterMacro]:
        """
        Parses Paxter macro.
        """
        start_pos = next_pos

        # Parse switch symbol character and identifier
        prefix_matchobj = self.lexer.paxter_macro_prefix_re.match(body, next_pos)
        if prefix_matchobj is None:
            raise RuntimeError("something went horribly wrong")
        id_node = self.lexer.extract_id_node(prefix_matchobj)
        next_pos = prefix_matchobj.end()

        # Parse the left (i.e. opening) pattern
        left_brace_matchobj = self.lexer.left_brace_re.match(body, next_pos)
        if left_brace_matchobj is None:
            self._improper_left_pattern(body, next_pos)

        # Extract text node based on the found left (i.e. opening) pattern
        # and use it to create a PaxterMacro node
        end_pos, text_node = self.parse_inner_text(body, left_brace_matchobj)
        return end_pos, PaxterMacro(start_pos, end_pos, id_node, text_node)

    def parse_paxter_phrase_pattern(
            self, body: str, next_pos: int,
    ) -> Tuple[int, PaxterPhrase]:
        """
        Parses Paxter phrase.
        """
        start_pos = next_pos

        # Parse the left (i.e. opening) pattern
        left_brace_matchobj = self.lexer.paxter_phrase_prefix_re.match(body, next_pos)
        if left_brace_matchobj is None:
            raise RuntimeError("something went horribly wrong")

        # Extract text node based on the found left (i.e. opening) pattern
        # and use it to create a PaxterPhrase node
        end_pos, text_node = self.parse_inner_text(body, left_brace_matchobj)
        return end_pos, PaxterPhrase(start_pos, end_pos, text_node)

    def parse_paxter_string_pattern(
            self, body: str, next_pos: int,
    ) -> Tuple[int, Text]:
        """
        Parses Paxter string literal.
        """
        start_pos = next_pos

        # Parses the left (i.e. opening) pattern
        left_quote_matchobj = self.lexer.paxter_string_prefix_re.match(body, next_pos)
        if left_quote_matchobj is None:
            raise RuntimeError("something went horribly wrong")

        # Extract text node based on the found left (i.e. opening) pattern
        # and fix the starting and ending positions before returning.
        end_pos, text_node = self.parse_inner_text(body, left_quote_matchobj)
        return end_pos, Text(start_pos, end_pos, text_node.string)

    def parse_inner_text(
            self, body: str, left_matchobj: Match[str],
    ) -> Tuple[int, Text]:
        """
        Parses input text body for the scope of text node.

        It extracts the left (i.e. opening) pattern from the given match object
        and use it to compute the break pattern of the text node.
        """
        left_pattern = left_matchobj.group('left')
        right_pattern = self.lexer.flip_pattern(left_pattern)
        break_re = self.lexer.text_break_re(right_pattern)
        next_pos = left_matchobj.end()

        # Parse for the right (i.e. closing) pattern
        text_matchobj = break_re.match(body, next_pos)
        if text_matchobj is None:
            self._cannot_match_right_pattern(
                body, next_pos,
                left_pattern, right_pattern,
            )

        # Construct text node
        text_node = self.lexer.extract_text_node(text_matchobj)
        end_pos = text_matchobj.end()
        return end_pos, text_node

    def parse_paxter_func_pattern(
            self, body: str, next_pos: int,
    ) -> Tuple[int, BaseFragment]:
        """
        Parses for either a Paxter function call or the special Paxter phrase
        when argument to the function call does not exist.
        """
        start_pos = next_pos

        # Parse switch symbol character and identifier
        prefix_matchobj = self.lexer.paxter_func_prefix_re.match(body, next_pos)
        if prefix_matchobj is None:
            raise RuntimeError("something went horribly wrong")
        id_node = self.lexer.extract_id_node(prefix_matchobj)
        next_pos = prefix_matchobj.end()

        # First attempt: parse for left square bracket
        if self.lexer.left_sq_bracket_re.match(body, next_pos):

            # TODO: reintroduce walrus operator usage
            left_bracket_matchobj = self.lexer.left_sq_bracket_re.match(body, next_pos)
            next_pos = left_bracket_matchobj.end()

            # Parse options until the right (i.e. closing) square bracket
            next_pos, opts = self.parse_inner_options(body, next_pos)

            # Parse for left (i.e. opening) brace
            left_brace_matchobj = self.lexer.left_brace_re.match(body, next_pos)
            if left_brace_matchobj is None:
                self._expected_opening_brace(body, next_pos)

        # Second attempt: parse for left (i.e. opening) brace
        elif self.lexer.left_brace_re.match(body, next_pos):
            # TODO: reintroduce walrus operator usage
            left_brace_matchobj = self.lexer.left_brace_re.match(body, next_pos)
            opts = None

        # Fallback: special case for PaxterPhrase
        else:
            text_node = Text(id_node.start_pos, id_node.end_pos, id_node.name)
            return next_pos, PaxterPhrase(start_pos, next_pos, text_node)

        # Continue extracting FragmentList node from the left brace match object
        end_pos, fragments_node = self.parse_nested_fragments(
            body=body, next_pos=left_brace_matchobj.end(),
            left_pattern=left_brace_matchobj.group(),
        )
        return end_pos, PaxterFunc(start_pos, end_pos, id_node, fragments_node, opts)

    def parse_inner_options(
            self, body: str, next_pos: int,
    ) -> Tuple[int, List[KeyValue]]:
        """
        Parses the list of options.
        """
        options = []

        # Keep on parsing the next option key-value pair
        # when the next token is not the right (i.e. closing) square bracket
        # TODO: reintroduce walrus operator usage
        while True:
            break_matchobj = self.lexer.option_break_re.match(body, next_pos)
            if break_matchobj:
                break

            # Parse the next option key-value pair
            option_matchobj = self.lexer.option_re.match(body, next_pos)
            if option_matchobj is None:
                self._expected_next_option_or_closing_bracket(body, next_pos)

            # Extract the key-value pair from match object
            kv_pair = self.lexer.extract_kv_pair(option_matchobj)
            options.append(kv_pair)
            next_pos = option_matchobj.end()

            # Parse for a comma or the abrupt right (i.e. closing) square bracket
            break_matchobj = self.lexer.comma_or_option_break_re.match(body, next_pos)
            if break_matchobj is None:
                self._expected_comma_or_closing_bracket(body, next_pos)
            if break_matchobj.group('break') == ']':
                break
            next_pos = break_matchobj.end()

        end_pos = break_matchobj.end()
        return end_pos, options

    @staticmethod
    def _cannot_match_right_pattern(
            body: str, next_pos: int,
            left_pattern: str, right_pattern: str,
    ):
        raise PaxterSyntaxError(
            f"cannot match closing pattern {right_pattern!r}"
            f"to the opening pattern {left_pattern!r} at {{next_pos}}",
            body=body, positions={'next_pos': next_pos},
        )

    @staticmethod
    def _improper_left_pattern(body: str, next_pos: int):
        raise PaxterSyntaxError(
            "improper opening pattern at {next_pos}",
            body=body, positions={'next_pos': next_pos},
        )

    @staticmethod
    def _expected_opening_brace(body: str, next_pos: int):
        raise PaxterSyntaxError(
            "expected opening brace after options at {next_pos}",
            body=body, positions={'next_pos': next_pos},
        )

    @staticmethod
    def _expected_next_option_or_closing_bracket(body: str, next_pos: int):
        raise PaxterSyntaxError(
            "expected next option or closing bracket at {next_pos}",
            body=body, positions={'next_pos': next_pos},
        )

    @staticmethod
    def _expected_comma_or_closing_bracket(body: str, next_pos: int):
        raise PaxterSyntaxError(
            "expected a comma or a closing bracket at {next_pos}",
            body=body, positions={'next_pos': next_pos},
        )
