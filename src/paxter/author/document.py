"""
Collections of data classes representing document elements
which may be used to construct a document for web, print, etc.
"""
import html
import re
from dataclasses import dataclass
from typing import Iterator, List, Sequence, Union

from paxter.evaluate import FragmentList
from paxter.exceptions import PaxterRenderError


########################
# Base element classes #
########################

@dataclass
class Element:
    """
    Base element node type for a structured document.
    """
    PARAGRAPH_SPLIT_RE = re.compile(r'\n(?:[ \t\r\f\v]*\n)+')

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

    def html_rec_token_stream(self, body: List) -> Iterator[str]:
        """
        Recursively produces a stream of HTML string tokens
        from the given blob which may be a string or a fragment list.
        """
        for elem in body:
            if isinstance(elem, Element):
                yield from elem.html_token_stream()
            elif hasattr(elem, '_html_'):
                yield elem._html_()  # noqa
            else:
                yield html.escape(str(elem))

    def flatten_fragments(self, fragments: Union[str, FragmentList]) -> List:
        """
        Flattens a fragment list of elements
        by unfolding nested fragment lists.
        """
        if not isinstance(fragments, (str, FragmentList)):
            raise PaxterRenderError("expected string or fragment list")
        return list(FragmentList.flatten(fragments))

    def split_fragments(
            self,
            fragments: Union[str, FragmentList],
            forced_paragraph: bool,
    ) -> List:
        """
        Attempts ot split the given fragment list
        into a list of paragraphs where each paragraph
        is a list of elements within the same paragraph.
        """
        paragraphs = self._split_paragraphs(fragments)
        if len(paragraphs) == 1 and not forced_paragraph:
            return list(paragraphs[0])
        result = []
        for para in paragraphs:
            if len(para) == 1 and isinstance(para[0], Element):
                result.append(para[0])
            else:
                result.append(Paragraph(body=para))
        return result

    def _split_paragraphs(
            self,
            fragments: Union[str, FragmentList],
    ) -> List[FragmentList]:

        # Special case: when the blob is just a string
        # then we treat them as a single element in paragraph.
        if isinstance(fragments, str):
            return [FragmentList([fragments])]
        if not isinstance(fragments, FragmentList):
            raise PaxterRenderError("expected string or fragment list")

        # Clean up fragment list blob by merging consecutive strings
        fragments = self._merge_strings(fragments)
        fragments = self._strip_paragraph(fragments)

        # Split into a collection of paragraphs
        paragraphs = []  # list of paragraphs
        para = []  # list of string or element pieces
        for piece in fragments:
            if isinstance(piece, str):
                particles = self.PARAGRAPH_SPLIT_RE.split(piece)
                if len(particles) >= 2:
                    if particles[0].strip():
                        para.append(particles[0])
                    paragraphs.append(para)
                    for p in particles[1:-1]:
                        paragraphs.append([p])
                    para = []
                    if particles[-1].strip():
                        para.append(particles[-1])
                else:
                    para.append(particles[0])
            else:
                para.append(piece)
        if para:
            paragraphs.append(para)

        paragraphs = [
            self._strip_paragraph(paragraph)
            for paragraph in paragraphs
        ]
        return paragraphs

    def _merge_strings(self, fragments: FragmentList) -> List:
        # First pass: group consecutive strings together
        groups = []
        for frag in fragments.flatten():
            if isinstance(frag, str):
                if groups and isinstance(groups[-1], FragmentList):
                    groups[-1].append(frag)
                else:
                    groups.append(FragmentList([frag]))
            else:
                groups.append(frag)
        # Second pass: merge each group consecutive strings into one string
        fragments = []
        for grp in groups:
            if isinstance(grp, FragmentList):
                fragments.append(''.join(grp))
            else:
                fragments.append(grp)
        return fragments

    def _strip_paragraph(self, paragraph: Sequence) -> FragmentList:
        paragraph = list(paragraph)  # make copy
        # Left-strip first paragraph
        if paragraph and isinstance(paragraph[0], str):
            paragraph[0] = paragraph[0].lstrip()
            if not paragraph[0]:
                paragraph = paragraph[1:]
        # Right-strip last paragraph
        if paragraph and isinstance(paragraph[-1], str):
            paragraph[-1] = paragraph[-1].rstrip()
            if not paragraph[-1]:
                paragraph = paragraph[:-1]
        return FragmentList(paragraph)


