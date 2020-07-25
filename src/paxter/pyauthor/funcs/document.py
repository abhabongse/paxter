"""
Collections of document-related data class to be used
as functions to construct a document for web or print.
"""
import html
import re
from dataclasses import dataclass
from typing import Iterator, List, Union

from paxter.core.exceptions import PaxterRenderError
from paxter.pyauthor.funcs.standards import flatten

ElementList = List[Union[None, str, 'Element']]


@dataclass
class Element:
    """
    Base element node type for a structured document.
    """
    PARAGRAPH_SPLIT_RE = re.compile(
        r'(?:[ \t\r\f\v]+|(?<!\\))\n(?:[ \t\r\f\v]*\n)+[ \t\r\f\v]*',
    )

    def html(self) -> Iterator[str]:
        """
        Renders the element node into HTML document
        as a sequence of strings.
        """
        raise NotImplementedError

    def latex(self) -> Iterator[str]:
        """
        Renders the element node into TeX document
        as a sequence of strings.

        This method is here as an example
        of what is possible with Paxter.
        """
        raise NotImplementedError

    def html_recursive(self, data: Union[str, ElementList]) -> Iterator[str]:
        """
        Recursively renders a sequence of string or elements as HTML output.
        """
        for fragment in flatten(data, is_joined=False):
            if isinstance(fragment, str):
                yield html.escape(fragment)
            elif isinstance(fragment, Element):
                yield from fragment.html()
            else:
                raise PaxterRenderError(f'malformed encounter: {fragment!r}')

    def split_paragraph(self, data: Union[str, ElementList]) -> List[ElementList]:
        """
        Attempts to split a sequence of string or elements
        into a list of paragraphs where each element is a sequence
        of string or elements within the same paragraph.
        """
        if isinstance(data, str):
            return [[data]]

        # Clean up element list sequence
        fragments = []
        for f in flatten(data, is_joined=False):
            if fragments and isinstance(fragments[-1], str) and isinstance(f, str):
                fragments[-1] = fragments[-1] + f
            else:
                fragments.append(f)
        fragments = self._clean_paragraph(fragments)

        # Split into a collection of paragraphs
        collection = []  # list of paragraphs
        paragraph = []  # list of string or element pieces
        for f in fragments:
            if isinstance(f, str):
                pieces = self.PARAGRAPH_SPLIT_RE.split(f)
                if len(pieces) >= 2:
                    if pieces[0].strip():
                        paragraph.append(pieces[0])
                    collection.append(paragraph)
                    for p in pieces[1:-1]:
                        collection.append([p])
                    paragraph = []
                    if pieces[-1].strip():
                        paragraph.append(pieces[-1])
                else:
                    paragraph.append(pieces[0])
            elif isinstance(f, Element):
                paragraph.append(f)
            else:
                raise PaxterRenderError(f'malformed encounter: {f!r}')
        if paragraph:
            collection.append(paragraph)

        collection = [
            self._clean_paragraph(paragraph)
            for paragraph in collection
        ]

        return collection

    def _clean_paragraph(self, paragraph: ElementList) -> ElementList:
        if paragraph and isinstance(paragraph[0], str):
            paragraph[0] = paragraph[0].lstrip()
            if not paragraph[0]:
                paragraph = paragraph[1:]
        if paragraph and isinstance(paragraph[-1], str):
            paragraph[-1] = paragraph[-1].rstrip()
            if not paragraph[-1]:
                paragraph = paragraph[:-1]
        return paragraph


@dataclass
class Document(Element):
    """
    Topmost-level element for the entire document itself.
    """
    children: ElementList

    def render_html(self) -> str:
        """
        Renders the document into HTML output.
        """
        return ''.join(self.html())

    def render_tex(self) -> str:
        """
        Renders the document into TeX output.
        """
        return ''.join(self.latex())

    def html(self) -> Iterator[str]:
        collection = self.split_paragraph(self.children)
        for paragraph in collection:
            if len(paragraph) == 1 and isinstance(paragraph[0], Element):
                yield from paragraph[0].html()
            else:
                yield '<p>'
                yield from self.html_recursive(paragraph)
                yield '</p>'


@dataclass
class RawElement(Element):
    """
    Renders stored string without escaping.
    """
    children: Union[str, ElementList]

    def html(self) -> Iterator[str]:
        yield from self.html_recursive(self.children)

    def html_recursive(self, data: Union[str, ElementList]) -> Iterator[str]:
        for fragment in flatten(data, is_joined=False):
            if isinstance(fragment, str):
                yield fragment
            elif isinstance(fragment, Element):
                yield from fragment.html()
            else:
                raise PaxterRenderError(f'malformed encounter: {fragment!r}')


LineBreak = RawElement(children='<br />')
HorizontalRule = RawElement(children='<hr />')
NonBreakingSpace = RawElement(children='&nbsp;')
HairSpace = RawElement(children='&hairsp;')
ThinSpace = RawElement(children='&thinsp;')


