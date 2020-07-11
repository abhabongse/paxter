"""
Collections of document-related data class to be used
as functions to construct a document for web or print.
"""
from dataclasses import dataclass
from typing import Any, List


@dataclass
class ElementNode:
    pass


@dataclass
class Paragraph(ElementNode):
    """
    Paragraph.
    """
    fragments: List[Any]

    def html(self) -> str:
        return '<p></p>'


@dataclass
class H1(ElementNode):
    """
    First-level heading.
    """
    fragments: List[Any]

    def html(self) -> str:
        return '<h1></h1>'
