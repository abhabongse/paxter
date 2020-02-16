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
    Fragments type which is the concatenation of other nodes.
    """
    nodes: List[Node]
    """List of nodes."""


@dataclass
class RawString(Node):
    """
    RawString type which stores the actual string from the main content.
    """
    raw_string: str
    """Actual string."""


@dataclass
class Identifier(Node):
    """
    Identifier which appears right after the @-symbol of the @-expression.
    """
    identifier: str


@dataclass
class AtFragments(Node):
    """
    Standard @-expression with recursive fragments.
    """
    identifier: Identifier
    fragments: Fragments
