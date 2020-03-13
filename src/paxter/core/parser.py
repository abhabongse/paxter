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
        if end_pos != len(body):  # pragma: no cover
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
                self._cannot_match_right_pattern(next_pos, left_pattern, right_pattern)

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
        by looking ahead for desired patterns.
        """
        prefix_matchobj = self.lexer.paxter_macro_prefix_re.match(body, next_pos)
        if prefix_matchobj:
            return self.parse_paxter_macro(body, next_pos, prefix_matchobj)

        prefix_matchobj = self.lexer.paxter_func_prefix_re.match(body, next_pos)
        if prefix_matchobj:
            return self.parse_paxter_func_or_phrase(body, next_pos, prefix_matchobj)

        prefix_matchobj = self.lexer.paxter_phrase_prefix_re.match(body, next_pos)
        if prefix_matchobj:
            return self.parse_paxter_phrase(body, next_pos, prefix_matchobj)

        prefix_matchobj = self.lexer.paxter_string_prefix_re.match(body, next_pos)
        if prefix_matchobj:
            return self.parse_paxter_string(body, next_pos, prefix_matchobj)

        raise PaxterSyntaxError(
            f"invalid expression after symbol {self.lexer.switch!r} "
            "at {pos}",
            positions={'pos': next_pos},
        )

    def parse_paxter_macro(
            self, body: str, next_pos: int,
            prefix_matchobj: Match[str],
    ) -> Tuple[int, PaxterMacro]:
        """
        Continues parsing for PaxterMarco.
        """
        start_pos = next_pos
        id_node = self.lexer.extract_id_node(prefix_matchobj)
        next_pos = prefix_matchobj.end()

        # Attempt: parse for left square bracket
        left_bracket_matchobj = self.lexer.left_sq_bracket_re.match(body, next_pos)
        if left_bracket_matchobj:
            next_pos = left_bracket_matchobj.end()

            # Parse options until the right (i.e. closing) square bracket
            next_pos, opts = self.parse_inner_options(body, next_pos)
        else:
            opts = None

        # Parse the left (i.e. opening) pattern
        left_brace_matchobj = self.lexer.left_brace_re.match(body, next_pos)
        if left_brace_matchobj is None:
            self._expected_opening_brace(next_pos)

        # Extract text node based on the found left (i.e. opening) pattern
        # and use it to create a PaxterMacro node
        end_pos, text_node = self.parse_inner_text(body, left_brace_matchobj)
        return end_pos, PaxterMacro(start_pos, end_pos, id_node, opts, text_node)

    def parse_paxter_phrase(
            self, body: str, next_pos: int,
            prefix_matchobj: Match[str],
    ) -> Tuple[int, PaxterPhrase]:
        """
        Continues parsing for the PaxterPhrase.

        It reuses the prefix match object provided which already captures
        the left (i.e. opening) pattern inside inner text parser function.
        """
        start_pos = next_pos
        end_pos, text_node = self.parse_inner_text(body, prefix_matchobj)
        return end_pos, PaxterPhrase(start_pos, end_pos, text_node)

    def parse_paxter_string(
            self, body: str, next_pos: int,
            prefix_matchobj: Match[str],
    ) -> Tuple[int, Text]:
        """
        Continues parsing for the Paxter string literal.

        It reuses the prefix match object provided which already captures
        the left (i.e. opening) pattern inside inner text parser function.
        """
        start_pos = next_pos
        end_pos, text_node = self.parse_inner_text(body, prefix_matchobj)
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
            self._cannot_match_right_pattern(next_pos, left_pattern, right_pattern)

        # Construct text node
        text_node = self.lexer.extract_text_node(text_matchobj)
        end_pos = text_matchobj.end()
        return end_pos, text_node

    def parse_paxter_func_or_phrase(
            self, body: str, next_pos: int,
            prefix_matchobj: Match[str],
    ) -> Tuple[int, BaseFragment]:
        """
        Continues parsing the Paxter function call pattern
        for either PaxterFunc or PaxterPhrase
        when argument to the function call does not exist.
        """
        start_pos = next_pos
        id_node = self.lexer.extract_id_node(prefix_matchobj)
        next_pos = prefix_matchobj.end()

        # First attempt: parse for left square bracket
        left_bracket_matchobj = self.lexer.left_sq_bracket_re.match(body, next_pos)
        if left_bracket_matchobj:
            next_pos = left_bracket_matchobj.end()

            # Parse options until the right (i.e. closing) square bracket
            next_pos, opts = self.parse_inner_options(body, next_pos)

            # Parse for left (i.e. opening) brace
            left_brace_matchobj = self.lexer.left_brace_re.match(body, next_pos)
            if left_brace_matchobj is None:
                self._expected_opening_brace(next_pos)
        else:
            # Second attempt: parse for left (i.e. opening) brace
            left_brace_matchobj = self.lexer.left_brace_re.match(body, next_pos)
            if left_brace_matchobj:
                opts = None
            else:
                # Fallback: special case for PaxterPhrase
                text_node = Text(id_node.start_pos, id_node.end_pos, id_node.name)
                return next_pos, PaxterPhrase(start_pos, next_pos, text_node)

        # Falling through from the above if-statements,
        # continue extracting FragmentList node
        # from the left brace match object
        end_pos, fragments_node = self.parse_nested_fragments(
            body=body, next_pos=left_brace_matchobj.end(),
            left_pattern=left_brace_matchobj.group(),
        )
        return end_pos, PaxterFunc(start_pos, end_pos, id_node, opts, fragments_node)

    def parse_inner_options(
            self, body: str, next_pos: int,
    ) -> Tuple[int, List[KeyValue]]:
        """
        Parses for the list of options.
        """
        options = []

        while True:
            # Keep on parsing the next option key-value pair
            # when the next token is not the right (i.e. closing) square bracket
            break_matchobj = self.lexer.option_break_re.match(body, next_pos)
            if break_matchobj:
                break  # end position will be extracted

            # Parse the next option key-value pair
            kv_pair_matchobj = self.lexer.kv_pair_re.match(body, next_pos)
            if kv_pair_matchobj is None:
                self._expected_next_option_or_closing_bracket(next_pos)

            # Extract the key-value pair from match object
            kv_pair = self.lexer.extract_kv_pair(kv_pair_matchobj)
            options.append(kv_pair)
            next_pos = kv_pair_matchobj.end()

            # Parse for a comma or the abrupt right (i.e. closing) square bracket
            break_matchobj = self.lexer.comma_or_option_break_re.match(body, next_pos)
            if break_matchobj is None:
                self._expected_comma_or_closing_bracket(next_pos)
            if break_matchobj.group('break') == ']':
                break  # end position will be extracted
            next_pos = break_matchobj.end()

        end_pos = break_matchobj.end()
        return end_pos, options

    @staticmethod
    def _cannot_match_right_pattern(pos: int, left_pattern: str, right_pattern: str):
        right_pattern = right_pattern.replace('}', '}}')
        left_pattern = left_pattern.replace('{', '{{')
        raise PaxterSyntaxError(
            f"cannot match closing pattern {right_pattern!r} "
            f"to the opening pattern {left_pattern!r} "
            "at {pos}",
            positions={'pos': pos},
        )

    @staticmethod
    def _expected_opening_brace(pos: int):
        raise PaxterSyntaxError(
            "expected opening brace after options at {pos}",
            positions={'pos': pos},
        )

    @staticmethod
    def _expected_next_option_or_closing_bracket(pos: int):
        raise PaxterSyntaxError(
            "expected next option or a closing bracket at {pos}",
            positions={'pos': pos},
        )

    @staticmethod
    def _expected_comma_or_closing_bracket(pos: int):
        raise PaxterSyntaxError(
            "expected a comma or a closing bracket at {pos}",
            positions={'pos': pos},
        )
