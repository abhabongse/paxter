"""
Recursive descent parser of Paxter language.
"""
from dataclasses import dataclass
from typing import List, Match, Tuple, Union

from paxter.core.data import (
    Fragment, FragmentList, Identifier, Number, Operator, PaxterApply, PaxterPhrase,
    Text, TokenList,
)
from paxter.core.exceptions import PaxterSyntaxError
from paxter.core.lexers import LEXER
from paxter.core.line_col import LineCol
from paxter.core.scope_pattern import (
    EMPTY_SCOPE_PATTERN, GLOBAL_SCOPE_PATTERN, ScopePattern,
)

__all__ = ['ParseContext']

OPENED_TO_CLOSED_SCOPE_TRANS = str.maketrans('([{', ')]}')


@dataclass
class ParseContext:
    """
    Implements recursive descent parser for Paxter language.

    Use class method `Parser.parse` instead of
    creating an instance of this class directly.
    """
    input_text: str

    def parse(self):
        """
        Parses the input text starting from the beginning.
        """
        end_pos, node = self.parse_inner_fragment_list(0, GLOBAL_SCOPE_PATTERN)
        if end_pos != len(self.input_text):  # pragma: no cover
            raise RuntimeError("unexpected error; input text not fully consumed")
        return node

    def parse_inner_fragment_list(
            self, next_pos: int, scope_pattern: ScopePattern,
    ) -> Tuple[int, FragmentList]:
        """
        Parses the input text at the given position
        for the scope of fragment node list.
        This method is called at the start of global-level text
        or the start of the text within the braces pattern.
        """
        start_pos = next_pos
        children: List[Fragment] = []

        while True:
            # Tries to match the break pattern
            break_matchobj = scope_pattern.rec_break_re.match(self.input_text, next_pos)
            if break_matchobj is None:
                self.cannot_match_closed_pattern(start_pos, scope_pattern)

            # Append non-empty text node to children list
            text_node = Text.from_matchobj(break_matchobj, 'inner', EMPTY_SCOPE_PATTERN)
            if text_node.inner:
                children.append(text_node)
            next_pos = break_matchobj.end()

            # Dispatch parsing between the @-command switch
            # and the closed (i.e. right) pattern
            break_char = break_matchobj.group('break')
            if break_char == '@':
                next_pos, result_node = self.parse_command(next_pos)
                children.append(result_node)
            else:
                fragment_list_node = FragmentList(
                    start_pos, break_matchobj.end('inner'),
                    children, scope_pattern,
                )
                return next_pos, fragment_list_node

    def parse_command(self, next_pos: int) -> Tuple[int, Fragment]:
        """
        Attempts to parse all kinds of Paxter expressions
        by looking ahead for desired patterns.
        """
        next_pos, command_node = self.parse_command_2nd_level(next_pos)
        if isinstance(command_node, (FragmentList, Text)):
            command_node.is_command = True
        return next_pos, command_node

    def parse_command_2nd_level(self, next_pos: int) -> Tuple[int, Fragment]:
        """
        Attempts to parse all kinds of Paxter expressions
        by looking ahead for desired patterns.
        """
        matchobj = LEXER.id_prefix_re.match(self.input_text, next_pos)
        if matchobj:
            return self.parse_command_after_id(matchobj)

        matchobj = LEXER.brace_prefix_re.match(self.input_text, next_pos)
        if matchobj:
            return self.parse_fragment_list(matchobj)

        matchobj = LEXER.quote_prefix_re.match(self.input_text, next_pos)
        if matchobj:
            return self.parse_text(matchobj)

        matchobj = LEXER.bar_prefix_re.match(self.input_text, next_pos)
        if matchobj:
            return self.parse_normal_phrase(matchobj)

        matchobj = LEXER.symbol_re.match(self.input_text, next_pos)
        if matchobj:
            return self.parse_symbol_phrase(matchobj)

        self.invalid_command(next_pos)

    def parse_command_after_id(
            self, id_prefix_matchobj: Match[str],
    ) -> Tuple[int, Union[PaxterApply, PaxterPhrase]]:
        """
        Continues parsing the command after the identifier section.
        The result of this function could either be `PaxterApply`
        (if the options section or the main argument section exists)
        or `PaxterPhrase` (otherwise).
        """
        start_pos = id_prefix_matchobj.start()
        next_pos = id_prefix_matchobj.end()

        # Parse for options section (square brackets)
        bracket_prefix_matchobj = LEXER.bracket_prefix_re.match(
            self.input_text, next_pos,
        )
        if bracket_prefix_matchobj:
            next_pos = bracket_prefix_matchobj.end()
            next_pos, options = self.parse_options(next_pos)
        else:
            options = None

        # Parse for main arguments
        brace_prefix_matchobj = LEXER.brace_prefix_re.match(self.input_text, next_pos)
        if brace_prefix_matchobj:
            next_pos, main_arg_node = self.parse_fragment_list(brace_prefix_matchobj)
        else:
            quote_prefix_matchobj = LEXER.quote_prefix_re.match(
                self.input_text, next_pos,
            )
            if quote_prefix_matchobj:
                next_pos, main_arg_node = self.parse_text(quote_prefix_matchobj)
            else:
                main_arg_node = None

        # Create PaxterPhrase node as a special case
        if options is None and main_arg_node is None:
            result_node = PaxterPhrase.from_matchobj(
                id_prefix_matchobj, 'id', EMPTY_SCOPE_PATTERN,
            )

        # Create PaxterApply node
        else:
            id_node = Identifier.from_matchobj(id_prefix_matchobj, 'id')
            result_node = PaxterApply(
                start_pos, next_pos, id_node, options, main_arg_node,
            )

        return next_pos, result_node

    def parse_fragment_list(
            self, brace_prefix_matchobj: Match[str],
    ) -> Tuple[int, FragmentList]:
        """
        Recursively parses the input text until the closed (i.e. right)
        pattern corresponding to the opened (i.e. left) pattern
        captured by the provided match object is discovered.
        """
        next_pos = brace_prefix_matchobj.end()
        scope_pattern = ScopePattern(opened=brace_prefix_matchobj.group('opened'))

        return self.parse_inner_fragment_list(next_pos, scope_pattern)

    def parse_text(self, quote_prefix_matchobj: Match[str]) -> Tuple[int, Text]:
        """
        Continues parsing the command for `Text`
        following the pattern `@"..."`.
        """
        next_pos = quote_prefix_matchobj.end()
        scope_pattern = ScopePattern(opened=quote_prefix_matchobj.group('opened'))

        inner_matchobj = scope_pattern.non_rec_break_re.match(self.input_text, next_pos)
        if inner_matchobj is None:
            self.cannot_match_closed_pattern(next_pos, scope_pattern)

        text_node = Text.from_matchobj(inner_matchobj, 'inner', scope_pattern)
        return inner_matchobj.end(), text_node

    def parse_normal_phrase(
            self, bar_prefix_matchobj: Match[str],
    ) -> Tuple[int, PaxterPhrase]:
        """
        Continues parsing the command for `PaxterPhrase`
        following the pattern `@|...|`.
        """
        next_pos = bar_prefix_matchobj.end()
        scope_pattern = ScopePattern(opened=bar_prefix_matchobj.group('opened'))

        inner_matchobj = scope_pattern.non_rec_break_re.match(self.input_text, next_pos)
        if inner_matchobj is None:
            self.cannot_match_closed_pattern(next_pos, scope_pattern)

        phrase_node = PaxterPhrase.from_matchobj(inner_matchobj, 'inner', scope_pattern)
        return inner_matchobj.end(), phrase_node

    def parse_symbol_phrase(
            self, symbol_matchobj: Match[str],
    ) -> Tuple[int, PaxterPhrase]:
        """
        Continues parsing the command for `PaxterPhrase`
        following the pattern `@_` where `_` is a single-character symbol.
        """
        phrase_node = PaxterPhrase.from_matchobj(
            symbol_matchobj, 'symbol', EMPTY_SCOPE_PATTERN,
        )
        return symbol_matchobj.end(), phrase_node

    def parse_options(self, next_pos: int) -> Tuple[int, TokenList]:
        """
        Parses the options section until reaching the closed square brackets.
        """
        return self.parse_options_rec(next_pos, '[')

    def parse_options_rec(
            self, next_pos: int,
            opened_char: str,
    ) -> Tuple[int, TokenList]:
        """
        Recursively parses the options section
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
                next_pos, command_node = self.parse_command(next_pos)
                children.append(command_node)
                continue

            # Attempts to parse a list of tokens in sub-level
            if isinstance(char, str) and char in '([{':
                next_pos, token_list_node = self.parse_options_rec(next_pos, char)
                children.append(token_list_node)
                continue

            # Asserts that the character matches the expected closed character.
            # Return the token list if this is the case.
            if isinstance(char, str) and char == expected_closed_char:
                end_pos = token_matchobj.start()
                return next_pos, TokenList(start_pos, end_pos, children)

            # Else, something was wrong at the parsing,
            # perhaps reaching the end of text or found unmatched parenthesis.
            self.cannot_match_closed_pattern(
                start_pos, ScopePattern(opened_char, expected_closed_char),
            )

    def cannot_match_closed_pattern(self, pos: int, scope_pattern: ScopePattern):
        """
        Raises syntax error for failing to match closed pattern
        to the corresponding opened pattern.
        """
        raise PaxterSyntaxError(
            f"cannot match closed pattern {scope_pattern.closed!r} "
            f"to the opened pattern {scope_pattern.opened!r} at %(pos)s",
            pos=LineCol(self.input_text, pos),
        )

    def invalid_command(self, pos: int):
        """
        Raises syntax error for failing to parse @-command.
        """
        raise PaxterSyntaxError(
            f"invalid expression after @-command at %(pos)s",
            pos=LineCol(self.input_text, pos),
        )
