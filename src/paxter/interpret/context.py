"""
Implementation of the renderer.
"""
import re
from dataclasses import dataclass, field
from typing import Any, Union

from paxter.exceptions import PaxterRenderError
from paxter.interpret.data import FragmentList
from paxter.interpret.wrappers import BaseApply, NormalApply
from paxter.parse import (
    CharLoc, Command, Fragment, FragmentSeq, Identifier, Number,
    Operator, Text, Token, TokenSeq,
)


@dataclass
class InterpreterContext:
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
    rendered: FragmentList = field(init=False)

    BACKSLASH_NEWLINE_RE = re.compile(r'\\[ \t\r\f\v]*\n[ \t\r\f\v]*')

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

    def transform_fragment_list(self, seq: FragmentSeq) -> FragmentList:
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
        return FragmentList(result)

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
        # Try to interpret the phrase section
        # using the interpret function from _phrase_eval_
        try:
            phrase_eval = self.env['_phrase_eval_']
        except KeyError as exc:
            raise PaxterRenderError(
                "expected '_phrase_eval_' to be defined at %(pos)s",
                pos=CharLoc(self.input_text, token.start_pos),
            ) from exc
        try:
            phrase_value = phrase_eval(token.phrase, self.env)
        except PaxterRenderError:
            raise
        except Exception as exc:
            raise PaxterRenderError(
                "paxter command phrase evaluation error at %(pos)s: "
                f"{token.phrase!r}",
                pos=CharLoc(self.input_text, token.start_pos),
            ) from exc

        # Bail out if options section and main arg section are empty
        if token.options is None and token.main_arg is None:
            return phrase_value

        # Wrap the function if not yet wrapped
        if not isinstance(phrase_value, BaseApply):
            phrase_value = NormalApply(phrase_value)

        # Make the call to the wrapped function
        try:
            return phrase_value.call(self, token)
        except PaxterRenderError:
            raise
        except Exception as exc:
            raise PaxterRenderError(
                "paxter apply evaluation error at %(pos)s",
                pos=CharLoc(self.input_text, token.start_pos),
            ) from exc
