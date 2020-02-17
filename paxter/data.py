"""
Collection of classes represents data node in parsed tree.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

Atom = Union[str, int, float, bool]


@dataclass
class BaseNode:
    """
    Base class for all types of nodes which would appear in parsed tree.
    """
    start: int
    """Starting index of the node definition inside input string (inclusive)."""

    end: int
    """Ending index of the node definition inside input string (exclusive)."""


@dataclass
class Fragments(BaseNode):
    """
    Represents the concatenation of children nodes in the parsed tree.
    """
    children: List[BaseNode]
    """List of children nodes."""


@dataclass
class EscapedRawString(BaseNode):
    """
    Represent the text wrapped inside the @-expression
    pattern in the form of `@"backslash-escaped string"`.
    """
    escaped_string: str
    """String with backslash being escaped."""


@dataclass
class RawString(BaseNode):
    """
    Represents the actual text lifted from the input string
    without any modifications.
    """
    string: str
    """Actual string."""


@dataclass
class Identifier(BaseNode):
    """
    Represents the identifier name token right after @-symbol.
    """
    name: str
    """Identifier name."""

@dataclass
class AtExpression(BaseNode):
    """
    Represents the @-expression consisting of
    the identifier, option dict, and optional recursive fragments.
    """
    identifier: Identifier
    """Identifier part."""

    options: Dict[str, Atom] = field(default_factory=dict)
    """Options which acts like keyword dictionary."""

    fragments: Optional[Fragments] = None
    """Recursive fragments of the @-expression."""
