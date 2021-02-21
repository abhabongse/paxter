"""
Collections of data classes representing document elements
which may be used to construct a document for web, print, etc.
"""
from __future__ import annotations

import html
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Union

from paxter.exceptions import PaxterRenderError
from paxter.interp import FragmentList
from paxter.quickauthor.fragmentutils import split_into_paragraphs


########################
# Base element classes #
########################

@dataclass
class Element:
    """
    Base element node type for a structured document.
    """

    def html(self) -> str:
        """
        Renders the element into HTML string output.
        """
        return ''.join(self.html_token_stream())

    def html_token_stream(self) -> Iterator[str]:
        """
        Produces a sequence of string tokens
        which are needed to be joined into the final HTML string output.
        """
        raise NotImplementedError

    def html_from_body(self, body: list) -> Iterator[str]:
        """
        Recursively produces a stream of HTML string tokens
        from the given body which is a list of elements.
        String elements will be HTML-escaped before yielded.
        """
        for elem in body:
            if isinstance(elem, Element):
                yield from elem.html_token_stream()
            elif hasattr(elem, '_html_'):
                yield elem._html_()  # noqa
            else:
                yield html.escape(str(elem))

    @classmethod
    def flatten_fragments(cls, fragments: Union[str, FragmentList]) -> list:
        """
        Flattens a given fragment list
        by unfolding nested fragment list.
        This function returns a list of elements known as a body.
        """
        if not isinstance(fragments, (str, FragmentList)):
            raise PaxterRenderError("expected a string or a fragment list")
        return list(FragmentList.flatten(fragments))

    @classmethod
    def split_fragments(
            cls,
            fragments: Union[str, FragmentList],
            forced_paragraph: bool,
    ) -> list:
        """
        Splits the given fragment list into a list of paragraphs
        where each paragraph is a fragment list of elements
        within the same paragraph.
        """
        paragraphs = split_into_paragraphs(fragments)
        if len(paragraphs) == 1 and not forced_paragraph:
            return list(paragraphs[0])
        result = []
        for para in paragraphs:
            if len(para) == 1 and isinstance(para[0], Element):
                result.append(para[0])
            else:
                result.append(Paragraph.from_fragments(para))
        return result


@dataclass
class RawElement(Element):
    """
    Element type which wraps over a raw string
    which would not be escaped when rendered to output.
    """
    body: str

    def __post_init__(self):
        if not isinstance(self.body, str):
            raise PaxterRenderError("expected raw string")

    def html_token_stream(self) -> Iterator[str]:
        yield self.body


@dataclass
class SimpleElement(Element):
    """
    Simple element node type which renders output in the form of
    ``{OPENING}{rendered body}{CLOSING}``.
    """
    body: list

    #: Opening part of the element
    HTML_OPENING = '<div>'

    #: Closing part of the element
    HTML_CLOSING = '</div>'

    @classmethod
    def from_fragments(cls, fragments: Union[str, FragmentList]):
        """
        Constructs an element from fragment list.
        """
        body = cls.flatten_fragments(fragments)
        return cls(body)

    @classmethod
    def from_direct_args(cls, *items):
        """
        Constructs an element directly from arguments.
        """
        body = list(items)
        return cls(body)

    def html_token_stream(self) -> Iterator[str]:
        yield self.HTML_OPENING
        yield from self.html_from_body(self.body)
        yield self.HTML_CLOSING


@dataclass
class EnumeratingElement(Element):
    """
    Special element which contains an enumeration of items
    where each item is a body (i.e. a list of elements).
    """
    items: list[list]

    #: Opening part of the entire element
    HTML_GLOBAL_OPENING = ''

    #: Closing part of the entire element
    HTML_GLOBAL_CLOSING = ''

    #: Opening part of each item element
    HTML_ITEM_OPENING = ''

    #: Closing part of each item element
    HTML_ITEM_CLOSING = ''

    @classmethod
    def from_direct_args(cls, *items: Union[str, FragmentList]):
        """
        Constructs an element directly from arguments.
        """
        items = [
            cls.split_fragments(fragments, forced_paragraph=False)
            for fragments in items
        ]
        return cls(items)

    def html_token_stream(self) -> Iterator[str]:
        yield self.HTML_GLOBAL_OPENING
        for item in self.items:
            yield self.HTML_ITEM_OPENING
            yield from self.html_from_body(item)
            yield self.HTML_ITEM_CLOSING
        yield self.HTML_GLOBAL_CLOSING


