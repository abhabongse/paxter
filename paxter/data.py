"""
Collection of classes represents data node in parsed tree.
"""
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union


@dataclass
class Node:
    """
    Base class for all types of nodes appearing in parsed tree.
    """
    start_index: int
    """Starting index of the node definition inside input string (inclusive)."""

    end_index: int
    """Ending index of the node definition inside input string (exclusive)."""


#  ____                    _   _
# | __ )  __ _ ___  ___   / \ | |_ ___  _ __ ___
# |  _ \ / _` / __|/ _ \ / _ \| __/ _ \| '_ ` _ \
# | |_) | (_| \__ \  __// ___ \ || (_) | | | | | |
# |____/ \__,_|___/\___/_/   \_\__\___/|_| |_| |_|
#

@dataclass
class BaseAtom(Node):
    """
    Node types which are acceptable as the value part of the key-value option list.
    """
    pass


@dataclass
class Identifier(BaseAtom):
    """
    Identifier name which immediately follows the @-symbol (except for phrases)
    or which is part of the key-value option list.
    """
    name: str
    """Identifier name."""


@dataclass
class Literal(BaseAtom):
    """
    Literal value part of the key-value option list.
    It can either be JSON-compatible number or string literal.
    """
    value: Union[str, int, float]
    """Python value of the JSON number of string literal."""


KeyValue = Tuple[Identifier, Optional[BaseAtom]]


#  ____                 _____                                     _
# | __ )  __ _ ___  ___|  ___| __ __ _  __ _ _ __ ___   ___ _ __ | |_
# |  _ \ / _` / __|/ _ \ |_ | '__/ _` |/ _` | '_ ` _ \ / _ \ '_ \| __|
# | |_) | (_| \__ \  __/  _|| | | (_| | (_| | | | | | |  __/ | | | |_
# |____/ \__,_|___/\___|_|  |_|  \__,_|\__, |_| |_| |_|\___|_| |_|\__|
#                                      |___/

@dataclass
class BaseFragment(Node):
    """
    Node types which are allowed to be part of the list of fragments.
    """
    pass


@dataclass
class Text(BaseFragment):
    """
    Text which may be presented inside a list of fragments,
    inside an @-expression macro, or embedded within the `@"raw string"`.
    """
    string: str
    """String content."""


@dataclass
class PaxterMacro(BaseFragment):
    """
    An @-expression macro following the `@id!{raw text}` pattern,
    consisting of an identifier (whose names ends with `!`)
    and the wrapped text which cannot contain nested @-expressions.
    """
    id: Identifier
    """Identifier part (always ending with an exclamation mark)."""

    text: Text
    """Text under the @-expression macro."""


@dataclass
class PaxterFunc(BaseFragment):
    """
    An @-expression function call following the `@id[options]{fragments...}`
    pattern (with options) or the `@id{fragments...}` pattern (without options).
    It consists of an identifier, the recursive fragments,
    and the optional key-value option list.

    The key-value option list is a comma-separated key-value pairs.
    For each pair, the key part must always present as an identifier,
    but the value part may still be absent from the key-value pair.
    Should the value part be present, there must be a `=` sign separating
    the key part and the value part within the key-value pair.
    """
    id: Identifier
    """Identifier part."""

    fragments: List[BaseFragment]
    """Recursively nested fragments."""

    options: Optional[List[KeyValue]]
    """
    Optional list of key-value pairs presented within the square brackets.
    
    - This value will be `None` when square brackets are not present.
    - If the value part is not present within each key-value pair,
      the value part will be represented with `None`.
    """


@dataclass
class PaxterPhrase(BaseFragment):
    """
    An @-expression phrase is one without the identifier.
    Normally it follows the `@{phrase}` pattern,
    but it may also follow the simpler `@phrase` pattern
    if it is unambiguously definitely _not_ the @-expression function call.
    """
    phrase: Text
    """Any text phrase."""
