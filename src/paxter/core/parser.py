"""
Recursive descent parser of Paxter language.
"""
from dataclasses import dataclass, field
from typing import List, Match, Tuple

from paxter.core.charloc import CharLoc
from paxter.core.data import (
    Command, Fragment, FragmentList, Identifier, Number, Operator, ShortSymbol, Text,
    TokenList,
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
                self._cannot_match_enclosing(start_pos, enclosing)

            # Append non-empty text node to children list
            text_node = Text.from_matchobj(
                break_matchobj, 'inner', enclosing=EnclosingPattern(left=''),
            )
            if text_node.inner:
                children.append(text_node)

            # Dispatch parsing between the @-expression switch
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
        Parses @-expressions starting from immediately after @-symbol
        by attempting to dispatch the next step through lookahead patterns.
        """
        matchobj = LEXER.id_re.match(self.input_text, next_pos)
        if matchobj:
            return self._parse_cmd_with_id_starter(matchobj)

        matchobj = LEXER.lbar_re.match(self.input_text, next_pos)
        if matchobj:
            return self._parse_cmd_with_bar_starter(matchobj)

        matchobj = LEXER.symbol_re.match(self.input_text, next_pos)
        if matchobj:
            return self._parse_short_symbol(matchobj)

        self._invalid_cmd(next_pos)

    def _parse_cmd_with_id_starter(
            self, id_matchobj: Match[str],
    ) -> Tuple[int, Command]:
        """
        Continues parsing the starter section of the Command
        by using the identifier name content as the starter section.
        """
        cmd_start_pos, next_pos = id_matchobj.span()
        starter = id_matchobj.group('id')
        starter_enclosing = EnclosingPattern(left='')
        return self._parse_cmd_after_starter(
            next_pos, cmd_start_pos, starter, starter_enclosing,
        )

    def _parse_cmd_with_bar_starter(
            self, lbar_matchobj: Match[str],
    ) -> Tuple[int, Command]:
        """
        Continues parsing the starter section of the Command
        which is enclosed by the bar pattern.
        """
        cmd_start_pos, next_pos = lbar_matchobj.span()
        starter_enclosing = EnclosingPattern(left=lbar_matchobj.group('left'))

        inner_matchobj = starter_enclosing.non_rec_break_re.match(
            self.input_text, next_pos,
        )
        if inner_matchobj is None:
            self._cannot_match_enclosing(next_pos, starter_enclosing)

        next_pos = inner_matchobj.end()
        starter = inner_matchobj.group('inner')
        return self._parse_cmd_after_starter(
            next_pos, cmd_start_pos, starter, starter_enclosing,
        )

    def _parse_cmd_after_starter(
            self, next_pos: int, cmd_start_pos: int,
            starter: str, starter_enclosing: EnclosingPattern,
    ) -> Tuple[int, Command]:
        """
        Continues parsing the Command after the starter section.
        """
        # Parses for option section (square brackets)
        lbracket_matchobj = LEXER.lbracket_re.match(self.input_text, next_pos)
        if lbracket_matchobj:
            next_pos = lbracket_matchobj.end()
            next_pos, options = self._parse_option(next_pos)
        else:
            options = None

        # Parses for main argument
        lbrace_matchobj = LEXER.lbrace_re.match(self.input_text, next_pos)
        if lbrace_matchobj:
            next_pos, main_arg_node = self._parse_fragment_list(lbrace_matchobj)
        else:
            lquote_matchobj = LEXER.lquote_re.match(self.input_text, next_pos)
            if lquote_matchobj:
                next_pos, main_arg_node = self._parse_text(lquote_matchobj)
            else:
                main_arg_node = None

        # Construct Command node
        cmd_node = Command(
            cmd_start_pos, next_pos, starter, starter_enclosing,
            options, main_arg_node,
        )
        return next_pos, cmd_node

    def _parse_fragment_list(
            self, lbrace_matchobj: Match[str],
    ) -> Tuple[int, FragmentList]:
        """
        Recursively parses the input until the enclosing right pattern
        corresponding to the enclosing left pattern
        (captured by the provided match object) is discovered.
        """
        next_pos = lbrace_matchobj.end()
        enclosing = EnclosingPattern(left=lbrace_matchobj.group('left'))
        return self._inner_parse_fragment_list(next_pos, enclosing)

    def _parse_text(self, lquote_matchobj: Match[str]) -> Tuple[int, Text]:
        """
        Continues parsing the input for raw :class:`Text` node
        until the enclosing right pattern corresponding to the
        enclosing left pattern (captured by the provided match object)
        is discovered.
        """
        next_pos = lquote_matchobj.end()
        enclosing = EnclosingPattern(left=lquote_matchobj.group('left'))

        inner_matchobj = enclosing.non_rec_break_re.match(self.input_text, next_pos)
        if inner_matchobj is None:
            self._cannot_match_enclosing(next_pos, enclosing)

        next_pos = inner_matchobj.end()
        text_node = Text.from_matchobj(inner_matchobj, 'inner', enclosing)
        return next_pos, text_node

    def _parse_short_symbol(
            self, symbol_matchobj: Match[str],
    ) -> Tuple[int, ShortSymbol]:
        """
        A special case of @-expression (called a "short symbol")
        where a single-character symbol follows the @-switch character.
        """
        next_pos = symbol_matchobj.end()
        command_node = ShortSymbol.from_matchobj(symbol_matchobj, 'symbol')
        return next_pos, command_node

    def _parse_option(self, next_pos: int) -> Tuple[int, TokenList]:
        """
        Parses the option section until reaching the right square brackets.
        """
        start_pos = next_pos
        children = []

        while True:
            # Remove leading whitespaces
            ws_matchobj = LEXER.ws_re.match(self.input_text, next_pos)
            next_pos = ws_matchobj.end()

            # Attempts to extract identifier node
            id_matchobj = LEXER.id_re.match(self.input_text, next_pos)
            if id_matchobj:
                next_pos = id_matchobj.end()
                id_node = Identifier.from_matchobj(id_matchobj, 'id')
                children.append(id_node)
                continue

            # Attempts to extract operator node
            op_matchobj = LEXER.op_re.match(self.input_text, next_pos)
            if op_matchobj:
                next_pos = op_matchobj.end()
                op_node = Operator.from_matchobj(op_matchobj, 'op')
                children.append(op_node)
                continue

            # Attempts to extract number literal node
            num_matchobj = LEXER.num_re.match(self.input_text, next_pos)
            if num_matchobj:
                next_pos = num_matchobj.end()
                num_node = Number.from_matchobj(num_matchobj, 'num')
                children.append(num_node)
                continue

            # Attempts to extract fragment list node
            lbrace_matchobj = LEXER.lbrace_re.match(self.input_text, next_pos)
            if lbrace_matchobj:
                next_pos, fragment_list_node = (
                    self._parse_fragment_list(lbrace_matchobj)
                )
                children.append(fragment_list_node)
                continue

            # Attempts to extract text node
            lquote_matchobj = LEXER.lquote_re.match(self.input_text, next_pos)
            if lquote_matchobj:
                next_pos, text_node = self._parse_text(lquote_matchobj)
                children.append(text_node)
                continue

            # Attempts to extract @-expressions
            at_matchobj = LEXER.at_re.match(self.input_text, next_pos)
            if at_matchobj:
                next_pos = at_matchobj.end()
                next_pos, at_expr_node = self._parse_at_expr(next_pos)
                children.append(at_expr_node)
                continue

            # Attempts to parse a sub-level list of tokens
            lbracket_matchobj = LEXER.lbracket_re.match(self.input_text, next_pos)
            if lbracket_matchobj:
                next_pos = lbracket_matchobj.end()
                next_pos, token_list_node = self._parse_option(next_pos)
                children.append(token_list_node)
                continue

            # Attempts to parse the end of token list
            # Return the token list if this is the case
            rbracket_matchobj = LEXER.rbracket_re.match(self.input_text, next_pos)
            if rbracket_matchobj:
                end_pos, next_pos = rbracket_matchobj.span()
                return next_pos, TokenList(start_pos, end_pos, children)

            # Else, something was wrong at the parsing,
            # perhaps reaching the end of text or found unmatched parenthesis.
            self._cannot_match_char(start_pos, '[', ']')

    def _cannot_match_enclosing(self, pos: int, enclosing: EnclosingPattern):
        """
        Raises syntax error for failing to match enclosing right pattern
        to the corresponding enclosing left pattern.
        """
        raise PaxterSyntaxError(
            f"cannot match enclosing right pattern {enclosing.right!r} "
            f"to the left pattern {enclosing.left!r} at %(pos)s",
            pos=CharLoc(self.input_text, pos - len(enclosing.left)),
        )

    def _cannot_match_char(self, pos: int, left_char: str, right_char: str):
        """
        Raises syntax error for failing to match enclosing right char
        to the corresponding enclosing left char.
        """
        raise PaxterSyntaxError(
            f"cannot match enclosing right character {right_char!r} "
            f"to the left character {left_char!r} at %(pos)s",
            pos=CharLoc(self.input_text, pos - len(left_char)),
        )

    def _invalid_cmd(self, pos: int):
        """
        Raises syntax error for failing to parse @-command.
        """
        raise PaxterSyntaxError(
            "invalid expression after @-command at %(pos)s",
            pos=CharLoc(self.input_text, pos),
        )
