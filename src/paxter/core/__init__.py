r"""
Core functionality of Paxter document pre-processing language.

## Language Specification

Here is the rough grammar of Paxter language in Backus–Naur Form.

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
    | "(" token*? ")"
    | "[" token*? "]"
    | "{" token*? "}"
    | IDENTIFIER                                    /* Identifier */
    | OPERATOR                                      /* Operator */
    | JSON_NUMBER                                   /* Number */

NON_GREEDY_TEXT ::= /.*?/
IDENTIFIER ::= ID_START ID_CONT*
OPERATOR ::= OP_CHAR+
JSON_NUMBER ::= /-?(?:[1-9][0-9]*|0)(?:\.[0-9]+)?(?:[Ee][+-]?[0-9]+)?)/
```

### Notes

-   `ID_START` represents a subset of characters (for regular expression)
    that is allowed to be the first character of an identifier,
    consisting of an underscore (`_`) plus Unicode character classes
    `Lu`, `Ll`, `Lt`, `Lm`, `Lo`, and `Nl`.
-   `ID_CONT` represents a subset of characters (for regular expression)
    that is allowed to be the subsequent characters of an identifier,
    consisting of all characters from `ID_START` plus Unicode character classes
    `Mn`, `Mc`, `Nd`, and `Pc`.
-   `OP_CHAR` represents a subset of characters (for regular expression)
    for operator tokens within the options section of PaxterApply,
    consisting of all characters from Unicode character classes
    `Po`, `Sc`, `Sk`, `Sm`, and `So`.
-   Please consult `paxter.core.data` module for definitions of all node types.
-   While parsing Paxter language input, white space will **not** be ignored
    **except** for within the options section.
"""
from paxter.core.data import (BaseAtom, BaseFragment, FragmentList, Identifier,
                              KeyValue, Literal, Node, PaxterFunc, PaxterMacro,
                              PaxterPhrase, Text)
from paxter.core.exceptions import (PaxterBaseException, PaxterConfigError,
                                    PaxterSyntaxError, PaxterTransformError)
from paxter.core.lexers import Lexer
from paxter.core.parser import Parser
from paxter.core.transformer import BaseTransformer

__all__ = ['BaseAtom', 'BaseFragment', 'FragmentList', 'Identifier', 'KeyValue',
           'Literal', 'Node', 'PaxterMacro', 'PaxterFunc', 'PaxterPhrase', 'Text',
           'PaxterBaseException', 'PaxterConfigError', 'PaxterSyntaxError',
           'PaxterTransformError',
           'Lexer', 'Parser', 'BaseTransformer']

# Disable all docstrings for classes and functions at this level
__pdoc__ = {item: False for item in __all__}