@dataclass
class RawElement(Element):
    """
    Element which wraps over a raw string
    which will not be escaped when rendered to output.
    """
    body: str

    def __post_init__(self):
        if not isinstance(self.body, str):
            raise PaxterRenderError("expected raw string")

    def html_token_stream(self) -> Iterator[str]:
        yield self.body


@dataclass(init=False)
class SimpleElement(Element):
    """
    Simple element node type which renders output in the form of
    ``{HTML_OPENING}{rendered content}{HTML_CLOSING}``.
    """
    body: List

    #: Opening part of the element
    HTML_OPENING = '<div>'

    #: Closing part of the element
    HTML_CLOSING = '</div>'

    def __init__(self, body: Union[str, FragmentList, List]):
        if isinstance(body, (str, FragmentList)):
            body = self.flatten_fragments(body)
        self.body = body

    def html_token_stream(self) -> Iterator[str]:
        yield self.HTML_OPENING
        yield from self.html_rec_token_stream(self.body)
        yield self.HTML_CLOSING


@dataclass(init=False)
class SequenceElement(Element):
    """
    Special element containing a sequence of items
    where each item is a fragment list.
    """
    items: List[List]

    HTML_GLOBAL_OPENING = ''
    HTML_GLOBAL_CLOSING = ''
    HTML_ITEM_OPENING = ''
    HTML_ITEM_CLOSING = ''

    def __init__(
            self,
            *items: Union[str, FragmentList, List],
            forced_paragraph: bool = False,
    ):
        self.items = []
        for item in items:
            if isinstance(item, (str, FragmentList)):
                item = self.split_fragments(item, forced_paragraph)
            self.items.append(item)

    def html_token_stream(self) -> Iterator[str]:
        yield self.HTML_GLOBAL_OPENING
        for item in self.items:
            yield self.HTML_ITEM_OPENING
            yield from self.html_rec_token_stream(item)
            yield self.HTML_ITEM_CLOSING
        yield self.HTML_GLOBAL_CLOSING


@dataclass(init=False)
class HigherSequenceElement(Element):
    """
    Special element containing a sequence of items
    where each item is an instance of :class:`SequenceElement`.
    """
    items: List

    HTML_OPENING = ''
    HTML_CLOSING = ''

    def __init__(self, *items):
        self.items = list(items)

    def html_token_stream(self) -> Iterator[str]:
        yield self.HTML_OPENING
        yield from self.html_rec_token_stream(self.items)
        yield self.HTML_CLOSING


############################
# Concrete element classes #
############################

@dataclass(init=False)
class Document(Element):
    """
    Topmost-level element for the entire document itself.
    It may split the provided body into multiple paragraphs.
    """
    body: List

    def __init__(self, body: Union[str, FragmentList, List]):
        if isinstance(body, (str, FragmentList)):
            body = self.split_fragments(body, forced_paragraph=True)
        self.body = body

    def html_token_stream(self) -> Iterator[str]:
        yield from self.html_rec_token_stream(self.body)


@dataclass(init=False)
class Paragraph(SimpleElement):
    HTML_OPENING = '<p>'
    HTML_CLOSING = '</p>'


@dataclass(init=False)
class Heading1(SimpleElement):
    HTML_OPENING = '<h1>'
    HTML_CLOSING = '</h1>'


@dataclass(init=False)
class Heading2(SimpleElement):
    HTML_OPENING = '<h2>'
    HTML_CLOSING = '</h2>'


@dataclass(init=False)
class Heading3(SimpleElement):
    HTML_OPENING = '<h3>'
    HTML_CLOSING = '</h3>'


@dataclass(init=False)
class Heading4(SimpleElement):
    HTML_OPENING = '<h4>'
    HTML_CLOSING = '</h4>'


@dataclass(init=False)
class Heading5(SimpleElement):
    HTML_OPENING = '<h5>'
    HTML_CLOSING = '</h5>'


