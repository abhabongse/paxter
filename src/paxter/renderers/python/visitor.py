"""
Implementation of the renderer.
"""
from dataclasses import dataclass
from typing import Any, List, Union

from paxter.core import (
    Fragment, FragmentList, Identifier, Number, Operator,
    PaxterApply, PaxterPhrase, Text, Token, TokenList,
)
from paxter.core.exceptions import PaxterRenderError
from paxter.renderers.python.wrappers import BaseApply, NormalApply


@dataclass
class RenderContext:
    """
    A suite of Paxter document tree renderer.
    """
    input_text: str
    env: dict

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
        raise PaxterRenderError("unrecognized token")

    def visit_fragment(self, fragment: Fragment) -> Any:
        if isinstance(fragment, FragmentList):
            return self.visit_fragment_list(fragment)
        if isinstance(fragment, Text):
            return self.visit_text(fragment)
        if isinstance(fragment, PaxterPhrase):
            return self.visit_paxter_phrase(fragment)
        if isinstance(fragment, PaxterApply):
            return self.visit_paxter_apply(fragment)
        raise PaxterRenderError("unrecognized fragment")

    def visit_token_list(self, seq: TokenList):
        raise PaxterRenderError("not expected to be directly visited")

    def visit_identifier(self, token: Identifier):
        raise PaxterRenderError("not expected to be directly visited")

    def visit_operator(self, token: Operator):
        raise PaxterRenderError("not expected to be directly visited")

    def visit_number(self, token: Number) -> Union[int, float]:
        return token.number

    def visit_fragment_list(self, seq: FragmentList) -> List[Any]:
        return [
            self.visit_fragment(fragment)
            for fragment in seq.children
        ]

    def visit_text(self, token: Text) -> str:
        return token.inner

    def visit_paxter_phrase(self, token: PaxterPhrase) -> Any:
        # If the phrase exists in the pre-defined symbols mapping
        # then returns the mapped value.
        try:
            phrase_eval = self.env['_phrase_eval_']
        except KeyError as exc:
            raise PaxterRenderError("expected _phrase_eval_ to be defined") from exc

        # Evaluate the expression embedded within the phrase
        try:
            return phrase_eval(token.inner, self.env)
        except PaxterRenderError:
            raise
        except Exception as exc:
            line, col = PaxterRenderError.pos_to_line_col(
                self.input_text, token.pos.start,
            )
            raise PaxterRenderError(
                f"paxter phrase evaluation error at line {line} col {col}",
            ) from exc

    def visit_paxter_apply(self, token: PaxterApply):
        # Look up the function from within the environment
        # then make the call for that function.
        try:
            func = self.env[token.id.name]
        except KeyError as exc:
            line, col = PaxterRenderError.pos_to_line_col(
                self.input_text, token.id.pos.start,
            )
            raise PaxterRenderError(
                f"unknown paxter application with id {token.id.name!r} "
                f"at line {line} col {col}",
            ) from exc
        if not isinstance(func, BaseApply):
            func = NormalApply(func)

        try:
            return func.call(self, token)
        except PaxterRenderError:
            raise
        except Exception as exc:
            line, col = PaxterRenderError.pos_to_line_col(
                self.input_text, token.id.pos.start,
            )
            raise PaxterRenderError(
                f"paxter apply evaluation error at line {line} col {col}"
            ) from exc