@dataclass
class SimpleElement(Element):
    """
    Simple element node type in the form of
    <tag>{rendered content}</tag>.
    """
    children: Union[str, ElementList]
    HTML_OPENING = '<div>'
    HTML_CLOSING = '</div>'

    def html(self) -> Iterator[str]:
        yield self.HTML_OPENING
        yield from self.html_recursive(self.children)
        yield self.HTML_CLOSING


@dataclass
class Paragraph(SimpleElement):
    HTML_OPENING = '<p>'
    HTML_CLOSING = '</p>'


@dataclass
class Heading1(SimpleElement):
    HTML_OPENING = '<h1>'
    HTML_CLOSING = '</h1>'


@dataclass
class Heading2(SimpleElement):
    HTML_OPENING = '<h2>'
    HTML_CLOSING = '</h2>'


@dataclass
class Heading3(SimpleElement):
    HTML_OPENING = '<h3>'
    HTML_CLOSING = '</h3>'


@dataclass
class Heading4(SimpleElement):
    HTML_OPENING = '<h4>'
    HTML_CLOSING = '</h4>'


@dataclass
class Heading5(SimpleElement):
    HTML_OPENING = '<h5>'
    HTML_CLOSING = '</h5>'


@dataclass
class Heading6(SimpleElement):
    HTML_OPENING = '<h6>'
    HTML_CLOSING = '</h6>'


@dataclass
class Bold(SimpleElement):
    HTML_OPENING = '<b>'
    HTML_CLOSING = '</b>'


@dataclass
class Italic(SimpleElement):
    HTML_OPENING = '<i>'
    HTML_CLOSING = '</i>'


@dataclass
class Underline(SimpleElement):
    HTML_OPENING = '<u>'
    HTML_CLOSING = '</u>'


@dataclass
class Code(SimpleElement):
    HTML_OPENING = '<code>'
    HTML_CLOSING = '</code>'


@dataclass
class Blockquote(Element):
    """
    Renders the blockquote which may contain multiple paragraphs.
    """
    children: Union[str, ElementList]
    forced_paragraph: bool = False

    def html(self) -> Iterator[str]:
        yield '<blockquote>'
        collection = self.split_paragraph(self.children)
        if len(collection) == 1 and not self.forced_paragraph:
            yield from self.html_recursive(collection[0])
        else:
            for paragraph in collection:
                if len(paragraph) == 1 and isinstance(paragraph[0], Element):
                    yield from self.html_recursive(paragraph)
                else:
                    yield '<p>'
                    yield from self.html_recursive(paragraph)
                    yield '</p>'
        yield '</blockquote>'


@dataclass
class Link(SimpleElement):
    """
    Hyperlink element.
    """
    children: Union[str, ElementList]
    href: str

    def html(self) -> str:
        yield f'<a href="{html.escape(self.href)}">'
        yield from self.html_recursive(self.children)
        yield '</a>'


@dataclass
class Image(Element):
    """
    Image embedding element.
    """
    src: str
    alt: str = ""

    def html(self) -> Iterator[str]:
        if not isinstance(self.src, str):
            raise PaxterRenderError(f'image source must be string: {self.src!r}')
        if not isinstance(self.alt, str):
            raise PaxterRenderError(f'image alt text must be string: {self.alt!r}')
        yield f'<img src="{html.escape(self.src)}" alt="{html.escape(self.alt)}" />'


@dataclass(init=False)
class BareList(Element):
    """
    Element containing a list of items without encapsulation.
    """
    items: List[Union[str, ElementList]]
    forced_paragraph: bool = False

    HTML_OPENING = ''
    HTML_CLOSING = ''

    def __init__(self, *items):
        self.items = list(items)

    def html(self) -> Iterator[str]:
        yield self.HTML_OPENING
        yield from self.html_list_items()
        yield self.HTML_CLOSING

    def html_list_items(self) -> Iterator[str]:
        for item in self.items:
            yield '<li>'
            collection = self.split_paragraph(item)
            if len(collection) == 1 and not self.forced_paragraph:
                yield from self.html_recursive(collection[0])
            else:
                for paragraph in collection:
                    if len(paragraph) == 1 and isinstance(paragraph[0], Element):
                        yield from self.html_recursive(paragraph)
                    else:
                        yield '<p>'
                        yield from self.html_recursive(paragraph)
                        yield '</p>'
            yield '</li>'


@dataclass(init=False)
class NumberedList(BareList):
    """
    Element containing an ordered (numbered) list.
    """
    HTML_OPENING = '<ol>'
    HTML_CLOSING = '</ol>'


@dataclass(init=False)
class BulletedList(BareList):
    """
    Element containing an unordered (bulleted) list.
    """
    HTML_OPENING = '<ul>'
    HTML_CLOSING = '</ul>'
