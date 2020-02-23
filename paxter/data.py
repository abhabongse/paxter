"""
Collection of classes represents data node in parsed tree.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

Atom = Union[str, int, float, bool, None]


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
    Concatenation of children nodes in the parsed tree.
    """
    children: List[BaseNode]
    """List of children nodes."""


@dataclass
class RawText(BaseNode):
    """
    Raw text which is presented inside a list of fragments,
    inside the @-expression macro, or embedded in `@"raw string"`.
    """
    string: str
    """String content."""


@dataclass
class Identifier(BaseNode):
    """
    Identifier name token succeeding the @-symbol.
    """
    name: str
    """Identifier name."""


@dataclass
class AtExprMacro(BaseNode):
    """
    An @-expression macro consisting of (possibly empty) identifier
    plus the wrapped raw text (as in `@id!{raw text}`).

    Note that lone `@id` that is part of a larger @-expression
    will be expanded to `@!{id}`.
    """
    identifier: Identifier
    """Identifier part."""

    raw_text: RawText
    """Raw text under the macro @-expression."""


@dataclass
class AtExprFunc(BaseNode):
    """
    An @-expression function call consisting of the identifier,
    the recursive fragments, and the option dictionary
    (as in `@id[options]{fragments...}`).
    """
    identifier: Identifier
    """Identifier part."""

    fragments: Fragments
    """Recursively nested fragments."""

    options: Dict[str, Atom] = field(default_factory=dict)
    """Options which acts like keyword argument dictionary."""
