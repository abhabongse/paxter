"""
Collections of data classes representing document elements
which may be used to construct a document for web, print, etc.
"""
import html
import re
from dataclasses import InitVar, dataclass
from typing import Iterator, List, Union

from paxter.authoring.standards import flatten
from paxter.evaluator import FragmentList
from paxter.exceptions import PaxterRenderError


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

    def html_rec_token_stream(
            self,
            blob: Union[str, FragmentList],
    ) -> Iterator[str]:
        """
        Recursively produces a stream of HTML string tokens
        from the given blob which may be a string or a fragment list.
        """
        for fragment in flatten(blob):
            if isinstance(fragment, Element):
                yield from fragment.html_token_stream()
            else:
                yield html.escape(str(fragment))

    def split_paragraphs(
            self,
            blob: Union[str, FragmentList],
            forced_paragraph: bool,
    ) -> FragmentList:
        """
        Attempts to split the given blob
        (which may be a string or a fragment list)
        into a list of paragraphs where each paragraph is
        a list of string or elements within the same paragraph.
        """
        paragraphs = self._inner_split_paragraphs(blob)
        if len(paragraphs) == 1 and not forced_paragraph:
            return paragraphs[0]
        updated_paragraphs = []
        for para in paragraphs:
            if len(para) == 1 and isinstance(para[0], Element):
                updated_paragraphs.append(para[0])
            else:
                updated_paragraphs.append(Paragraph(blob=para))
        return FragmentList(updated_paragraphs)

    def _inner_split_paragraphs(
            self,
            blob: Union[str, FragmentList],
    ) -> FragmentList[FragmentList]:
        # Special case: when the blob is just a string
        # then we treat them as a single element in paragraph.
        if isinstance(blob, str):
            return FragmentList([FragmentList(blob)])

        # Clean up fragment list blob by merging consecutive strings
        blob = self._merge_strings(blob)
        blob = self._strip_paragraph(blob)

        # Split into a collection of paragraphs
        paragraphs = []  # list of paragraphs
        para = []  # list of string or element pieces
        for piece in blob:
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
        return FragmentList(paragraphs)

    def _merge_strings(self, fragments: FragmentList) -> FragmentList:
        groups = []
        for frag in flatten(fragments):
            if isinstance(frag, str):
                if groups and isinstance(groups[-1], FragmentList):
                    groups[-1].append(frag)
                else:
                    groups.append(FragmentList([frag]))
            else:
                groups.append(frag)
        fragments = []
        for grp in groups:
            if isinstance(grp, FragmentList):
                fragments.append(''.join(grp))
            else:
                fragments.append(grp)
        return FragmentList(fragments)

    def _strip_paragraph(self, paragraph: List) -> FragmentList:
        if paragraph and isinstance(paragraph[0], str):
            paragraph[0] = paragraph[0].lstrip()
            if not paragraph[0]:
                paragraph = paragraph[1:]
        if paragraph and isinstance(paragraph[-1], str):
            paragraph[-1] = paragraph[-1].rstrip()
            if not paragraph[-1]:
                paragraph = paragraph[:-1]
        return FragmentList(paragraph)


@dataclass
class Document(Element):
    """
    Topmost-level element for the entire document itself.
    """
    blob: FragmentList

    def __post_init__(self):
        self.blob = self.split_paragraphs(self.blob, forced_paragraph=True)

    def html_token_stream(self) -> Iterator[str]:
        yield from self.html_rec_token_stream(self.blob)


@dataclass
class RawElement(Element):
    """
    Renders stored string without escaping.
    """
    blob: Union[str, FragmentList]

    def html_token_stream(self) -> Iterator[str]:
        yield from self.html_rec_token_stream(self.blob)

    def html_rec_token_stream(self, elements: Union[str, FragmentList]) -> Iterator[str]:
        for fragment in flatten(elements):
            if isinstance(fragment, Element):
                yield from fragment.html_token_stream()
            else:
                yield str(fragment)


#: Line break raw element
line_break = RawElement(blob='<br />')
horizontal_rule = RawElement(blob='<hr />')
non_breaking_space = RawElement(blob='&nbsp;')
hair_space = RawElement(blob='&hairsp;')
thin_space = RawElement(blob='&thinsp;')


@dataclass
class SimpleElement(Element):
    """
    Simple element node type in the form of
    ``{HTML_OPENING}{rendered content}{HTML_CLOSING}``.
    """
    blob: Union[str, FragmentList]

    #: Opening part of the element
    HTML_OPENING = '<div>'

    #: Closing part of the element
    HTML_CLOSING = '</div>'

    def html_token_stream(self) -> Iterator[str]:
        yield self.HTML_OPENING
        yield from self.html_rec_token_stream(self.blob)
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
    blob: Union[str, FragmentList]
    forced_paragraph: InitVar[bool] = False

    def __post_init__(self, forced_paragraph: bool):
        self.blob = self.split_paragraphs(self.blob, forced_paragraph)

    def html_token_stream(self) -> Iterator[str]:
        yield '<blockquote>'
        yield from self.html_rec_token_stream(self.blob)
        yield '</blockquote>'


@dataclass
class Link(SimpleElement):
    """
    Hyperlink element.
    """
    blob: Union[str, FragmentList]
    href: str

    def html_token_stream(self) -> str:
        yield f'<a href="{html.escape(self.href)}">'
        yield from self.html_rec_token_stream(self.blob)
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
    items: List[Union[str, FragmentList]]

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
