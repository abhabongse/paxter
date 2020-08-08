"""
Implementation of the renderer.
"""
import re
from dataclasses import dataclass, field
from typing import Any, Union

from paxter.evaluator.data import Fragments
from paxter.evaluator.wrappers import BaseApply, NormalApply
from paxter.exceptions import PaxterRenderError
from paxter.parser import (
    CharLoc, Command, Fragment, FragmentSeq, Identifier, Number,
    Operator, SingleSymbol, Text, Token, TokenSeq,
)


@dataclass
class EvaluateContext:
    """
    Base rendering class for Paxter parsed document tree.

    Users of this renderer may embed and run pyauthor code
    directly from within the Paxter document source file.
    """
    #: Document source text
    input_text: str

    #: Python execution environment data
    env: dict

    #: Parsed document tree
    tree: FragmentSeq

    #: Result of the rendering
    rendered: Union[str, list] = field(init=False)

    BACKSLASH_NEWLINE_RE = re.compile(r'\\[ \t\r\f\v]*\n[ \t\r\f\v]*')
    FALLBACK_SYMBOLS = {'!': '', '@': '@'}

    def __post_init__(self):
        self.rendered = self.render()

    def render(self):
        return self.transform_fragment_list(self.tree)

    def transform_token(self, token: Token) -> Any:
        """
        Transforms a given parsed token.
        """
        if isinstance(token, Fragment):
            return self.transform_fragment(token)
        if isinstance(token, TokenSeq):
            return self.transform_token_list(token)
        if isinstance(token, Identifier):
            return self.transform_identifier(token)
        if isinstance(token, Operator):
            return self.transform_operator(token)
        if isinstance(token, Number):
            return self.transform_number(token)
        if isinstance(token, FragmentSeq):
            return self.transform_fragment_list(token)
        raise PaxterRenderError(
            "unrecognized token at %(pos)s",
            pos=CharLoc(self.input_text, token.start_pos),
        )

    def transform_fragment(self, fragment: Fragment) -> Any:
        """
        Transforms a given parsed fragment.
        """
        if isinstance(fragment, Text):
            return self.transform_text(fragment)
        if isinstance(fragment, Command):
            return self.transform_command(fragment)
        if isinstance(fragment, SingleSymbol):
            return self.transform_symbol_command(fragment)
        raise PaxterRenderError(
            "unrecognized fragment at %(pos)s",
            pos=CharLoc(self.input_text, fragment.start_pos),
        )

    def transform_token_list(self, seq: TokenSeq):
        """
        Transforms a given parsed token list.
        """
        raise PaxterRenderError(
            "token list not expected at %(pos)s",
            pos=CharLoc(self.input_text, seq.start_pos),
        )

    def transform_identifier(self, token: Identifier):
        """
        Transforms a given parsed identifier.
        """
        raise PaxterRenderError(
            "identifier not expected at %(pos)",
            pos=CharLoc(self.input_text, token.start_pos),
        )

    def transform_operator(self, token: Operator):
        """
        Transforms a given parsed operator.
        """
        raise PaxterRenderError(
            "operator not expected at %(pos)",
            pos=CharLoc(self.input_text, token.start_pos),
        )

    def transform_number(self, token: Number) -> Union[int, float]:
        """
        Transforms a given parsed number.
        """
        return token.value

    def transform_fragment_list(self, seq: FragmentSeq) -> Fragments:
        """
        Transforms a given parsed fragment list.
        """
        transformed_fragments = (
            self.transform_fragment(fragment)
            for fragment in seq.children
        )
        result = [
            fragment for fragment in transformed_fragments
            if fragment is not None
        ]
        return Fragments(result)

    def transform_text(self, token: Text) -> str:
        """
        Transforms a given parsed text fragment.
        """
        text = token.inner
        if not token.enclosing.left:
            text = self.BACKSLASH_NEWLINE_RE.sub('', text)
        return text

    def transform_command(self, token: Command) -> Any:
        """
        Transforms a given parsed command.
        """
        # Try to evaluate the starter section
        # using the evaluator function from _starter_eval_
        try:
            starter_eval = self.env['_starter_eval_']
        except KeyError as exc:
            raise PaxterRenderError(
                "expected '_starter_eval_' to be defined at %(pos)s",
                pos=CharLoc(self.input_text, token.start_pos),
            ) from exc
        try:
            starter_value = starter_eval(token.starter, self.env)
        except PaxterRenderError:
            raise
        except Exception as exc:
            raise PaxterRenderError(
                "paxter command starter evaluation error at %(pos)s: "
                f"{token.starter!r}",
                pos=CharLoc(self.input_text, token.start_pos),
            ) from exc

        # Bail out if option section and main arg section are empty
        if token.option is None and token.main_arg is None:
            return starter_value

        # Wrap the function if not yet wrapped
        if not isinstance(starter_value, BaseApply):
            starter_value = NormalApply(starter_value)

        # Make the call to the wrapped function
        try:
            return starter_value.call(self, token)
        except PaxterRenderError:
            raise
        except Exception as exc:
            raise PaxterRenderError(
                "paxter apply evaluation error at %(pos)s",
                pos=CharLoc(self.input_text, token.start_pos),
            ) from exc

    def transform_symbol_command(self, token: SingleSymbol) -> Any:
        """
        Transforms a given parsed symbol command.
        """
        # Lookup _symbols_ for the desired symbol
        try:
            symbols = self.env['_symbols_']
        except KeyError as exc:
            if token.symbol in self.FALLBACK_SYMBOLS:
                return self.FALLBACK_SYMBOLS[token.symbol]
            raise PaxterRenderError(
                "expected '_symbols_' to be defined at %(pos)s",
                pos=CharLoc(self.input_text, token.start_pos),
            ) from exc
        try:
            return symbols[token.symbol]
        except KeyError as exc:
            if token.symbol in self.FALLBACK_SYMBOLS:
                return self.FALLBACK_SYMBOLS[token.symbol]
            raise PaxterRenderError(
                f"undefined symbol {token.symbol} within '_symbol_' at %(pos)s",
                pos=CharLoc(self.input_text, token.start_pos),
            ) from exc
        except Exception as exc:
            raise RuntimeError("unexpected error from within library") from exc
