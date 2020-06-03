"""
Data definitions for node types in Paxter parsed tree.
"""
import json
from abc import ABCMeta
from dataclasses import dataclass, field
from typing import Any, List, Match, Optional, Type, TypeVar, Union

from paxter.core.enclosing import EnclosingPattern

__all__ = [
    'Token', 'Fragment',
    'TokenList', 'Identifier', 'Operator', 'Number',
    'FragmentList', 'Text', 'Command',
]

MainArgument = Union['FragmentList', 'Text']
T = TypeVar('T', bound='Token')


@dataclass
class Token(metaclass=ABCMeta):
    """
    Base class for all types of nodes to appear in Paxter document tree.
    """
    #: The index of the starting position of the token
    start_pos: int = field(repr=True, compare=False)

    #: The index right after the ending position of the token
    end_pos: int = field(repr=True, compare=False)

    @classmethod
    def from_matchobj(
            cls: Type[T], matchobj: Match[str], capture_name: str,
            *args, **kwargs,
    ) -> T:
        """
        Creates a new node from the provided match object
        returned by regexp matching under the provided capture group name.

        This class method work only with subclasses of this parent class
        when it has just one extra attribute.
        """
        if not callable(cls.sanitize):
            raise RuntimeError("something went horribly wrong")  # pragma: no cover

        value = cls.sanitize(matchobj.group(capture_name))
        start_pos, end_pos = matchobj.span(capture_name)
        return cls(start_pos, end_pos, value, *args, **kwargs)  # type: ignore

    @classmethod
    def sanitize(cls, value: str) -> Any:
        """
        Sanitizes string form of value (extracted from match object)
        into proper type so that it can be saved to the first argument
        of node construction.
        """
        return value

    @classmethod
    def without_pos(cls, *args, **kwargs):
        """
        Creates a new node but specifying the position with null data.
        """
        return cls(None, None, *args, **kwargs)


@dataclass
class Fragment(Token, metaclass=ABCMeta):
    """
    Subtypes of nodes in Paxter document tree that is allowed
    to appear as elements of :class:`FragmentList`.
    """
    pass


@dataclass
class TokenList(Token):
    """
    Node type which represents a sequence of tokens wrapped under
    a pair of parentheses ``()``, brackets ``[]``, or braces ``{}``,
    all of which appears exclusively within the option section of :class:`Command`.
    """
    #: List of :class:`Token` instances
    children: List[Token]

    sanitize = None


@dataclass
class Identifier(Token):
    """
    Node type which represents an identifier,
    which can appear only within the option section of :class:`Command`.
    """
    #: Identifier string name
    name: str


@dataclass
class Operator(Token):
    """
    Node type which represents an operator,
    which can appear only within the option section of :class:`Command`.
    """
    #: Symbol as a string of characters
    symbols: str


@dataclass
class Number(Token):
    """
    Node type which represents a number recognized by JSON grammar.
    It appears exclusively within the option section of :class:`PaxterApply`.
    """
    #: Numerical value deserialized from the number literal
    value: Union[int, float]

    @classmethod
    def sanitize(cls, value: str) -> Union[int, float]:
        return json.loads(value)


@dataclass
class FragmentList(Fragment):
    """
    Special intermediate node maintaining a list of fragment children nodes.
    Nodes of this type usually correspond to either the global-level fragments
    or fragments nested within enclosing brace pattern.

    The enclosing brace pattern may appear right after the @-symbol
    within the option section of the :class:`Command` node
    or as a :class:`Fragment` node within the :class:`FragmentList`.
    It may also appear as the main argument of a :class:`Command` node.
    """
    #: List of :class:`Fragment` instances
    children: List[Fragment]

    #: Information of the enclosing braces pattern
    enclosing: EnclosingPattern

    #: Boolean indicating whether this fragment list begins with @-symbol
    #: (i.e. whether it is a part of @-expression)
    at_prefix: bool = False

    sanitize = None


@dataclass
class Text(Fragment):
    """
    Text node type which does not contain nested @-expressions.
    Nodes of this type usually be presented as an element of :class:`FragmentList`
    or as text wrapped within enclosing quoted pattern.

    The enclosing quote pattern may appear right after the @-symbol
    within the option section of the :class:`Command` node
    or as a :class:`Fragment` node within the :class:`FragmentList`.
    It may also appear as the main argument of a :class:`Command` node.
    """
    #: Inner string content
    inner: str

    #: Information of the enclosing quote pattern
    enclosing: EnclosingPattern

    #: Boolean indicating whether this fragment list begins with @-symbol
    #: (i.e. whether it is a part of @-expression)
    at_prefix: bool = False


@dataclass
class Command(Fragment):
    """
    Node type which represents @-command which has the following form:

    - It begins with a command switch ``@``,

    - Then, it is immediately followed by a command introduction section
      which is simply a string in valid identifier form
      or a string surrounded by enclosing bar pattern: ``|...|``.

    - Next, it may optionally be followed by an option section
      surrounded by square brackets: ``[...]``.

    - Finally, it may optionally be followed by a main argument section
      which can either be a :class:`Fragment` or a :class:`Text`.
      Note that the former would be surrounded by
      the enclosing brace pattern such as ``{...}``
      whereas the latter by the enclosing quote pattern such as ``"..."``.
    """
    #: Command introduction section
    intro: str

    #: Information of the enclosing bar pattern over the introduction section
    intro_enclosing: EnclosingPattern

    #: A list of tokens for the option section enclosed by ``[]``,
    #: or :const:`None` if this section is not present.
    options: Optional[TokenList]

    #: The main argument section at the end of expression,
    #: or :const:`None` if this section is not present.
    main_arg: Optional[MainArgument]
