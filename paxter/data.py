"""
Collection of classes represents data node in parsed tree.
"""
from dataclasses import dataclass
from typing import List


@dataclass
class Node:
    """
    Base class for all types of nodes in parsed tree.
    """
    start: int
    """The starting position inside content (inclusive)."""

    end: int
    """The ending position inside content (exclusive)."""


@dataclass
class Fragments(Node):
    """
    Fragments type is the concatenation of all other nodes
    at the same level.
    """
    nodes: List[Node]
    """List of nodes."""


@dataclass
class RawString(Node):
    """
    RawString type stores the actual text extracted
    from main content.
    """
    text: str
    """Actual string."""


@dataclass
class Identifier(Node):
    """
    Identifier type stores identifier name
    which appears right after @-symbol of the @-expression.
    """
    name: str


@dataclass
class AtMacroExpr(Node):
    """
    AtMacroExpr type stores the identifier
    as well as the raw string within the @-expression.
    """
    identifier: Identifier
    raw_string: RawString


@dataclass
class AtNormalExpr(Node):
    """
    AtNormalExpr type stores the identifier
    as well as the recursive fragments within the @-expression.
    """
    identifier: Identifier
    fragments: Fragments
