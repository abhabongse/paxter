"""
Recursive descent parser of Paxter language.
"""
from dataclasses import dataclass, field
from typing import List, Match, Tuple

from paxter.core.charloc import CharLoc
from paxter.core.data import (
    Command, Fragment, FragmentList, Identifier, Number, Operator, Text, TokenList,
)
from paxter.core.enclosing import EnclosingPattern, GlobalEnclosingPattern
from paxter.core.exceptions import PaxterSyntaxError
from paxter.core.lexers import LEXER

__all__ = ['ParseContext']

OPENED_TO_CLOSED_SCOPE_TRANS = str.maketrans('([{', ')]}')


@dataclass
class ParseContext:
    """
    Implements a recursive descent parser for Paxter language text input.

    To utilize this class, provide the input text to the constructor,
    and the resulting parsed tree node will be generated upon instantiation.
    """
    #: Document source text
    input_text: str

    #: Root node of the parsed tree
    tree: FragmentList = field(init=False)

    def __post_init__(self):
        self.tree = self._parse_global_fragment_list()

    def _parse_global_fragment_list(self) -> FragmentList:
        """
        Parses the entirety of the already provided input text
        for the global-level fragment list from the very beginning.
        """
        end_pos, node = self._inner_parse_fragment_list(0, GlobalEnclosingPattern())
        if end_pos != len(self.input_text):  # pragma: no cover
            raise RuntimeError("unexpected error; input text not fully consumed")
        return node

    def _inner_parse_fragment_list(
            self, next_pos: int, enclosing: EnclosingPattern,
    ) -> Tuple[int, FragmentList]:
        """
        Subroutinely parses the input expecting a list of fragment nodes
        starting from the given position indicated by ``next_pos``.
        This method is called when parsing the global-level input
        or when parsing under a scope enclosed by braces pattern.
        """
        start_pos = next_pos
        children: List[Fragment] = []

        while True:
            # Attempts to match the next break pattern
            break_matchobj = enclosing.rec_break_re.match(self.input_text, next_pos)
            if break_matchobj is None:
                self._cannot_match_enclosing(start_pos, enclosing.left, enclosing.right)

            # Append non-empty text node to children list
            text_node = Text.from_matchobj(
                break_matchobj, 'inner', enclosing=EnclosingPattern(left=''),
            )
            if text_node.inner:
                children.append(text_node)

            # Dispatch parsing between the @-command switch
            # and the closing (i.e. right) pattern
            next_pos = break_matchobj.end()
            break_char = break_matchobj.group('break')
            if break_char == '@':
                next_pos, result_node = self._parse_at_expr(next_pos)
                children.append(result_node)
            else:
                break

        end_pos = break_matchobj.end('inner')
        fragment_list_node = FragmentList(start_pos, end_pos, children, enclosing)
        return next_pos, fragment_list_node

    def _parse_at_expr(self, next_pos: int) -> Tuple[int, Fragment]:
        """
        Parses at expressions starting from right after @-symbol.
        This method is the wraps over the actual working method
        and gives the final touch to the output.
        """
        next_pos, command_node = self._parse_2nd_level_at_expr(next_pos)
        if isinstance(command_node, (FragmentList, Text)):
            command_node.at_prefix = True
        return next_pos, command_node

    def _parse_2nd_level_at_expr(self, next_pos: int) -> Tuple[int, Fragment]:
        """
        Parses at expressions starting from right after @-symbol.
        Attempts to dispatch the parsing according to lookahead patterns.
        """
        matchobj = LEXER.id_re.match(self.input_text, next_pos)
        if matchobj:
            return self._parse_cmd_id_intro(matchobj)

        matchobj = LEXER.left_bar_re.match(self.input_text, next_pos)
        if matchobj:
            return self._parse_cmd_bar_intro(matchobj)

        matchobj = LEXER.left_brace_re.match(self.input_text, next_pos)
        if matchobj:
            return self._parse_fragment_list(matchobj)

        matchobj = LEXER.left_quote_re.match(self.input_text, next_pos)
        if matchobj:
            return self._parse_text(matchobj)

        matchobj = LEXER.symbol_re.match(self.input_text, next_pos)
        if matchobj:
            return self.parse_symbol_phrase(matchobj)

        self._invalid_command(next_pos)

    def _parse_cmd_id_intro(self, id_matchobj: Match[str]) -> Tuple[int, Command]:
        """
        Continues parsing the intro section of the Command
        by using the identifier name content as the intro section.
        """
        cmd_start_pos, next_pos = id_matchobj.span()
        intro = id_matchobj.group('id')
        enclosing = EnclosingPattern(left='')
        return self._parse_cmd_after_intro(next_pos, cmd_start_pos, intro, enclosing)

    def _parse_cmd_bar_intro(
            self, left_bar_matchobj: Match[str],
    ) -> Tuple[int, Command]:
        """
        Continues parsing the intro section of the Command
        which is enclosed by the bar pattern.
        """
        cmd_start_pos, next_pos = left_bar_matchobj.span()
        enclosing = EnclosingPattern(left=left_bar_matchobj.group('left'))

        inner_matchobj = enclosing.non_rec_break_re.match(self.input_text, next_pos)
        if inner_matchobj is None:
            self._cannot_match_enclosing(next_pos, enclosing.left, enclosing.right)

        next_pos = inner_matchobj.end()
        intro = inner_matchobj.group('inner')
        return self._parse_cmd_after_intro(next_pos, cmd_start_pos, intro, enclosing)

    def _parse_cmd_after_intro(
            self, next_pos: int, cmd_start_pos: int,
            intro: str, intro_enclosing: EnclosingPattern,
    ) -> Tuple[int, Command]:
        """
        Continues parsing the Command after the intro section.
        """
        # Parses for option section (square brackets)
        left_bracket_matchobj = LEXER.left_bracket_re.match(self.input_text, next_pos)
        if left_bracket_matchobj:
            next_pos = left_bracket_matchobj.end()
            next_pos, options = self._parse_options(next_pos)
        else:
            options = None

        # Parses for main argument
        left_brace_matchobj = LEXER.left_brace_re.match(self.input_text, next_pos)
        if left_brace_matchobj:
            next_pos, main_arg_node = self._parse_fragment_list(left_brace_matchobj)
        else:
            quote_matchobj = LEXER.left_quote_re.match(self.input_text, next_pos)
            if quote_matchobj:
                next_pos, main_arg_node = self._parse_text(quote_matchobj)
            else:
                main_arg_node = None

        # Construct Command node
        cmd_node = Command(
            cmd_start_pos, next_pos, intro, intro_enclosing,
            options, main_arg_node,
        )
        return next_pos, cmd_node

    def _parse_fragment_list(
            self, left_brace_matchobj: Match[str],
    ) -> Tuple[int, FragmentList]:
        """
        Recursively parses the input until the enclosing right pattern
        corresponding to the enclosing left pattern
        (captured by the provided match object) is discovered.
        """
        next_pos = left_brace_matchobj.end()
        enclosing = EnclosingPattern(left=left_brace_matchobj.group('left'))
        return self._inner_parse_fragment_list(next_pos, enclosing)

    def _parse_text(self, left_quote_matchobj: Match[str]) -> Tuple[int, Text]:
        """
        Continues parsing the input for raw :class:`Text` node
        until the enclosing right pattern corresponding to the
        enclosing left pattern (captured by the provided match object)
        is discovered.
        """
        next_pos = left_quote_matchobj.end()
        enclosing = EnclosingPattern(left=left_quote_matchobj.group('left'))

        inner_matchobj = enclosing.non_rec_break_re.match(self.input_text, next_pos)
        if inner_matchobj is None:
            self._cannot_match_enclosing(next_pos, enclosing.left, enclosing.right)

        next_pos = inner_matchobj.end()
        text_node = Text.from_matchobj(inner_matchobj, 'inner', enclosing)
        return next_pos, text_node

    def parse_symbol_phrase(
            self, symbol_matchobj: Match[str],
    ) -> Tuple[int, Command]:
        """
        A special case of at-expression where a single-character symbol
        follows the @-symbol, which will result in a special Command
        with such symbol as the intro section and without anything else.
        """
        cmd_start_pos, next_pos = symbol_matchobj.span()
        symbol = symbol_matchobj.group('symbol')
        enclosing = EnclosingPattern(left='')
        cmd_node = Command(cmd_start_pos, next_pos, symbol, enclosing, None, None)
        return next_pos, cmd_node

    def _parse_options(self, next_pos: int) -> Tuple[int, TokenList]:
        """
        Parses the option section until reaching the closed square brackets.
        """
        return self._parse_options_rec(next_pos, '[')

    def _parse_options_rec(
            self, next_pos: int, opened_char: str,
    ) -> Tuple[int, TokenList]:
        """
        Recursively parses the option section
        until reaching the given breaking character.
        """
        start_pos = next_pos
        expected_closed_char = opened_char.translate(OPENED_TO_CLOSED_SCOPE_TRANS)
        children = []

        while True:
            token_matchobj = LEXER.option_token_re.match(self.input_text, next_pos)
            next_pos = token_matchobj.end()

            # Attempts to extract identifier node
            if token_matchobj.group('id'):
                id_node = Identifier.from_matchobj(token_matchobj, 'id')
                children.append(id_node)
                continue

            # Attempts to extract operator node
            if token_matchobj.group('op'):
                op_node = Operator.from_matchobj(token_matchobj, 'op')
                children.append(op_node)
                continue

            # Attempts to extract number literal node
            if token_matchobj.group('num'):
                num_node = Number.from_matchobj(token_matchobj, 'num')
                children.append(num_node)
                continue

            char = token_matchobj.group('char')

            # Attempts to parse the command
            if char == '@':
                next_pos, command_node = self._parse_at_expr(next_pos)
                children.append(command_node)
                continue

            # Attempts to parse a list of tokens in sub-level
            if isinstance(char, str) and char in '([{':
                next_pos, token_list_node = self._parse_options_rec(next_pos, char)
                children.append(token_list_node)
                continue

            # Asserts that the character matches the expected closed character.
            # Return the token list if this is the case.
            if isinstance(char, str) and char == expected_closed_char:
                end_pos = token_matchobj.start()
                return next_pos, TokenList(start_pos, end_pos, children)

            # Else, something was wrong at the parsing,
            # perhaps reaching the end of text or found unmatched parenthesis.
            self._cannot_match_enclosing(start_pos, opened_char, expected_closed_char)

    def _cannot_match_enclosing(self, pos: int, left_pattern: str, right_pattern: str):
        """
        Raises syntax error for failing to match enclosing right pattern
        to the corresponding enclosing left pattern.
        """
        raise PaxterSyntaxError(
            f"cannot match enclosing right pattern {right_pattern!r} "
            f"to the left pattern {left_pattern!r} at %(pos)s",
            pos=CharLoc(self.input_text, pos),
        )

    def _invalid_command(self, pos: int):
        """
        Raises syntax error for failing to parse @-command.
        """
        raise PaxterSyntaxError(
            "invalid expression after @-command at %(pos)s",
            pos=CharLoc(self.input_text, pos),
        )
