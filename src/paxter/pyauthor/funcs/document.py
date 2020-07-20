"""
Collections of document-related data class to be used
as functions to construct a document for web or print.
"""
import html
from dataclasses import dataclass
from typing import Iterator, List, Union

from paxter.core.exceptions import PaxterRenderError
from paxter.pyauthor.funcs.standards import flatten


@dataclass
class Element:
    """
    Base element node for the document.
    """

    def html(self) -> Iterator[str]:
        """
        Renders the element node into HTML document
        as a sequence of strings.
        """
        raise NotImplementedError

    def tex(self) -> Iterator[str]:
        """
        Renders the element node into TeX document
        as a sequence of strings.
        """
        raise NotImplementedError

    def html_children(self, children) -> Iterator[str]:
        """
        Renders each child element into HTML.
        """
        for fragment in flatten(children, is_joined=False):
            if fragment is None:
                pass
            elif isinstance(fragment, str):
                yield html.escape(fragment)
            elif isinstance(fragment, Element):
                yield from fragment.html()
            else:
                raise PaxterRenderError(f'malformed encounter: {fragment!r}')


@dataclass
class StaticElement(Element):
    """
    Static element content without arguments.
    """
    content: str = '<div />'

    def html(self) -> Iterator[str]:
        yield self.content


LineBreak = StaticElement('<br />')
HorizontalRule = StaticElement('<hr />')


@dataclass
class ElementWithChildren(Element):
    """
    Element nodes with list of fragments as children.
    """
    children: List[Union[str, Element]]
    HTML_TAG = 'div'

    def html(self) -> Iterator[str]:
        yield f'<{self.HTML_TAG}>'
        yield from self.html_children(self.children)
        yield f'</{self.HTML_TAG}>'


@dataclass
class Document(ElementWithChildren):
    """
    Top-most data type for the entire document.
    """

    def render_html(self) -> str:
        """
        Renders the document into HTML output.
        """
        return ''.join(self.html())

    def render_tex(self) -> str:
        """
        Renders the document into TeX output.
        """
        return ''.join(self.tex())

    def html(self) -> Iterator[str]:
        yield from self.html_children(self.children)


@dataclass
class Paragraph(ElementWithChildren):
    HTML_TAG = 'p'


@dataclass
class Heading1(ElementWithChildren):
    HTML_TAG = 'h1'


@dataclass
class Heading2(ElementWithChildren):
    HTML_TAG = 'h2'


@dataclass
class Heading3(ElementWithChildren):
    HTML_TAG = 'h3'


@dataclass
class Heading4(ElementWithChildren):
    HTML_TAG = 'h4'


@dataclass
class Heading5(ElementWithChildren):
    HTML_TAG = 'h5'


@dataclass
class Heading6(ElementWithChildren):
    HTML_TAG = 'h6'


@dataclass
class Blockquote(ElementWithChildren):
    HTML_TAG = 'blockquote'


@dataclass
class Bold(ElementWithChildren):
    HTML_TAG = 'strong'


@dataclass
class Italic(ElementWithChildren):
    HTML_TAG = 'em'


@dataclass
class Underline(ElementWithChildren):
    HTML_TAG = 'u'


@dataclass
class Code(ElementWithChildren):
    HTML_TAG = 'code'


@dataclass
class Link(ElementWithChildren):
    """
    Hyperlink element.
    """
    href: str

    def html(self) -> str:
        yield f'<a href="{html.escape(self.href)}">'
        yield from self.html_children(self.children)
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

    def tex(self) -> Iterator[str]:
        raise NotImplementedError


@dataclass(init=False)
class BareList(Element):
    """
    Element containing a list of items without encapsulation.
    """
    items: List[List[Union[str, Element]]]

    def __init__(self, *items):
        self.items = list(items)

    def html(self) -> Iterator[str]:
        yield from self.html_list_items()

    def html_list_items(self) -> Iterator[str]:
        for item in self.items:
            yield '<li>'
            yield from self.html_children(item)
            yield '</li>'


@dataclass(init=False)
class NumberedList(BareList):
    """
    Element containing an ordered (numbered) list.
    """

    def html(self) -> Iterator[str]:
        yield '<ol>'
        yield from self.html_list_items()
        yield '</ol>'


@dataclass(init=False)
class BulletedList(BareList):
    """
    Element containing an unordered (bulleted) list.
    """

    def html(self) -> Iterator[str]:
        yield '<ul>'
        yield from self.html_list_items()
        yield '</ul>'
