"""
Data definitions for node types presented in parsed tree

**Warning:** Docstrings in this module assumes the switch symbol character `@`
for simplicity, though the concept is also applied to other switch symbols.

## Fragment Types

There are four kinds of `BaseFragment` types:
`PaxterMacro`, `PaxterFunc`, `PaxterPhrase`, and `Text`.
The first three types are collectively known as @-expressions.

1.  `PaxterMacro` represents a piece of string in input text with the form
    `@id![...]{...}` or `@id!{...}` where
    -   The identifier part is any valid string of any length followed by a `!`
    -   The option list part follows the [spec described below](#option-list)
    -   The main text part will **not** recognize nested @-expressions

2.  `PaxterFunc` represents a piece of string in input text with the form
    `@id[...]{...}` or `@id{...}` where
    -   The identifier part is any valid string of non-zero length
    -   The option list part follows the [spec described below](#option-list)
    -   The main text part recognizes nested @-expressions

3.  `PaxterPhrase` represents a piece of string in input text with the form
    `@{phrase}` or `@phrase`.
    For the latter form, it must **not** be followed by an opening square bracket
    (i.e. the option list) or a set of opening brace pattern.

4.  `Text` represents all other pieces of string in input text
    or the @-string literal of the form `@"text"`.

## Matching Braces Pattern

For each `{...}` pattern appeared in @-expressions,
it can be recursively wrapped with `#`/`#` pairs or `<`/`>` pairs.

For example, these following `PaxterFunc`'s yield the same parsed tree:

```plain
@id{...}
@id<{...}>
@id#{...}#
@id<<{...}>>
@id<#{...}#>
@id#<{...}>#
@id##{...}##
```

Paxter @-string literal also can be recursively wrapped with
`#`/`#` pairs or `<`/`>` pairs, such as `@#"text"#` or `@<<"text">>`.


## Option List

The option list of key-value pairs is a comma-separated key-value pairs
appearing between a pair of matching square brackets.
If the square brackets is **not at all** present in `PaxterMacro` or `PaxterFunc`,
then it will appear as `None` in the parsed tree of both types of nodes.
Otherwise, it will be a list of `KeyValue` tuple.

For each key-value pair, the value part must be present and can only be
a valid identifier or a valid JSON number or string literal.

On the other hand, the key part is optional or it must be an identifier
preceding the value part (separated by `=`) if present.

For example, the option `[v1,"v2",3,k4=v3,k5="v5",k6=6]`
translates to the following (with unimportant fields omitted for clarity):

```
options = [(None, Identifier("v1"),
           (None, Literal("v2"),
           (None, Literal(3),
           (Identifier("v4", Identifier("v4"),
           (Identifier("v5", Literal("v5"),
           (Identifier("v6", Literal(6)]
```

Please note that white spaces are ignored inside the option list,
and it is the only place where it is so in Paxter language.
"""
from dataclasses import dataclass
from typing import Dict, List, NamedTuple, Optional, Tuple, Union

__all__ = ['Node', 'BaseAtom', 'Identifier', 'Literal', 'KeyValue', 'BaseFragment',
           'FragmentList', 'Text', 'PaxterMacro', 'PaxterFunc', 'PaxterPhrase']

