r"""
Core functionality of Paxter document pre-processing language.

## Language Specification

Here is the _rough_ grammar of Paxter language in Backus–Naur Form.

```bnf
start ::= non_greedy_fragments                      /* FragmentList */
non_greedy_fragments ::= fragment*?
fragment ::= command | NON_GREEDY_TEXT
command ::=
    | "@" IDENTIFIER options wrapped_main_arg       /* PaxterApply */
    | "@" IDENTIFIER wrapped_main_arg               /* PaxterApply */
    | "@" IDENTIFIER options                        /* PaxterApply */
    | "@" IDENTIFIER                                /* PaxterPhrase (special case) */
    | "@" wrapped_phrase                            /* PaxterPhrase */
    | "@" wrapped_main_arg                          /* FragmentList or Text */
    | "@" SYMBOL                                    /* PaxterPhrase (special case) */
wrapped_main_arg ::=
    | wrapped_fragments                             /* FragmentList */
    | wrapped_quoted_text                           /* Text */
wrapped_fragments ::=
    | "#" wrapped_fragments "#"
    | "<" wrapped_fragments ">"
    | "{" non_greedy_fragments "}"
wrapped_quoted_text ::=
    | "#" wrapped_quoted_text "#"
    | "<" wrapped_quoted_text ">"
    | "\"" NON_GREEDY_TEXT "\""
wrapped_phrase ::=
    | "#" wrapped_phrase "#"
    | "<" wrapped_phrase ">"
    | "|" NON_GREEDY_TEXT "|"
options ::= "[" token*? "]"
token ::=
    | command
    | "(" token*? ")"                               /* TokenList */
    | "[" token*? "]"                               /* TokenList */
    | "{" token*? "}"                               /* TokenList */
    | IDENTIFIER                                    /* Identifier */
    | OPERATOR_TOKEN                                /* Operator */
    | NUMBER_TOKEN                                  /* Number */

NON_GREEDY_TEXT ::= /.*?/
IDENTIFIER ::= ID_START ID_CONT*
OPERATOR_TOKEN ::= "," | ";" | OP_CHAR+
NUMBER_TOKEN ::= /-?(?:[1-9][0-9]*|0)(?:\.[0-9]+)?(?:[Ee][+-]?[0-9]+)?)/
```

### Additional Character Sets

Some of the character sets appeared in the above grammar
has the following definitions.

-   Rule `ID_START` represents a subset of characters that is allowed
    to be the first character of a valid identifier.
    It consists of an underscore (`_`) plus Unicode character classes
    `Lu`, `Ll`, `Lt`, `Lm`, `Lo`, and `Nl`.
-   Rule `ID_CONT` represents a subset of characters that is allowed
    to be the subsequent characters of an identifier.
    It consists of all characters from `ID_START` plus Unicode character
    classes `Mn`, `Mc`, `Nd`, and `Pc`.
-   Rule `OP_CHAR` represents a subset of characters for operator tokens
    within the options section of `PaxterApply`.
    It consists of Unicode character classes `Pd`, `Po` (excluding ';' and ','),
    `Sc`, `Sk`, `Sm`, and `So`.
-   `SYMBOL` represents a subset of characters that is allowed
    to solely appear right after the @-command switch to indicate
    a special case of `PaxterPhrase`.
    It consists of Unicode character classes `Ps`, `Pe`, `Pi`, `Pf`, `Pd`, `Po`,
    `Sc`, `Sk`, `Sm`, and `So`.

### Notes

-   For more information, please consult `paxter.core.data` module
    for definitions of all node types in parsed document tree.
-   While parsing Paxter language input, white space will **not** be ignored
    **except** for within the options section.
-   All rules of the grammar will be parsed non-greedily and without backtracking.
"""
from paxter.core.data import (
    Fragment, FragmentList, Identifier, Number, Operator,
    PaxterApply, PaxterPhrase, Text, Token, TokenList,
)
from paxter.core.parser import parse

__all__ = [
    'Fragment', 'FragmentList', 'Identifier', 'Number', 'Operator',
    'PaxterApply', 'PaxterPhrase', 'Text', 'Token', 'TokenList',
    'parse',
]
