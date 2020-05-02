"""
Implementation of the renderer.
"""
import re
from dataclasses import dataclass
from typing import Any, List, Union

from paxter.core import (
    Fragment, FragmentList, Identifier, Number, Operator,
    PaxterApply, PaxterPhrase, Text, Token, TokenList,
)
from paxter.core.exceptions import PaxterRenderError
from paxter.core.line_col import LineCol
from paxter.renderers.python import flatten
from paxter.renderers.python.wrappers import BaseApply, NormalApply

BACKSLASH_NEWLINE_RE = re.compile(r'\\\n')


@dataclass
class RenderContext:
    """
    A suite of Paxter document tree renderer.
    """
    input_text: str
    env: dict

    def visit(self, seq: FragmentList) -> str:
        return flatten(self.visit_fragment_list(seq))

    def visit_token(self, token: Token) -> Any:
        if isinstance(token, Fragment):
            return self.visit_fragment(token)
        if isinstance(token, TokenList):
            return self.visit_token_list(token)
        if isinstance(token, Identifier):
            return self.visit_identifier(token)
        if isinstance(token, Operator):
            return self.visit_operator(token)
        if isinstance(token, Number):
            return self.visit_number(token)
        raise PaxterRenderError(
            "unrecognized token at %(pos)s",
            pos=LineCol(self.input_text, token.start_pos),
        )

    def visit_fragment(self, fragment: Fragment) -> Any:
        if isinstance(fragment, FragmentList):
            return self.visit_fragment_list(fragment)
        if isinstance(fragment, Text):
            return self.visit_text(fragment)
        if isinstance(fragment, PaxterPhrase):
            return self.visit_paxter_phrase(fragment)
        if isinstance(fragment, PaxterApply):
            return self.visit_paxter_apply(fragment)
        raise PaxterRenderError(
            "unrecognized fragment at %(pos)s",
            pos=LineCol(self.input_text, fragment.start_pos),
        )

    def visit_token_list(self, seq: TokenList):
        raise PaxterRenderError(
            "token list not expected at %(pos)s",
            pos=LineCol(self.input_text, seq.start_pos),
        )

    def visit_identifier(self, token: Identifier):
        raise PaxterRenderError(
            "identifier not expected at %(pos)",
            pos=LineCol(self.input_text, token.start_pos),
        )

    def visit_operator(self, token: Operator):
        raise PaxterRenderError(
            "operator not expected at %(pos)",
            pos=LineCol(self.input_text, token.start_pos),
        )

    def visit_number(self, token: Number) -> Union[int, float]:
        return token.value

    def visit_fragment_list(self, seq: FragmentList) -> List[Any]:
        return [
            self.visit_fragment(fragment)
            for fragment in seq.children
        ]

    def visit_text(self, token: Text) -> str:
        text = token.inner
        if not token.scope_pattern.opened:
            text = BACKSLASH_NEWLINE_RE.sub('', text)
        return text

    def visit_paxter_phrase(self, token: PaxterPhrase) -> Any:
        # Fetch the phrase evaluation function from within the environment
        try:
            phrase_eval = self.env['_phrase_eval_']
        except KeyError as exc:
            raise PaxterRenderError(
                "expected '_phrase_eval_' to be defined at %(pos)s",
                pos=LineCol(self.input_text, token.start_pos),
            ) from exc

        # Evaluate the expression embedded within the phrase
        try:
            return phrase_eval(token.inner, self.env)
        except PaxterRenderError:
            raise
        except Exception as exc:
            raise PaxterRenderError(
                f"paxter phrase evaluation error at %(pos)s",
                pos=LineCol(self.input_text, token.start_pos),
            ) from exc

    def visit_paxter_apply(self, token: PaxterApply):
        # Fetch the function from within the environment
        try:
            func = self.env[token.id.name]
        except KeyError as exc:
            raise PaxterRenderError(
                f"unknown paxter application with id {token.id.name!r} at %(pos)s",
                pos=LineCol(self.input_text, token.start_pos),
            ) from exc

        # Wrap the function if not yet wrapped
        if not isinstance(func, BaseApply):
            func = NormalApply(func)

        # Make the call to the wrapped function
        try:
            return func.call(self, token)
        except PaxterRenderError:
            raise
        except Exception as exc:
            raise PaxterRenderError(
                f"paxter apply evaluation error at %(pos)s",
                pos=LineCol(self.input_text, token.start_pos),
            ) from exc