############################
# Concrete element classes #
############################

@dataclass
class Document(Element):
    """
    Topmost-level element for the entire document itself.
    It may split the provided body into multiple paragraphs.
    """
    body: list

    @classmethod
    def from_fragments(cls, fragments: Union[str, FragmentList]):
        body = cls.split_fragments(fragments, forced_paragraph=True)
        return cls(body)

    def html_token_stream(self) -> Iterator[str]:
        yield from self.html_from_body(self.body)


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
class Link(SimpleElement):
    """
    Hyperlink element.
    """
    body: list
    href: str

    @classmethod
    def from_fragments(cls, fragments: Union[str, FragmentList], href: str):
        """
        Constructs an element from fragment list.
        """
        body = cls.flatten_fragments(fragments)
        if not isinstance(href, str):
            raise PaxterRenderError("href must be a string")
        return cls(body, href)

    def html_token_stream(self) -> str:
        yield f'<a href="{html.escape(self.href)}">'
        yield from self.html_from_body(self.body)
        yield '</a>'


@dataclass
class Blockquote(Element):
    """
    Renders the blockquote which may split the provided body
    into multiple paragraphs.
    """
    body: list

    @classmethod
    def from_fragments(cls, fragments: Union[str, FragmentList]):
        """
        Constructs an element from fragment list.
        """
        body = cls.split_fragments(fragments, forced_paragraph=False)
        return cls(body)

    def html_token_stream(self) -> Iterator[str]:
        yield '<blockquote>'
        yield from self.html_from_body(self.body)
        yield '</blockquote>'


@dataclass
class Image(Element):
    """
    Image embedding element.
    """
    #: Image source
    src: str

    #: Image alternative text
    alt: str = ""

    def __post_init__(self):
        if not isinstance(self.src, str):
            raise PaxterRenderError(f'image source must be string: {self.src!r}')
        if not isinstance(self.alt, str):
            raise PaxterRenderError(f'image alt text must be string: {self.alt!r}')

    def html_token_stream(self) -> Iterator[str]:
        yield f'<img src="{html.escape(self.src)}" alt="{html.escape(self.alt)}" />'


@dataclass(init=False)
class NumberedList(EnumeratingElement):
    """
    Element containing an ordered (numbered) list.
    Each item may be split into multiple paragraphs.
    """
    HTML_GLOBAL_OPENING = '<ol>'
    HTML_GLOBAL_CLOSING = '</ol>'
    HTML_ITEM_OPENING = '<li>'
    HTML_ITEM_CLOSING = '</li>'


@dataclass(init=False)
class BulletedList(EnumeratingElement):
    """
    Element containing an unordered (bulleted) list.
    Each item may be split into multiple paragraphs.
    """
    HTML_GLOBAL_OPENING = '<ul>'
    HTML_GLOBAL_CLOSING = '</ul>'
    HTML_ITEM_OPENING = '<li>'
    HTML_ITEM_CLOSING = '</li>'


@dataclass(init=False)
class Table(SimpleElement):
    """
    Element containing an entire table as a sequence of rows.
    """
    HTML_OPENING = '<table>'
    HTML_CLOSING = '</table>'


@dataclass(init=False)
class TableHeader(EnumeratingElement):
    """
    Element containing a table header row as a sequence of cells.
    Each cell may be split into multiple paragraphs.
    """
    HTML_GLOBAL_OPENING = '<tr>'
    HTML_GLOBAL_CLOSING = '</tr>'
    HTML_ITEM_OPENING = '<th>'
    HTML_ITEM_CLOSING = '</th>'


@dataclass(init=False)
class TableRow(EnumeratingElement):
    """
    Element containing a table data row as a sequence of cells.
    Each cell may be split into multiple paragraphs.
    """
    HTML_GLOBAL_OPENING = '<tr>'
    HTML_GLOBAL_CLOSING = '</tr>'
    HTML_ITEM_OPENING = '<td>'
    HTML_ITEM_CLOSING = '</td>'


#################
# Extra objects #
#################

#: Line break raw element
line_break = RawElement(body='<br />')

#: Horizontal rule (thematic break) raw element
horizontal_rule = RawElement(body='<hr />')

#: Non-breaking space raw element
non_breaking_space = RawElement(body='&nbsp;')

#: Hair space raw element
hair_space = RawElement(body='&hairsp;')

#: Thin space raw element
thin_space = RawElement(body='&thinsp;')
