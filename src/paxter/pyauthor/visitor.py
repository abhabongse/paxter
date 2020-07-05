"""
Implementation of the renderer.
"""
import re
from dataclasses import dataclass, field
from typing import Any, List, Union

from paxter.core import (
    CharLoc, Command, Fragment, FragmentList, Identifier, Number,
    Operator, SymbolCommand, Text, Token, TokenList,
)
from paxter.core.exceptions import PaxterRenderError
from paxter.pyauthor.funcs import flatten
from paxter.pyauthor.wrappers import BaseApply, NormalApply

BACKSLASH_NEWLINE_RE = re.compile(r'\\\n')


@dataclass
class RenderContext:
    """
    A suite of Paxter document tree renderer.

    Users of this renderer may embed and run pyauthor code
    directly from within the Paxter document source file.
    """
    #: Document source text
    input_text: str

    #: Python execution environment data
    env: dict

    #: Parsed document tree
    tree: FragmentList

    #: Whether the list should always be joined into string
    #: whenever possible
    is_joined: bool = True

    #: Result of the rendering
    rendered: Union[str, list] = field(init=False)

    def __post_init__(self):
        self.rendered = self.transform_fragment_list(self.tree)
        if self.is_joined:
            self.rendered = flatten(self.rendered, is_joined=True)

    def transform_token(self, token: Token) -> Any:
        if isinstance(token, Fragment):
            return self.transform_fragment(token)
        if isinstance(token, TokenList):
            return self.transform_token_list(token)
        if isinstance(token, Identifier):
            return self.transform_identifier(token)
        if isinstance(token, Operator):
            return self.transform_operator(token)
        if isinstance(token, Number):
            return self.transform_number(token)
        if isinstance(token, FragmentList):
            return self.transform_fragment_list(token)
        raise PaxterRenderError(
            "unrecognized token at %(pos)s",
            pos=CharLoc(self.input_text, token.start_pos),
        )

    def transform_fragment(self, fragment: Fragment) -> Any:
        if isinstance(fragment, Text):
            return self.transform_text(fragment)
        if isinstance(fragment, Command):
            return self.transform_command(fragment)
        if isinstance(fragment, SymbolCommand):
            return self.transform_symbol_command(fragment)
        raise PaxterRenderError(
            "unrecognized fragment at %(pos)s",
            pos=CharLoc(self.input_text, fragment.start_pos),
        )

    def transform_token_list(self, seq: TokenList):
        raise PaxterRenderError(
            "token list not expected at %(pos)s",
            pos=CharLoc(self.input_text, seq.start_pos),
        )

    def transform_identifier(self, token: Identifier):
        raise PaxterRenderError(
            "identifier not expected at %(pos)",
            pos=CharLoc(self.input_text, token.start_pos),
        )

    def transform_operator(self, token: Operator):
        raise PaxterRenderError(
            "operator not expected at %(pos)",
            pos=CharLoc(self.input_text, token.start_pos),
        )

    def transform_number(self, token: Number) -> Union[int, float]:
        return token.value

    def transform_fragment_list(self, seq: FragmentList) -> List[Any]:
        transformed_fragments = (
            self.transform_fragment(fragment)
            for fragment in seq.children
        )
        result = [
            fragment for fragment in transformed_fragments
            if fragment is not None
        ]
        if self.is_joined:
            result = ''.join(str(fragment) for fragment in result)
        return result

    def transform_text(self, token: Text) -> str:
        text = token.inner
        if not token.enclosing.left:
            text = BACKSLASH_NEWLINE_RE.sub('', text)
        return text

    def transform_command(self, token: Command):
        # Try to evaluate the intro section
        # using the evaluator function from _intro_eval_
        try:
            intro_eval = self.env['_intro_eval_']
        except KeyError as exc:
            raise PaxterRenderError(
                "expected '_intro_eval_' to be defined at %(pos)s",
                pos=CharLoc(self.input_text, token.start_pos),
            ) from exc
        try:
            intro_value = intro_eval(token.intro, self.env)
        except PaxterRenderError:
            raise
        except Exception as exc:
            raise PaxterRenderError(
                "paxter command intro evaluation error at %(pos)s: "
                f"{token.intro!r}",
                pos=CharLoc(self.input_text, token.start_pos),
            ) from exc

        # Bail out if option section and main arg section are empty
        if token.options is None and token.main_arg is None:
            return intro_value

        # Wrap the function if not yet wrapped
        if not isinstance(intro_value, BaseApply):
            intro_value = NormalApply(intro_value)

        # Make the call to the wrapped function
        try:
            return intro_value.call(self, token)
        except PaxterRenderError:
            raise
        except Exception as exc:
            raise PaxterRenderError(
                "paxter apply evaluation error at %(pos)s",
                pos=CharLoc(self.input_text, token.start_pos),
            ) from exc

    def transform_symbol_command(self, token: SymbolCommand):
        # Lookup _symbols_ for the desired symbol
        try:
            symbols = self.env['_symbols_']
        except KeyError as exc:
            raise PaxterRenderError(
                "expected '_symbols_' to be defined at %(pos)s",
                pos=CharLoc(self.input_text, token.start_pos),
            ) from exc
        try:
            return symbols[token.symbol]
        except KeyError as exc:
            raise PaxterRenderError(
                f"undefined symbol {token.symbol} within '_symbol_' at %(pos)s",
                pos=CharLoc(self.input_text, token.start_pos),
            ) from exc
        except Exception as exc:
            raise RuntimeError("unexpected error from within library") from exc
