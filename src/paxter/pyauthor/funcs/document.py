"""
Collections of document-related data class to be used
as functions to construct a document for web or print.
"""
from abc import ABCMeta
from dataclasses import dataclass
from typing import List, Union


@dataclass
class BaseNode(metaclass=ABCMeta):
    """
    Base document element node.
    """

    def html(self) -> str:
        """
        Rendered the node into HTML document.
        """
        raise NotImplementedError

    @staticmethod
    def render_fragments(fragments: List[Union[str, 'BaseNode']]) -> str:
        return ''.join(
            fragment.html() if isinstance(fragment, BaseNode) else fragment
            for fragment in fragments
        )


@dataclass
class FragmentNode(BaseNode, metaclass=ABCMeta):
    """
    Element node containing list of fragments.
    """
    children: List[Union[str, BaseNode]]
    HTML_TAG = 'div'

    def html(self) -> str:
        rendered = self.render_fragments(self.children)
        return f'<{self.HTML_TAG}>{rendered}</{self.HTML_TAG}>'


@dataclass
class Paragraph(FragmentNode):
    """
    Paragraph node.
    """
    HTML_TAG = 'p'


@dataclass
class Heading1(FragmentNode):
    """
    First-level heading node.
    """
    HTML_TAG = 'h1'


@dataclass
class Heading2(FragmentNode):
    """
    Second-level heading node.
    """
    HTML_TAG = 'h2'


@dataclass
class Heading3(FragmentNode):
    """
    Third-level heading node.
    """
    HTML_TAG = 'h3'


@dataclass
class Heading4(FragmentNode):
    """
    Fourth-level heading node.
    """
    HTML_TAG = 'h4'


@dataclass
class Heading5(FragmentNode):
    """
    Fifth-level heading node.
    """
    HTML_TAG = 'h5'


@dataclass
class Heading6(FragmentNode):
    """
    Sixth-level heading node.
    """
    HTML_TAG = 'h6'


@dataclass
class Blockquote(FragmentNode):
    """
    Blockquote node.
    """
    HTML_TAG = 'blockquote'


@dataclass
class Bold(FragmentNode):
    """
    Bold text node.
    """
    HTML_TAG = 'strong'


@dataclass
class Italic(FragmentNode):
    """
    Italic text node.
    """
    HTML_TAG = 'em'


@dataclass
class Underline(FragmentNode):
    """
    Underline text node.
    """
    HTML_TAG = 'u'


@dataclass
class Code(FragmentNode):
    """
    Underline text node.
    """
    HTML_TAG = 'code'


@dataclass
class Link(FragmentNode):
    """
    Url link node.
    """
    href: str

    def html(self) -> str:
        rendered = self.render_fragments(self.children)
        return f'<a href="{self.href}">{rendered}</a>'


class HorizontalRule(BaseNode):
    """
    Horizontal rule node.
    """

    def html(self) -> str:
        return '<hr />'


@dataclass
class Image(BaseNode):
    """
    Image node.
    """
    src: str
    alt: str = ""

    def html(self) -> str:
        return f'<img src="{self.src}" alt="{self.alt}" />'


class NumberedList(BaseNode):
    """
    Ordered list node.
    """
    items: List[List[Union[str, BaseNode]]]

    def __init__(self, *items):
        self.items = list(items)

    def html(self) -> str:
        rendered = '\n'.join(
            f'<li>{self.render_fragments(item)}</li>'
            for item in self.items
        )
        return f'<ol>\n{rendered}\n</ol>'


class BulletedList(BaseNode):
    """
    Unordered list node.
    """
    items: List[List[Union[str, BaseNode]]]

    def __init__(self, *items):
        self.items = list(items)

    def html(self) -> str:
        rendered = '\n'.join(
            f'<li>{self.render_fragments(item)}</li>'
            for item in self.items
        )
        return f'<ul>\n{rendered}\n</ul>'