__pdoc__ = {'PaxterWithOptions.get_args_and_kwargs': True}


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
    Base node subclass representing types which are acceptable
    as the value part of the option list of key-value pairs.
    """


@dataclass
class Identifier(BaseAtom):
    """
    Node representing an identifier which immediately follows
    the switch symbol character (such as `@` symbol)
    or which is a part of the option list of key-value pairs.

    Attributes:
        name: Name of the identifier
    """
    name: str


@dataclass
class Literal(BaseAtom):
    """
    Node representing a literal value which can only appear as
    the value part of the option list of key-value pairs.
    The value is the either a JSON number of string
    translated by `json.loads` function.
    """
    value: Union[str, int, float]


class KeyValue(NamedTuple):
    """
    Tuple pair of key and value.
    """
    k: Optional[Identifier]
    """Key part with index 0."""

    v: BaseAtom
    """Value part with index 1."""

    def get_faux_key(self) -> str:
        """
        Obtains the faux key which is the identifier name on the value part
        when the key part is absent.
        It raises `paxter.core.exceptions.PaxterTransformError` otherwise.
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
    Base node subclass representing types which are acceptable
    as part of the list of fragments in `FragmentList`.
    """


@dataclass
class FragmentList(Node):
    """
    Node representing a list of fragment nodes.
    It appears only at the global level of input text
    or as the main text of `PaxterFunc`.

    Attributes:
        children: List of children fragment nodes
    """
    children: List[BaseFragment]


@dataclass
class Text(BaseFragment):
    """
    Node representing text which may be presented inside the main text of
    `FragmentList`, `PaxterMacro`, and `PaxterPhrase`,
    or it may be within the raw text following the @-string literal
    with the form `@"text"`.

    Attributes:
        string: String content
    """
    string: str


@dataclass
class _PaxterWithOptions(BaseFragment):
    id: Identifier
    options: Optional[List[KeyValue]]

    def get_args_and_kwargs(self) -> Tuple[List[BaseAtom], Dict[str, BaseAtom]]:
        """
        Obtains a tuple of args tuple and kwargs dict
        with the same pattern as python function call.
        If the options are out-of-order are any keys are duplicated,
        then `paxter.core.exceptions.PaxterTransformError` will be raised.
        """
        from paxter.core.exceptions import PaxterTransformError

        options: List[KeyValue] = self.options or []
        flipped = False  # kwargs found
        args = []
        kwargs = {}

        for k, v in options:
            if k is not None:
                flipped = True
                if k.name in kwargs:
                    raise PaxterTransformError(
                        f"duplicated keyword {k.name!r} at {{pos}}",
                        positions={'pos': k.start_pos},
                    )
                kwargs[k.name] = v
            elif flipped:
                raise PaxterTransformError(
                    "found positional argument after keyword argument at {pos}",
                    positions={'pos': v.start_pos},
                )
            else:
                args.append(v)

        return args, kwargs


@dataclass
class PaxterMacro(_PaxterWithOptions):
    """
    Node representing @-expression macro with the form
    `@id![...]{...}` or `@id!{...}` where content within the braces
    may not recognize recursively nested @-expressions.

    Attributes:
        id: Identifier part (whose name always contains the `!` ending)
        options: Optional list of key-value pairs within the square brackets
        text: Main text under the @-expression macro
    """
    text: Text

    def get_args_and_kwargs(self):
        """
        Obtains a tuple of args tuple and kwargs dict
        with the same pattern as python function call.
        If the options are out-of-order are any keys are duplicated,
        then `paxter.core.exceptions.PaxterTransformError` will be raised.
        """
        return super().get_args_and_kwargs()


@dataclass
class PaxterFunc(_PaxterWithOptions):
    """
    Node representing @-expression function call with the form
    `@id[...]{...}` or `@id[...]{...}` where content within the braces
    does recognize recursively nested @-expressions.

    Attributes:
        id: Identifier part
        options: Optional list of key-value pairs within the square brackets
        fragments: List of recursively nested fragments
    """
    id: Identifier
    options: Optional[List[KeyValue]]
    fragments: FragmentList

    def get_args_and_kwargs(self):
        """
        Obtains a tuple of args tuple and kwargs dict
        with the same pattern as python function call.
        If the options are out-of-order are any keys are duplicated,
        then `paxter.core.exceptions.PaxterTransformError` will be raised.
        """
        return super().get_args_and_kwargs()


@dataclass
class PaxterPhrase(BaseFragment):
    """
    Node representing @-expression phrase, which is one without real identifier.
    Normally it has the form of `@{phrase}`
    but it may also follow the form of `@phrase`
    if it is **not** immediately followed by an opening square bracket
    or an opening brace pattern.

    Attributes:
        phrase: Any text phrase
    """
    phrase: Text
