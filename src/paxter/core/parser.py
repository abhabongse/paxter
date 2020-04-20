"""
Recursive descent parser of Paxter language.
"""
from typing import List, Match, Pattern, Tuple, Union

from paxter.core.data import (
    Fragment, FragmentList, Identifier, Number, Operator,
    PaxterApply, PaxterPhrase, Text, TokenList,
)
from paxter.core.exceptions import PaxterSyntaxError
from paxter.core.lexers import LEXER

__all__ = ['Parser']

OPENED_TO_CLOSED_SCOPE_TRANS = str.maketrans('([{', ')]}')


class Parser:
    """
    Implements recursive descent parser for Paxter language.

    Use class method `Parser.parse` instead of
    creating an instance of this class directly.
    """
    input_text: str

    @classmethod
    def parse(cls, input_text: str) -> FragmentList:
        """
        Parses the given input text into the parsed tree.
        Internally, this class method creates a new instance of this class
        and calls internal methods to handle the work.
        """
        instance = cls()
        instance.input_text = input_text
        return instance._parse_global_fragments()

    def _parse_global_fragments(self):
        """
        Parses the input text starting from the beginning.
        """
        end_pos, node = self._parse_inner_fragments(
            next_pos=0,
            opened_pattern=r'\A', closed_pattern=r'\Z',
            break_re=LEXER.global_break_re,
        )
        if end_pos != len(self.input_text):  # pragma: no cover
            raise RuntimeError("unexpected error; input text not fully consumed")
        return node

    def _parse_inner_fragments(
            self, next_pos: int,
            opened_pattern: str, closed_pattern: str,
            break_re: Pattern[str],
    ) -> Tuple[int, FragmentList]:
        """
        Parses the input text at the given position
        for the scope of fragment node list.
        This method is called at the start of global-level text
        or the start of the text within the braces pattern.
        """
        children: List[Fragment] = []

        while True:
            # Tries to match the break pattern
            break_matchobj = break_re.match(self.input_text, next_pos)
            if break_matchobj is None:
                self._cannot_match_closed_pattern(
                    next_pos,
                    opened_pattern, closed_pattern,
                )

            # Append non-empty text node to children list
            text_node = Text.from_matchobj(break_matchobj, 'inner')
            if text_node.inner:
                children.append(text_node)
            next_pos = break_matchobj.end()

            # Dispatch parsing between the @-command switch
            # and the closed (i.e. right) pattern
            break_char = break_matchobj.group('break')
            if break_char == '@':
                next_pos, result_node = self._parse_command(next_pos=next_pos)
                children.append(result_node)
            else:
                return next_pos, FragmentList(children=children)

    def _parse_command(self, next_pos: int) -> Tuple[int, Fragment]:
        """
        Attempts to parse all kinds of Paxter expressions
        by looking ahead for desired patterns.
        """
        matchobj = LEXER.id_prefix_re.match(self.input_text, next_pos)
        if matchobj:
            return self._parse_command_after_id(matchobj)

        matchobj = LEXER.brace_prefix_re.match(self.input_text, next_pos)
        if matchobj:
            return self._parse_rec_inner(matchobj)

        matchobj = LEXER.quote_prefix_re.match(self.input_text, next_pos)
        if matchobj:
            return self._parse_text(matchobj)

        matchobj = LEXER.bar_prefix_re.match(self.input_text, next_pos)
        if matchobj:
            return self._parse_normal_phrase(matchobj)

        matchobj = LEXER.symbol_re.match(self.input_text, next_pos)
        if matchobj:
            return self._parse_symbol_phrase(matchobj)

        raise PaxterSyntaxError(
            "invalid expression after @-command switch at {pos}",
            positions={'pos': next_pos},
        )

    def _parse_command_after_id(
            self, id_prefix_matchobj: Match[str],
    ) -> Tuple[int, Union[PaxterApply, PaxterPhrase]]:
        """
        Continues parsing the command after the identifier section.
        The result of this function could either be `PaxterApply`
        (if the options section or the main argument section exists)
        or `PaxterPhrase` (otherwise).
        """
        next_pos = id_prefix_matchobj.end()

        # Parse for options section (square brackets)
        bracket_prefix_matchobj = LEXER.bracket_prefix_re.match(
            self.input_text, next_pos,
        )
        if bracket_prefix_matchobj:
            next_pos = bracket_prefix_matchobj.end()
            next_pos, options = self._parse_options(next_pos)
        else:
            options = None

        # Parse for main arguments
        brace_prefix_matchobj = LEXER.brace_prefix_re.match(self.input_text, next_pos)
        if brace_prefix_matchobj:
            next_pos, main_arg_node = self._parse_rec_inner(brace_prefix_matchobj)
        else:
            quote_prefix_matchobj = LEXER.quote_prefix_re.match(
                self.input_text, next_pos,
            )
            if quote_prefix_matchobj:
                next_pos, main_arg_node = self._parse_text(quote_prefix_matchobj)
            else:
                main_arg_node = None

        # Create PaxterPhrase node as a special case
        if options is None and main_arg_node is None:
            result_node = PaxterPhrase.from_matchobj(id_prefix_matchobj, 'id')

        # Create PaxterApply node
        else:
            id_node = Identifier.from_matchobj(id_prefix_matchobj, 'id')
            result_node = PaxterApply(
                id=id_node, options=options, main_arg=main_arg_node,
            )

        return next_pos, result_node

    def _parse_text(
            self, quote_prefix_matchobj: Match[str],
    ) -> Tuple[int, Text]:
        """
        Continues parsing the command for `Text`
        following the pattern `@"..."`.
        """
        inner_matchobj = self._parse_non_rec_inner(quote_prefix_matchobj)
        text_node = Text.from_matchobj(inner_matchobj, 'inner')
        return inner_matchobj.end(), text_node

    def _parse_normal_phrase(
            self, bar_prefix_matchobj: Match[str],
    ) -> Tuple[int, PaxterPhrase]:
        """
        Continues parsing the command for `PaxterPhrase`
        following the pattern `@|...|`.
        """
        inner_matchobj = self._parse_non_rec_inner(bar_prefix_matchobj)
        phrase_node = PaxterPhrase.from_matchobj(inner_matchobj, 'inner')
        return inner_matchobj.end(), phrase_node

    def _parse_symbol_phrase(  # noqa
            self, symbol_matchobj: Match[str],
    ) -> Tuple[int, PaxterPhrase]:
        """
        Continues parsing the command for `PaxterPhrase`
        following the pattern `@_` where `_` is a single-character symbol.
        """
        phrase_node = PaxterPhrase.from_matchobj(symbol_matchobj, 'symbol')
        return symbol_matchobj.end(), phrase_node

    def _parse_rec_inner(self, opened_matchobj: Match[str]) -> Tuple[int, FragmentList]:
        """
        Recursively parses the input text until the closed (i.e. right)
        pattern corresponding to the opened (i.e. left) pattern
        captured by the provided match object is discovered.
        """
        opened_pattern = opened_matchobj.group('opened')
        closed_pattern = LEXER.flip_pattern(opened_pattern)
        break_re = LEXER.rec_break_re(closed_pattern)
        next_pos = opened_matchobj.end()

        return self._parse_inner_fragments(
            next_pos=next_pos,
            opened_pattern=opened_pattern, closed_pattern=closed_pattern,
            break_re=break_re,
        )

    def _parse_non_rec_inner(self, opened_matchobj: Match[str]) -> Match[str]:
        """
        Non-recursively parses the input text until the closed (i.e. right)
        pattern corresponding to the opened (i.e. left) pattern
        captured by the provided match object is discovered.
        """
        opened_pattern = opened_matchobj.group('opened')
        closed_pattern = LEXER.flip_pattern(opened_pattern)
        break_re = LEXER.non_rec_break_re(closed_pattern)
        next_pos = opened_matchobj.end()

        inner_matchobj = break_re.match(self.input_text, next_pos)
        if inner_matchobj is None:
            self._cannot_match_closed_pattern(next_pos, opened_pattern, closed_pattern)
        return inner_matchobj

    def _parse_options(self, next_pos: int) -> Tuple[int, TokenList]:
        """
        Parses the options section until reaching the closed square brackets.
        """
        return self._parse_options_rec(next_pos, '[')

    def _parse_options_rec(
            self, next_pos: int,
            opened_char: str,
    ) -> Tuple[int, TokenList]:
        """
        Recursively parses the options section
        until reaching the given breaking character.
        """
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
                next_pos, command_node = self._parse_command(next_pos)
                children.append(command_node)
                continue

            # Attempts to parse a list of tokens in sub-level
            if char in '([{':
                next_pos, token_list_node = self._parse_options_rec(next_pos, char)
                children.append(token_list_node)
                continue

            # Asserts that the character matches the expected closed character.
            # Return the token list if this is the case.
            if char in ')]}' and char == expected_closed_char:
                return next_pos, TokenList(children=children)

            # Else, something was wrong at the parsing,
            # perhaps reaching the end of text or found unmatched parenthesis.
            self._cannot_match_closed_pattern(
                pos=next_pos,
                opened_pattern=opened_char, closed_pattern=expected_closed_char,
            )

    @staticmethod
    def _cannot_match_closed_pattern(
            pos: int,
            opened_pattern: str, closed_pattern: str,
    ):
        opened_pattern = opened_pattern.replace('{', '{{')
        closed_pattern = closed_pattern.replace('}', '}}')
        raise PaxterSyntaxError(
            f"cannot match closed pattern {closed_pattern!r} "
            f"to the opened pattern {opened_pattern!r} "
            "at {pos}",
            positions={'pos': pos},
        )
