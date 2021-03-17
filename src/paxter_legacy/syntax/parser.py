"""
Recursive descent syntax of Paxter language.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Match

from paxter.exceptions import PaxterSyntaxError
from paxter.syntax.charloc import CharLoc
from paxter.syntax.enclosing import EnclosingPattern, GlobalEnclosingPattern
from paxter.syntax.lexers import _LEXER
from paxter.syntax.nodetypes import (
    Command, Fragment, FragmentSeq, Identifier, Number, Operator, Text, TokenSeq,
)


@dataclass
class Parser:
    """
    Implements a recursive descent syntax for Paxter language text input.

    To use this class, initialize an instance with the source text
    then call the instance method :meth:`parse() <ParsingTask.parse>`
    to obtain the parsed tree::

        parsed_tree = ParsingTask(src_text).parse()
    """
    #: Document source text
    src_text: str

    def run(self) -> FragmentSeq:
        """
        Parses source text written in Paxter language into the parsed tree
        which is a node of type :class:`paxter_legacy.syntax.FragmentSeq`.

        This instance method is computationally expensive;
        please avoid repeatedly calling this method.
        """
        return self._parse_global_fragment_seq()

    def _parse_global_fragment_seq(self) -> FragmentSeq:
        """
        Parses the entirety of the already provided input text
        for the global-level fragment sequence from the very beginning.
        """
        end_pos, node = self._parse_inner_fragment_seq(0, GlobalEnclosingPattern())
        if end_pos != len(self.src_text):  # pragma: no cover
            raise RuntimeError("unexpected error; input text not fully consumed")
        return node

    def _parse_inner_fragment_seq(
            self,
            next_pos: int,
            enclosing: EnclosingPattern,
    ) -> tuple[int, FragmentSeq]:
        """
        Subroutinely parses the input expecting a sequence of fragment nodes
        starting from the given position indicated by ``next_pos``.
        This method is called when syntax the global-level input
        or when syntax under a scope enclosed by braces pattern.
        """
        start_pos = next_pos
        children: list[Fragment] = []

        while True:
            # Attempts to match the next break pattern
            matchobj = enclosing.rec_break_re.match(self.src_text, next_pos)
            if matchobj is None:
                self._raise_cannot_match_enclosing(start_pos, enclosing)

            # Append non-empty text node to children list
            text_node = Text.from_matchobj(matchobj, 'inner', enclosing=EnclosingPattern(left=''))
            if text_node.inner:
                children.append(text_node)

            # Dispatch syntax between the @-expression switch
            # and the closing (i.e. right) pattern
            next_pos = matchobj.end()
            break_char = matchobj['break']
            if break_char == '@':
                next_pos, result_node = self._parse_cmd(next_pos)
                children.append(result_node)
            else:
                break

        end_pos = matchobj.end('inner')
        fragment_seq_node = FragmentSeq(start_pos, end_pos, children, enclosing)
        return next_pos, fragment_seq_node

    def _parse_cmd(self, next_pos: int) -> tuple[int, Command]:
        """
        Parses @-expressions starting from immediately after @-symbol
        by attempting to dispatch the next step through lookahead patterns.
        """
        if matchobj := _LEXER.id_re.match(self.src_text, next_pos):
            return self._parse_id_phrase_cmd(matchobj)

        if matchobj := _LEXER.lbar_re.match(self.src_text, next_pos):
            return self._parse_bar_phrase_cmd(matchobj)

        if matchobj := _LEXER.symbol_re.match(self.src_text, next_pos):
            return self._parse_single_symbol(matchobj)

        self._raise_invalid_cmd(next_pos)

    def _parse_id_phrase_cmd(self, id_matchobj: Match[str]) -> tuple[int, Command]:
        """
        Continues syntax the phrase section of the Command
        by using the identifier name content as the phrase section.
        """
        cmd_start_pos, next_pos = id_matchobj.span()
        phrase = id_matchobj['id']
        phrase_enclosing = EnclosingPattern(left='')
        return self._parse_cmd_after_phrase(next_pos, cmd_start_pos, phrase, phrase_enclosing)

    def _parse_bar_phrase_cmd(self, lbar_matchobj: Match[str]) -> tuple[int, Command]:
        """
        Continues syntax the phrase section of the Command
        which is enclosed by the bar pattern.
        """
        cmd_start_pos, next_pos = lbar_matchobj.span()
        phrase_enclosing = EnclosingPattern(left=lbar_matchobj['left'])

        inner_matchobj = phrase_enclosing.non_rec_break_re.match(self.src_text, next_pos)
        if inner_matchobj is None:
            self._raise_cannot_match_enclosing(next_pos, phrase_enclosing)

        next_pos = inner_matchobj.end()
        phrase = inner_matchobj['inner']
        return self._parse_cmd_after_phrase(next_pos, cmd_start_pos, phrase, phrase_enclosing)

    def _parse_cmd_after_phrase(
            self,
            next_pos: int,
            cmd_start_pos: int,
            phrase: str,
            phrase_enclosing: EnclosingPattern,
    ) -> tuple[int, Command]:
        """
        Continues syntax the Command after the phrase section.
        """
        # If phrase is empty, stop syntax for options or main argument
        if not phrase:
            options = None
            main_arg = None
        else:
            # Parses for options section (square brackets)
            if lbracket_matchobj := _LEXER.lbracket_re.match(self.src_text, next_pos):
                next_pos = lbracket_matchobj.end()
                next_pos, options = self._parse_options(next_pos)
            else:
                options = None

            # Parses for main argument
            if lbrace_matchobj := _LEXER.lbrace_re.match(self.src_text, next_pos):
                next_pos, main_arg = self._parse_fragment_seq(lbrace_matchobj)
            elif lquote_matchobj := _LEXER.lquote_re.match(self.src_text, next_pos):
                next_pos, main_arg = self._parse_text(lquote_matchobj)
            else:
                main_arg = None

        # Construct Command node
        cmd_node = Command(cmd_start_pos, next_pos, phrase, phrase_enclosing, options, main_arg)
        return next_pos, cmd_node

    def _parse_fragment_seq(self, lbrace_matchobj: Match[str]) -> tuple[int, FragmentSeq]:
        """
        Recursively parses the input until the enclosing right pattern
        corresponding to the enclosing left pattern
        (captured by the provided match object) is discovered.
        """
        next_pos = lbrace_matchobj.end()
        enclosing = EnclosingPattern(left=lbrace_matchobj['left'])
        return self._parse_inner_fragment_seq(next_pos, enclosing)

    def _parse_text(self, lquote_matchobj: Match[str]) -> tuple[int, Text]:
        """
        Continues syntax the input for raw :class:`Text` node
        until the enclosing right pattern corresponding to the
        enclosing left pattern (captured by the provided match object)
        is discovered.
        """
        next_pos = lquote_matchobj.end()
        enclosing = EnclosingPattern(left=lquote_matchobj['left'])

        inner_matchobj = enclosing.non_rec_break_re.match(self.src_text, next_pos)
        if inner_matchobj is None:
            self._raise_cannot_match_enclosing(next_pos, enclosing)

        next_pos = inner_matchobj.end()
        text_node = Text.from_matchobj(inner_matchobj, 'inner', enclosing)
        return next_pos, text_node

    def _parse_single_symbol(self, symbol_matchobj: Match[str]) -> tuple[int, Command]:
        """
        A special case of @-expression (called a "single symbol")
        where a single-character symbol follows the @-switch character.
        """
        cmd_start_pos, next_pos = symbol_matchobj.span()
        phrase = symbol_matchobj['symbol']
        phrase_enclosing = EnclosingPattern(left='')
        command_node = Command(
            cmd_start_pos,
            next_pos,
            phrase,
            phrase_enclosing,
            options=None,
            main_arg=None,
        )
        return next_pos, command_node

    def _parse_options(self, next_pos: int) -> tuple[int, TokenSeq]:
        """
        Parses the options section until reaching the right square brackets.
        """
        start_pos = next_pos
        children = []

        while True:
            # Remove leading whitespaces
            ws_matchobj = _LEXER.ws_re.match(self.src_text, next_pos)
            next_pos = ws_matchobj.end()

            # Attempts to extract identifier node
            if id_matchobj := _LEXER.id_re.match(self.src_text, next_pos):
                next_pos = id_matchobj.end()
                id_node = Identifier.from_matchobj(id_matchobj, 'id')
                children.append(id_node)
                continue

            # Attempts to extract operator node
            if op_matchobj := _LEXER.op_re.match(self.src_text, next_pos):
                next_pos = op_matchobj.end()
                op_node = Operator.from_matchobj(op_matchobj, 'op')
                children.append(op_node)
                continue

            # Attempts to extract number literal node
            if num_matchobj := _LEXER.num_re.match(self.src_text, next_pos):
                next_pos = num_matchobj.end()
                num_node = Number.from_matchobj(num_matchobj, 'num')
                children.append(num_node)
                continue

            # Attempts to extract fragment sequence node
            if lbrace_matchobj := _LEXER.lbrace_re.match(self.src_text, next_pos):
                next_pos, fragment_seq_node = self._parse_fragment_seq(lbrace_matchobj)
                children.append(fragment_seq_node)
                continue

            # Attempts to extract text node
            if lquote_matchobj := _LEXER.lquote_re.match(self.src_text, next_pos):
                next_pos, text_node = self._parse_text(lquote_matchobj)
                children.append(text_node)
                continue

            # Attempts to extract @-expressions
            if at_matchobj := _LEXER.at_re.match(self.src_text, next_pos):
                next_pos = at_matchobj.end()
                next_pos, at_expr_node = self._parse_cmd(next_pos)
                children.append(at_expr_node)
                continue

            # Attempts to syntax a sub-level sequence of tokens
            if lbracket_matchobj := _LEXER.lbracket_re.match(self.src_text, next_pos):
                next_pos = lbracket_matchobj.end()
                next_pos, token_seq_node = self._parse_options(next_pos)
                children.append(token_seq_node)
                continue

            # Attempts to syntax the end of token sequence
            # Return the token sequence if this is the case
            if rbracket_matchobj := _LEXER.rbracket_re.match(self.src_text, next_pos):
                end_pos, next_pos = rbracket_matchobj.span()
                return next_pos, TokenSeq(start_pos, end_pos, children)

            # Else, something was wrong at the syntax,
            # perhaps reaching the end of text or found unmatched parenthesis.
            self._raise_cannot_match_char(start_pos, '[', ']')

    def _raise_cannot_match_enclosing(self, pos: int, enclosing: EnclosingPattern):
        """
        Raises syntax error for failing to match enclosing right pattern
        to the corresponding enclosing left pattern.
        """
        raise PaxterSyntaxError(
            f"cannot match enclosing right pattern {enclosing.right!r} "
            f"to the left pattern {enclosing.left!r} at %(pos)s",
            pos=CharLoc(self.src_text, pos - len(enclosing.left)),
        )

    def _raise_cannot_match_char(self, pos: int, left_char: str, right_char: str):
        """
        Raises syntax error for failing to match enclosing right char
        to the corresponding enclosing left char.
        """
        raise PaxterSyntaxError(
            f"cannot match enclosing right character {right_char!r} "
            f"to the left character {left_char!r} at %(pos)s",
            pos=CharLoc(self.src_text, pos - len(left_char)),
        )

    def _raise_invalid_cmd(self, pos: int):
        """
        Raises syntax error for failing to syntax @-command.
        """
        raise PaxterSyntaxError(
            "invalid expression after @-command at %(pos)s",
            pos=CharLoc(self.src_text, pos),
        )
