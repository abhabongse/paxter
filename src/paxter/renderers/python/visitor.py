"""
Implementation of the renderer.
"""
import re
from dataclasses import dataclass, field
from typing import Any, List, Union

from paxter.core import (
    CharLoc, Command, Fragment, FragmentList, Identifier, Number,
    Operator, Text, Token, TokenList,
)
from paxter.core.exceptions import PaxterRenderError
from paxter.renderers.python import flatten
from paxter.renderers.python.wrappers import BaseApply, NormalApply

BACKSLASH_NEWLINE_RE = re.compile(r'\\\n')


@dataclass
class RenderContext:
    """
    A suite of Paxter document tree renderer.

    Users of this renderer may embed and run python code
    directly from within the Paxter document source file.
    """
    #: Document source text
    input_text: str

    #: Python execution environment data
    env: dict

    #: Parsed document tree
    tree: FragmentList

    #: Result of the rendering
    rendered: str = field(init=False)

    def __post_init__(self):
        self.rendered = flatten(self.transform_fragment_list(self.tree))

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
        raise PaxterRenderError(
            "unrecognized token at %(pos)s",
            pos=CharLoc(self.input_text, token.start_pos),
        )

    def transform_fragment(self, fragment: Fragment) -> Any:
        if isinstance(fragment, FragmentList):
            return self.transform_fragment_list(fragment)
        if isinstance(fragment, Text):
            return self.transform_text(fragment)
        if isinstance(fragment, Command):
            return self.transform_paxter_apply(fragment)
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
        return [
            self.transform_fragment(fragment)
            for fragment in seq.children
        ]

    def transform_text(self, token: Text) -> str:
        text = token.inner
        if not token.enclosing.left:
            text = BACKSLASH_NEWLINE_RE.sub('', text)
        return text

    def transform_paxter_apply(self, token: Command):
        # Fetch the intro value from within the environment if exists
        try:
            intro = self.env[token.intro]
        except KeyError:
            # Otherwise, try to evaluate the intro section
            # using the command evaluator stored within '_cmd_eval_'
            try:
                cmd_eval = self.env['_cmd_eval_']
            except KeyError as exc:
                raise PaxterRenderError(
                    "expected '_cmd_eval_' to be defined at %(pos)s",
                    pos=CharLoc(self.input_text, token.start_pos),
                ) from exc
            try:
                intro = cmd_eval(token.intro, self.env)
            except PaxterRenderError:
                raise
            except Exception as exc:
                raise PaxterRenderError(
                    f"paxter command intro evaluation error at %(pos)s",
                    pos=CharLoc(self.input_text, token.start_pos),
                ) from exc

        # Bail out if options section and main arg section are empty
        if token.options is None and token.main_arg is None:
            return intro

        # Wrap the function if not yet wrapped
        if not isinstance(intro, BaseApply):
            intro = NormalApply(intro)

        # Make the call to the wrapped function
        try:
            return intro.call(self, token)
        except PaxterRenderError:
            raise
        except Exception as exc:
            raise PaxterRenderError(
                f"paxter apply evaluation error at %(pos)s",
                pos=CharLoc(self.input_text, token.start_pos),
            ) from exc
