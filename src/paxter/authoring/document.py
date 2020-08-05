"""
Collections of data classes representing document elements
which may be used to construct a document for web, print, etc.
"""
import html
import re
from dataclasses import InitVar, dataclass
from typing import Iterator, List, Union

from paxter.authoring.standards import flatten
from paxter.exceptions import PaxterRenderError

ElementList = List[Union[None, str, 'Element']]


@dataclass
class Element:
    """
    Base element node type for a structured document.
    """
    PARAGRAPH_SPLIT_RE = re.compile(
        r'(?:[ \t\r\f\v]+|(?<!\\))\n(?:[ \t\r\f\v]*\n)+[ \t\r\f\v]*',
    )

    def html(self) -> str:
        """
        Renders the element into HTML string output.
        """
        return ''.join(self.html_token_stream())

    def latex(self) -> str:
        """
        Renders the element into LaTeX string output.
        This method is presented here as an example of
        what is possible with Paxter package.
        """
        return ''.join(self.latex_token_stream())

    def html_token_stream(self) -> Iterator[str]:
        """
        Produces a sequence of string tokens which is needed to be joined
        in order to produce the final HTML string output.
        """
        raise NotImplementedError

    def latex_token_stream(self) -> Iterator[str]:
        """
        Produces a sequence of string tokens which is needed to be joined
        in order to produce the final LaTeX string output.
        This method is presented here as an example of
        what is possible with Paxter package.
        """
        raise NotImplementedError

    def html_rec_token_stream(self, elements: Union[str, ElementList]) -> Iterator[str]:
        """
        Recursively produces a sequence of HTML string tokens
        from the given input sequence of string or elements.
        """
        for fragment in flatten(elements):
            if isinstance(fragment, str):
                yield html.escape(fragment)
            elif isinstance(fragment, Element):
                yield from fragment.html_token_stream()
            else:
                raise PaxterRenderError(f'malformed encounter: {fragment!r}')

    def split_paragraphs(self, elements: Union[str, ElementList], forced_paragraph: bool) -> ElementList:
        """
        Attempts to split a sequence of string or elements
        using a double newline into a list of paragraphs
        where each paragraph is a sequence of string or elements
        within the same paragraph.
        """
        collection = self._divide_paragraphs(elements)
        if len(collection) == 1 and not forced_paragraph:
            return collection[0]
        children = []
        for paragraph in collection:
            if len(paragraph) == 1 and isinstance(paragraph[0], Element):
                children.append(paragraph[0])
            else:
                children.append(Paragraph(children=paragraph))
        return children

    def _divide_paragraphs(self, elements: Union[str, ElementList]) -> List[ElementList]:
        if isinstance(elements, str):
            return [[elements]]

        # Clean up element list sequence
        fragments = []
        for f in flatten(elements):
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

    def __post_init__(self):
        self.children = self.split_paragraphs(self.children, forced_paragraph=True)

    def html_token_stream(self) -> Iterator[str]:
        yield from self.html_rec_token_stream(self.children)


@dataclass
class RawElement(Element):
    """
    Renders stored string without escaping.
    """
    children: Union[str, ElementList]

    def html_token_stream(self) -> Iterator[str]:
        yield from self.html_rec_token_stream(self.children)

    def html_rec_token_stream(self, elements: Union[str, ElementList]) -> Iterator[str]:
        for fragment in flatten(elements):
            if isinstance(fragment, str):
                yield fragment
            elif isinstance(fragment, Element):
                yield from fragment.html_token_stream()
            else:
                raise PaxterRenderError(f'malformed encounter: {fragment!r}')


#: Line break raw element
line_break = RawElement(children='<br />')
horizontal_rule = RawElement(children='<hr />')
non_breaking_space = RawElement(children='&nbsp;')
hair_space = RawElement(children='&hairsp;')
thin_space = RawElement(children='&thinsp;')


@dataclass
class SimpleElement(Element):
    """
    Simple element node type in the form of
    ``{HTML_OPENING}{rendered content}{HTML_CLOSING}``.
    """
    children: Union[str, ElementList]

    #: Opening part of the element
    HTML_OPENING = '<div>'

    #: Closing part of the element
    HTML_CLOSING = '</div>'

    def html_token_stream(self) -> Iterator[str]:
        yield self.HTML_OPENING
        yield from self.html_rec_token_stream(self.children)
        yield self.HTML_CLOSING


@dataclass
class Paragraph(SimpleElement):
    """"""
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
    forced_paragraph: InitVar[bool] = False

    def __post_init__(self, forced_paragraph: bool):
        self.children = self.split_paragraphs(self.children, forced_paragraph)

    def html_token_stream(self) -> Iterator[str]:
        yield '<blockquote>'
        yield from self.html_rec_token_stream(self.children)
        yield '</blockquote>'


@dataclass
class Link(SimpleElement):
    """
    Hyperlink element.
    """
    children: Union[str, ElementList]
    href: str

    def html_token_stream(self) -> str:
        yield f'<a href="{html.escape(self.href)}">'
        yield from self.html_rec_token_stream(self.children)
        yield '</a>'


@dataclass
class Image(Element):
    """
    Image embedding element., is_joined=False
    """
    src: str
    alt: str = ""

    def html_token_stream(self) -> Iterator[str]:
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

    HTML_OPENING = ''
    HTML_CLOSING = ''

    def __init__(self, *items, forced_paragraph: bool = False):
        self.items = [
            self.split_paragraphs(item, forced_paragraph)
            for item in items
        ]

    def html_token_stream(self) -> Iterator[str]:
        yield self.HTML_OPENING
        for item in self.items:
            yield '<li>'
            yield from self.html_rec_token_stream(item)
            yield '</li>'
        yield self.HTML_CLOSING


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
