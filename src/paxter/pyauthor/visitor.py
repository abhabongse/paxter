"""
Implementation of the renderer.
"""
import html
import re
from dataclasses import dataclass, field
from typing import Any, List, Union

from paxter.core import (
    CharLoc, Command, Fragment, FragmentList, Identifier, Number,
    Operator, ShortSymbol, Text, Token, TokenList,
)
from paxter.core.exceptions import PaxterRenderError
from paxter.pyauthor.funcs.document import Document, Paragraph
from paxter.pyauthor.funcs.standards import flatten
from paxter.pyauthor.wrappers import BaseApply, NormalApply

BACKSLASH_NEWLINE_RE = re.compile(r'\\\n')
PARAGRAPH_SPLIT_RE = re.compile(
    r'(?:[ \t\r\f\v]+|(?<!\\))\n(?:[ \t\r\f\v]*\n)+[ \t\r\f\v]*',
)


@dataclass
class BaseRenderContext:
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
    tree: FragmentList

    #: Result of the rendering
    rendered: Union[str, list] = field(init=False)

    def __post_init__(self):
        self.rendered = self.render()

    def render(self):
        return self.transform_fragment_list(self.tree)

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
        if isinstance(fragment, ShortSymbol):
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
        return result

    def transform_text(self, token: Text) -> str:
        text = token.inner
        if not token.enclosing.left:
            text = BACKSLASH_NEWLINE_RE.sub('', text)
        return text

    def transform_command(self, token: Command):
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

    def transform_symbol_command(self, token: ShortSymbol):
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


@dataclass
class StringRenderContext(BaseRenderContext):
    """
    String-based variant of rendering class.
    Each fragment list will be flattened into a single string
    each time it is evaluated.
    """

    def transform_fragment_list(self, seq: FragmentList) -> str:
        result = super().transform_fragment_list(seq)
        result = flatten(result, is_joined=True)
        return result


@dataclass
class DocumentRenderContext(BaseRenderContext):
    """
    Document-based variant of rendering class.
    This is for constructing HTML or LaTeX documents.
    """
    rendered: Document = field(init=False)

    def render(self):
        # Top-level paragraph splitting
        document = []  # list of paragraphs
        paragraph = []  # list of pieces
        for fragment in self.tree.children:
            if isinstance(fragment, Text):
                text = fragment.inner
                pieces = [
                    html.escape(BACKSLASH_NEWLINE_RE.sub('', piece))
                    for piece in PARAGRAPH_SPLIT_RE.split(text)
                ]
                if pieces[0].strip():
                    paragraph.append(pieces[0])
                if len(pieces) >= 2:
                    document.append(paragraph)
                    for piece in pieces[1:-1]:
                        document.append([piece])
                    paragraph = []
                    if pieces[-1].strip():
                        paragraph.append(pieces[-1])
            else:
                paragraph.append(fragment)
        if paragraph:
            document.append(paragraph)

        # Re-iterate: for each paragraph in the document
        # if it is not a list of one non-text token,
        # then wrap it under paragraph data class.
        rendered_document = []
        for paragraph in document:
            rendered_paragraph = [
                self.transform_fragment(fragment)
                if isinstance(fragment, Fragment)
                else fragment
                for fragment in paragraph
            ]
            if len(paragraph) == 1 and isinstance(paragraph[0], Fragment):
                rendered_document.append(rendered_paragraph[0])
            else:
                rendered_document.append(Paragraph(rendered_paragraph))

        return Document(children=rendered_document)

    def transform_text(self, token: Text) -> str:
        text = super().transform_text(token)
        text = html.escape(text)
        return text
