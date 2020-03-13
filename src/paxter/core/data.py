"""
Data definitions for node types presented in parsed tree

Docstrings in this module assumes the switch symbol character `@`
for simplicity, though the concept is also applied to other switch symbols.
"""
from dataclasses import dataclass
from typing import List, NamedTuple, Optional, Union

__all__ = ['Node', 'BaseAtom', 'Identifier', 'Literal', 'KeyValue', 'BaseFragment',
           'FragmentList', 'Text', 'PaxterMacro', 'PaxterFunc', 'PaxterPhrase']


@dataclass
class Node:
    """
    Base class for all types of nodes appearing in parsed tree.

    Attributes:
        start_pos: Starting index of the node definition
            inside input string (inclusive)
        end_pos: Ending index of the node definition
            inside input string (exclusive)
    """
    start_pos: int
    end_pos: int


#  ____                    _   _
# | __ )  __ _ ___  ___   / \ | |_ ___  _ __ ___
# |  _ \ / _` / __|/ _ \ / _ \| __/ _ \| '_ ` _ \
# | |_) | (_| \__ \  __// ___ \ || (_) | | | | | |
# |____/ \__,_|___/\___/_/   \_\__\___/|_| |_| |_|
#

@dataclass
class BaseAtom(Node):
    """
    Node types which are acceptable as the value part
    of the key-value option list.
    """


@dataclass
class Identifier(BaseAtom):
    """
    Identifier name which either immediately follows
    the switch symbol character (such as `@` symbol)
    or is a part of the key-value options list.

    Attributes:
        name: Identifier name
    """
    name: str


@dataclass
class Literal(BaseAtom):
    """
    Literal value part of the key-value option list
    which can either be JSON-compatible number or string literals.

    Attributes:
        value: The value of literal being transformed by `json.loads` function
    """
    value: Union[str, int, float]


class KeyValue(NamedTuple):
    """
    Tuple pair of key and value.
    """
    k: Optional[Identifier]
    v: BaseAtom

    def get_faux_key(self) -> str:
        """
        Obtains the faux key which is when the key part is absent
        and the value part is an identifier.
        Raises `PaxterTransformError` otherwise.
        """
        from paxter.core.exceptions import PaxterTransformError

        if self.k is not None:
            raise PaxterTransformError(
                "option should not have the key part at {pos}",
                positions={'pos': self.k.start_pos},
            )
        if not isinstance(self.v, Identifier):
            raise PaxterTransformError(
                "expected non-literal value part at {pos}",
                positions={'pos': self.v.start_pos},
            )
        return self.v.name


#  ____                 _____                                     _
# | __ )  __ _ ___  ___|  ___| __ __ _  __ _ _ __ ___   ___ _ __ | |_
# |  _ \ / _` / __|/ _ \ |_ | '__/ _` |/ _` | '_ ` _ \ / _ \ '_ \| __|
# | |_) | (_| \__ \  __/  _|| | | (_| | (_| | | | | | |  __/ | | | |_
# |____/ \__,_|___/\___|_|  |_|  \__,_|\__, |_| |_| |_|\___|_| |_|\__|
#                                      |___/

@dataclass
class BaseFragment(Node):
    """
    Node types which are allowed to be part
    of the list of fragments.
    """


@dataclass
class FragmentList(Node):
    """
    A list of fragment nodes.

    Attributes:
        children: List of children fragment nodes
    """
    children: List[BaseFragment]


@dataclass
class Text(BaseFragment):
    """
    Text which may be presented inside the main body text of
    `FragmentList`, `PaxterMacro`, and `PaxterPhrase`,
    or may be embedded within the raw text following the pattern `@"text"`.

    Attributes:
        string: String content
    """
    string: str


@dataclass
class PaxterMacro(BaseFragment):
    """
    An @-expression macro following the `@id!{raw text}` pattern,
    consisting of an identifier (whose names always ends with `!`)
    and the wrapped text which _cannot_ contain nested @-expressions.

    Attributes:
        id: Identifier part (always ending with an exclamation mark)
        text: Main text under the @-expression macro
    """
    id: Identifier
    text: Text


@dataclass
class PaxterFunc(BaseFragment):
    """
    An @-expression function call following the `@id[options]{fragments...}`
    pattern (with options) or the `@id{fragments...}` pattern (without options).
    It consists of an identifier, the recursive fragments,
    and the optional key-value option list.

    The key-value option list is a comma-separated key-value pairs.
    For each pair, the value part must be present
    and can only be an identifier or a JSON number/string literal.
    On the other hand, the key part if optional
    and must be an identifier preceding the value part if present
    (with an equal `=` sign separating the key and the value part).

    For example, the option `[v1,"v2",3,k4=v3,k5="v5",k6=6]`
    translates to the following (unimportant fields omitted for clarity):

    ```
    options = [(None, Identifier("v1"),
               (None, Literal("v2"),
               (None, Literal(3),
               (Identifier("v4", Identifier("v4"),
               (Identifier("v5", Literal("v5"),
               (Identifier("v6", Literal(6)]
    ```

    Attributes:
        id: Identifier part
        fragments: List of recursively nested fragments
        options: Optional list of key-value pairs presented within the square brackets.

            - This value will be `None` when square brackets pair is _not_ present.
            - When the square brackets pair is present,
              if the key part is omitted from the key-valur pair,
              the key part will be represented with `None`.

    """
    id: Identifier
    fragments: FragmentList
    options: Optional[List[KeyValue]]

    # TODO: add validation functions
    #       - whether options are all keyword arguments
    #       - whether all positional arguments precede all keyword arguments
    #       - and for each of the above, whether keyword arguments repeat


@dataclass
class PaxterPhrase(BaseFragment):
    """
    An @-expression phrase is one without the identifier.
    Normally it follows the `@{phrase}` pattern,
    but it may also follow the simpler `@phrase` pattern
    if it is unambiguously definitely _not_ the @-expression function call.

    Attributes:
        phrase: Any text phrase
    """
    phrase: Text