@dataclass(init=False)
class Heading6(SimpleElement):
    HTML_OPENING = '<h6>'
    HTML_CLOSING = '</h6>'


@dataclass(init=False)
class Bold(SimpleElement):
    HTML_OPENING = '<b>'
    HTML_CLOSING = '</b>'


@dataclass(init=False)
class Italic(SimpleElement):
    HTML_OPENING = '<i>'
    HTML_CLOSING = '</i>'


@dataclass(init=False)
class Underline(SimpleElement):
    HTML_OPENING = '<u>'
    HTML_CLOSING = '</u>'


@dataclass(init=False)
class Code(SimpleElement):
    HTML_OPENING = '<code>'
    HTML_CLOSING = '</code>'


@dataclass(init=False)
class Link(SimpleElement):
    """
    Hyperlink element.
    """
    body: List
    href: str

    def __init__(self, body: Union[str, FragmentList, List], href: str):
        super().__init__(body)
        self.href = href

    def html_token_stream(self) -> str:
        yield f'<a href="{html.escape(self.href)}">'
        yield from self.html_rec_token_stream(self.body)
        yield '</a>'


@dataclass(init=False)
class Blockquote(Element):
    """
    Renders the blockquote which may split the provided body
    into multiple paragraphs.
    """
    body: List

    def __init__(
            self,
            body: Union[str, FragmentList, List],
            forced_paragraph: bool = False,
    ):
        if isinstance(body, (str, FragmentList)):
            body = self.split_fragments(body, forced_paragraph)
        self.body = body

    def html_token_stream(self) -> Iterator[str]:
        yield '<blockquote>'
        yield from self.html_rec_token_stream(self.body)
        yield '</blockquote>'


@dataclass
class Image(Element):
    """
    Image embedding element.
    """
    src: str
    alt: str = ""

    def __post_init__(self):
        if not isinstance(self.src, str):
            raise PaxterRenderError(f'image source must be string: {self.src!r}')
        if not isinstance(self.alt, str):
            raise PaxterRenderError(f'image alt text must be string: {self.alt!r}')

    def html_token_stream(self) -> Iterator[str]:
        yield f'<img src="{html.escape(self.src)}" alt="{html.escape(self.alt)}" />'


@dataclass(init=False)
class NumberedList(SequenceElement):
    """
    Element containing an ordered (numbered) list.
    """
    HTML_GLOBAL_OPENING = '<ol>'
    HTML_GLOBAL_CLOSING = '</ol>'
    HTML_ITEM_OPENING = '<li>'
    HTML_ITEM_CLOSING = '</li>'


@dataclass(init=False)
class BulletedList(SequenceElement):
    """
    Element containing an unordered (bulleted) list.
    """
    HTML_GLOBAL_OPENING = '<ul>'
    HTML_GLOBAL_CLOSING = '</ul>'
    HTML_ITEM_OPENING = '<li>'
    HTML_ITEM_CLOSING = '</li>'


@dataclass(init=False)
class Table(HigherSequenceElement):
    """
    Element containing an entire table as a sequence of rows.
    """
    HTML_OPENING = '<table>'
    HTML_CLOSING = '</table>'


@dataclass(init=False)
class TableHeader(SequenceElement):
    """
    Element containing a table header row as a sequence of cells.
    """
    HTML_GLOBAL_OPENING = '<tr>'
    HTML_GLOBAL_CLOSING = '</tr>'
    HTML_ITEM_OPENING = '<th>'
    HTML_ITEM_CLOSING = '</th>'


@dataclass(init=False)
class TableRow(SequenceElement):
    """
    Element containing a table data row as a sequence of cells.
    """
    HTML_GLOBAL_OPENING = '<tr>'
    HTML_GLOBAL_CLOSING = '</tr>'
    HTML_ITEM_OPENING = '<td>'
    HTML_ITEM_CLOSING = '</td>'


#################
# Extra objects #
#################

line_break = RawElement(body='<br />')
horizontal_rule = RawElement(body='<hr />')
non_breaking_space = RawElement(body='&nbsp;')
hair_space = RawElement(body='&hairsp;')
thin_space = RawElement(body='&thinsp;')
