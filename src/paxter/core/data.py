"""
Data definition for node types in Paxter parsed tree.
"""
import json
from abc import ABCMeta
from dataclasses import dataclass, field
from typing import List, Match, Optional, Union

from paxter.core.scope_pattern import ScopePattern

__all__ = [
    'Token', 'Fragment',
    'FragmentList', 'Text', 'PaxterApply', 'PaxterPhrase',
    'TokenList', 'Identifier', 'Operator', 'Number',
]

MainArgument = Union['FragmentList', 'Text']


@dataclass
class Token(metaclass=ABCMeta):
    """
    Base class for all types of nodes to appear in Paxter document tree.
    """
    start_pos: int = field(repr=False, compare=False)
    end_pos: int = field(repr=False, compare=False)

    @classmethod
    def without_pos(cls, *args, **kwargs):
        """
        Create instance of the class without start_pos and end_pos.
        """
        return cls(None, None, *args, **kwargs)


@dataclass
class Fragment(Token, metaclass=ABCMeta):
    """
    Subtypes of nodes in Paxter document tree that is allowed
    to appear as elements of `FragmentList`.
    """
    pass


@dataclass
class TokenList(Token):
    """
    Node type which represents a group of tokens wrapped under
    a pair of parentheses `()`, brackets `[]`, or braces `{}`.
    """
    children: List[Token]


@dataclass
class Identifier(Token):
    """
    Node type which represents an identifier and can either be
    the identifier part of or within the option section of the `PaxterApply`.
    """
    name: str

    @classmethod
    def from_matchobj(cls, matchobj: Match[str], capture_name: str) -> 'Identifier':
        """
        Creates a new node from the provided match object
        returned by regular expression matching under the provided capture group.

        This class method only works for classes with a single main value only
        (which includes all token types except `PaxterApply`).
        """
        start_pos, end_pos = matchobj.span(capture_name)
        name = matchobj.group(capture_name)
        return Identifier(start_pos, end_pos, name)


@dataclass
class Operator(Token):
    """
    Node type which represents an operator
    and can only be part of the option section of `PaxterApply`.
    """
    symbol: str

    @classmethod
    def from_matchobj(cls, matchobj: Match[str], capture_name: str) -> 'Operator':
        """
        Creates a new node from the provided match object
        returned by regular expression matching under the provided capture group.

        This class method only works for classes with a single main value only
        (which includes all token types except `PaxterApply`).
        """
        start_pos, end_pos = matchobj.span(capture_name)
        symbol = matchobj.group(capture_name)
        return Operator(start_pos, end_pos, symbol)


@dataclass
class Number(Token):
    """
    Node type which represents a number recognized by JSON grammar.
    It can only be part of the option section of `PaxterApply`.
    """
    value: Union[int, float]

    @classmethod
    def from_matchobj(cls, matchobj: Match[str], capture_name: str) -> 'Number':
        """
        Creates a new node from the provided match object
        returned by regular expression matching under the provided capture group.

        This class method only works for classes with a single main value only
        (which includes all token types except `PaxterApply`).
        """
        start_pos, end_pos = matchobj.span(capture_name)
        value = json.loads(matchobj.group(capture_name))
        return Number(start_pos, end_pos, value)


@dataclass
class FragmentList(Fragment):
    """
    Special intermediate node maintaining a list of fragment children nodes.
    This usually corresponds to global-level fragments
    or fragments nested within braces following the @-command.
    """
    children: List[Fragment]
    scope_pattern: ScopePattern
    is_command: bool = False


@dataclass
class Text(Fragment):
    """
    Text node type which does not contain nested @-commands.
    It may be presented as an element of `FragmentList`,
    the main argument of `PaxterApply` and `PaxterPhrase`,
    or within the option section of `PaxterApply`.
    """
    inner: str
    scope_pattern: ScopePattern
    is_command: bool = False

    @classmethod
    def from_matchobj(
            cls, matchobj: Match[str], capture_name: str,
            scope_pattern: ScopePattern,
    ) -> 'Text':
        """
        Creates a new node from the provided match object
        returned by regular expression matching under the provided capture group.

        This class method only works for classes with a single main value only
        (which includes all token types except `PaxterApply`).
        """
        start_pos, end_pos = matchobj.span(capture_name)
        inner = matchobj.group(capture_name)
        return Text(start_pos, end_pos, inner, scope_pattern, False)


@dataclass
class PaxterPhrase(Fragment):
    """
    Node type which represents @-command and has one of the following form:

    -   It begins with a command switch `@`
        and is immediately followed by a non-empty identifier.
        It also must unambiguously not be a `PaxterApply`
        (i.e. it is not followed by an option section or main argument section).

    -   It begins with a command switch `@` and is immediately followed by
        a wrapped bar section (e.g. `@|...phrase...|`, `@<#|...phrase...|#>`).

    -   It begins with a command switch `@` and is immediately followed by
        a single symbol character that is unmistakeably not a quote `"`,
        a brace `{`, or a bar `|`.
    """
    inner: str
    scope_pattern: ScopePattern

    @classmethod
    def from_matchobj(
            cls, matchobj: Match[str], capture_name: str,
            scope_pattern: ScopePattern,
    ) -> 'PaxterPhrase':
        """
        Creates a new node from the provided match object
        returned by regular expression matching under the provided capture group.

        This class method only works for classes with a single main value only
        (which includes all token types except `PaxterApply`).
        """
        start_pos, end_pos = matchobj.span(capture_name)
        inner = matchobj.group(capture_name)
        return PaxterPhrase(start_pos, end_pos, inner, scope_pattern)


@dataclass
class PaxterApply(Fragment):
    """
    Node type which represents @-command which has the following form:

    -   It begins with a command switch `@`,
        and is immediately followed by a non-empty identifier.

    -   Then it may optionally be followed by an option section
        surrounded by square brackets.

    -   If options section is present, then it may be followed by
        a main argument section; however, if options is not present,
        then it must be followed by the main argument section.

        The main argument section, if present, can either be
        a `FragmentList` (surrounded by wrapped braces such as `{...main arg...}`)
        or a `Text` (surrounded by wrapped quotation marks such as `"...text..."`).
    """
    id: Identifier
    options: Optional[TokenList]
    main_arg: Optional[MainArgument]
