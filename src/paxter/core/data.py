"""
Data definition for node types in Paxter parsed tree.
"""
from dataclasses import dataclass
from typing import List, Optional, Union

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
class Token:
    """
    Base class for all types of nodes to appear in Paxter parsed tree.
    """
    pass


@dataclass
class Fragment(Token):
    """
    Subcategory of base node representing all kinds of nodes
    which can be an element of the `FragmentList`.
    """
    pass


@dataclass
class FragmentList(Fragment):
    """
    Special intermediate node maintaining a list of fragment children nodes.
    This usually corresponds to global-level fragments
    or fragments nested within braces following the @-command.
    """
    children: List['Fragment']
    opened: str
    closed: str


@dataclass
class Text(Fragment):
    """
    Text node type which does not contain nested @-commands.
    It may be presented as an element of `FragmentList`,
    the main argument of `PaxterApply` and `PaxterPhrase`,
    or within the option section of `PaxterApply`.
    """
    value: str
    opened: str
    closed: str
    pos: Span


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
    id: 'Identifier'
    options: Optional[List[Token]]
    main_arg: Optional[MainArgument]


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
    content: Text


@dataclass
class TokenList(Token):
    """
    Node type which represents a group of tokens wrapped under
    a pair of parentheses `()`, brackets `[]`, or braces `{}`.
    """
    children: List[Token]
    opened: str
    closed: str


@dataclass
class Identifier(Token):
    """
    Node type which represents an identifier and can either be
    the identifier part of or within the option section of the `PaxterApply`.
    """
    name: str
    pos: Span


@dataclass
class Operator(Token):
    """
    Node type which represents an operator
    and can only be part of the option section of `PaxterApply`.
    """
    symbol: str
    pos: Span


@dataclass
class Number(Token):
    """
    Node type which represents a number recognized by JSON grammar.
    It can only be part of the option section of `PaxterApply`.
    """
    number: Union[int, float]
    pos: Span
