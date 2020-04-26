"""
Data definition for node types in Paxter parsed tree.
"""
import json
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import List, Match, Optional, Union

__all__ = [
    'Span', 'Token', 'Fragment',
    'FragmentList', 'Text', 'PaxterApply', 'PaxterPhrase',
    'TokenList', 'Identifier', 'Operator', 'Number',
]

_ENABLE_POS_PRINT = True
MainArgument = Union['FragmentList', 'Text']


@dataclass
class Span:
    """
    The position of the first character in the section
    and the position after the last character in the section.
    """
    start: int
    end: int


@dataclass
class Token(metaclass=ABCMeta):
    """
    Base class for all types of nodes to appear in Paxter document tree.
    """

    @property
    @abstractmethod
    def pos(self) -> Span:
        """
        Returns the positional span of the node.
        """
        raise NotImplementedError


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

    @property
    def pos(self) -> Span:
        positions = [token.pos for token in self.children]
        return Span(
            start=min(sub_span.start for sub_span in positions),
            end=max(sub_span.start for sub_span in positions),
        )


@dataclass
class Identifier(Token):
    """
    Node type which represents an identifier and can either be
    the identifier part of or within the option section of the `PaxterApply`.
    """
    name: str
    pos: Span = field(default=None, repr=_ENABLE_POS_PRINT, compare=False)

    @classmethod
    def from_matchobj(cls, matchobj: Match[str], capture_name: str) -> 'Identifier':
        """
        Creates a new node from the provided match object
        returned by regular expression matching under the provided capture group.
        """
        return Identifier(
            name=matchobj.group(capture_name),
            pos=Span(*matchobj.span(capture_name)),
        )


@dataclass
class Operator(Token):
    """
    Node type which represents an operator
    and can only be part of the option section of `PaxterApply`.
    """
    symbol: str
    pos: Span = field(default=None, repr=_ENABLE_POS_PRINT, compare=False)

    @classmethod
    def from_matchobj(cls, matchobj: Match[str], capture_name: str) -> 'Operator':
        """
        Creates a new node from the provided match object
        returned by regular expression matching under the provided capture group.
        """
        return Operator(
            symbol=matchobj.group(capture_name),
            pos=Span(*matchobj.span(capture_name)),
        )


@dataclass
class Number(Token):
    """
    Node type which represents a number recognized by JSON grammar.
    It can only be part of the option section of `PaxterApply`.
    """
    number: Union[int, float]
    pos: Span = field(default=None, repr=_ENABLE_POS_PRINT, compare=False)

    @classmethod
    def from_matchobj(cls, matchobj: Match[str], capture_name: str) -> 'Number':
        """
        Creates a new node from the provided match object
        returned by regular expression matching under the provided capture group.
        """
        return Number(
            number=json.loads(matchobj.group(capture_name)),
            pos=Span(*matchobj.span(capture_name)),
        )


@dataclass
class FragmentList(Fragment):
    """
    Special intermediate node maintaining a list of fragment children nodes.
    This usually corresponds to global-level fragments
    or fragments nested within braces following the @-command.
    """
    children: List[Fragment]

    @property
    def pos(self) -> Span:
        positions = [token.pos for token in self.children]
        return Span(
            start=min(sub_span.start for sub_span in positions),
            end=max(sub_span.start for sub_span in positions),
        )


@dataclass
class Text(Fragment):
    """
    Text node type which does not contain nested @-commands.
    It may be presented as an element of `FragmentList`,
    the main argument of `PaxterApply` and `PaxterPhrase`,
    or within the option section of `PaxterApply`.
    """
    inner: str
    pos: Span = field(default=None, repr=_ENABLE_POS_PRINT, compare=False)

    @classmethod
    def from_matchobj(cls, matchobj: Match[str], capture_name: str) -> 'Text':
        """
        Creates a new node from the provided match object
        returned by regular expression matching under the provided capture group.
        """
        return Text(
            inner=matchobj.group(capture_name),
            pos=Span(*matchobj.span(capture_name)),
        )


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
    pos: Span = field(default=None, repr=_ENABLE_POS_PRINT, compare=False)

    @classmethod
    def from_matchobj(cls, matchobj: Match[str], capture_name: str) -> 'PaxterPhrase':
        """
        Creates a new node from the provided match object
        returned by regular expression matching under the provided capture group.
        """
        return PaxterPhrase(
            inner=matchobj.group(capture_name),
            pos=Span(*matchobj.span(capture_name)),
        )


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

    @property
    def pos(self) -> Span:
        positions = ([self.id.pos]
                     + (self.options.pos if self.options else [])
                     + (self.main_arg.pos if self.main_arg else []))
        return Span(
            start=min(sub_span.start for sub_span in positions),
            end=max(sub_span.start for sub_span in positions),
        )
