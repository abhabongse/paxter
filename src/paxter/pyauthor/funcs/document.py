"""
Collections of document-related data class to be used
as functions to construct a document for web or print.
"""
from dataclasses import dataclass, field
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


@dataclass
class StaticElement(Element):
    """
    Static element content without arguments.
    """
    html_content: str = '<div />'

    def html(self) -> Iterator[str]:
        yield self.html_content


LineBreak = StaticElement('<br />')
HorizontalRule = StaticElement('<hr />')


@dataclass
class ChildrenFragmentElement(Element):
    """
    Element nodes with list of fragments as children.
    """
    children: List[Union[str, Element]]
    html_tag: str = 'div'

    def html(self) -> Iterator[str]:
        yield f'<{self.html_tag}>'
        for fragment in self.children:
            if isinstance(fragment, str):
                yield fragment
            elif isinstance(fragment, Element):
                yield from fragment.html()
            else:
                raise PaxterRenderError('malformed document')
        yield f'</{self.html_tag}>'


@dataclass
class Document(ChildrenFragmentElement):
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


@dataclass
class Paragraph(ChildrenFragmentElement):
    html_tag: str = field(default='p', init=False)


@dataclass
class Heading1(ChildrenFragmentElement):
    html_tag: str = field(default='h1', init=False)


@dataclass
class Heading2(ChildrenFragmentElement):
    html_tag: str = field(default='h2', init=False)


@dataclass
class Heading3(ChildrenFragmentElement):
    html_tag: str = field(default='h3', init=False)


@dataclass
class Heading4(ChildrenFragmentElement):
    html_tag: str = field(default='h4', init=False)


@dataclass
class Heading5(ChildrenFragmentElement):
    html_tag: str = field(default='h5', init=False)


@dataclass
class Heading6(ChildrenFragmentElement):
    html_tag: str = field(default='h6', init=False)


@dataclass
class Blockquote(ChildrenFragmentElement):
    html_tag: str = field(default='blockquote', init=False)


@dataclass
class Bold(ChildrenFragmentElement):
    html_tag: str = field(default='strong', init=False)


@dataclass
class Italic(ChildrenFragmentElement):
    html_tag: str = field(default='em', init=False)


@dataclass
class Underline(ChildrenFragmentElement):
    html_tag: str = field(default='u', init=False)


@dataclass
class Code(ChildrenFragmentElement):
    html_tag: str = field(default='code', init=False)


@dataclass
class Link(Element):
    """
    Hyperlink element.
    """
    children: List[Union[str, Element]]
    href: str

    def html(self) -> str:
        yield f'<a href="{self.href}">'
        for fragment in self.children:
            if isinstance(fragment, str):
                yield fragment
            elif isinstance(fragment, Element):
                yield from fragment.html()
            else:
                raise PaxterRenderError('malformed document')
        yield '</a>'

    def tex(self) -> Iterator[str]:
        raise NotImplementedError


@dataclass
class Image(Element):
    """
    Image embedding element.
    """
    src: str
    alt: str = ""

    def html(self) -> Iterator[str]:
        src = flatten(self.src, is_joined=True)
        yield f'<img src="{src}" alt="{self.alt}" />'

    def tex(self) -> Iterator[str]:
        raise NotImplementedError


class BareList(Element):
    """
    Element containing a list of items without encapsulation.
    """
    items: List[List[Union[str, Element]]]

    def __init__(self, *items):
        self.items = list(items)

    def html(self) -> Iterator[str]:
        for item in self.items:
            yield '<li>'
            if isinstance(item, str):
                yield item
            elif isinstance(item, list):
                for fragment in item:
                    if isinstance(fragment, str):
                        yield fragment
                    elif isinstance(fragment, Element):
                        yield from fragment.html()
                    else:
                        raise PaxterRenderError('malformed document')
            else:
                raise PaxterRenderError('malformed document')
            yield '</li>'


class NumberedList(BareList):
    """
    Element containing an ordered (numbered) list.
    """

    def html(self) -> Iterator[str]:
        yield '<ol>'
        yield from super().html()
        yield '</ol>'


class BulletedList(BareList):
    """
    Element containing an unordered (bulleted) list.
    """

    def html(self) -> Iterator[str]:
        yield '<ul>'
        yield from super().html()
        yield '</ul>'
