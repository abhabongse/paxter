"""
Core implementation of Paxter document pre-processing language.

## Language Specification

```bnf
start ::= fragments
fragments ::= fragment*
fragment ::=
    | "@" IDENTIFIER? "!" wrapped_macro_text    /* PaxterMacro */
    | "@" IDENTIFIER opts? wrapped_fragments    /* PaxterFunc */
    | "@" IDENTIFIER                            /* PaxterPhrase (special case) */
    | "@" wrapped_phrase                        /* PaxterPhrase */
    | "@" wrapped_string_literal                /* Text (special case) */
    | NON_GREEDY_TEXT                           /* Text */
wrapped_macro_text ::=
    | "#" wrapped_macro_text "#"
    | "<" wrapped_macro_text ">"
    | "{" NON_GREEDY_TEXT "}"
wrapped_fragments ::=
    | "#" wrapped_fragments "#"
    | "<" wrapped_fragments ">"
    | "{" fragments "}"
wrapped_phrase ::=
    | "#" wrapped_phrase "#"
    | "<" wrapped_phrase ">"
    | "{" NON_GREEDY_TEXT "}"
wrapped_string_literal ::=
    | "#" wrapped_string_literal "#"
    | "<" wrapped_string_literal ">"
    | "\\"" NON_GREEDY_TEXT "\\""
opts ::= "[" ( opt ( "," opt )* ","? )? "]"    /* space delimited */
opt ::=
    | IDENTIFIER "=" ATOMIC_VALUE
    | ATOMIC_VALUE

NON_GREEDY_TEXT ::= /.*?/
IDENTIFIER ::= /[A-Za-z_][A-Za-z0-9_]*/
ATOMIC_VALUE ::= NUMBER | STRING | IDENTIFIER
```

**Note:** Parsing `NUMBER` and `STRING` tokens will follow
the [JSON specification](https://www.json.org/json-en.html).
"""
from paxter.core.data import (BaseAtom, BaseFragment, FragmentList, Identifier, Literal,
                              Node, PaxterFunc, PaxterMacro, PaxterPhrase, Text)
from paxter.core.exceptions import (PaxterBaseException, PaxterConfigError,
                                    PaxterSyntaxError)
from paxter.core.lexers import Lexer
from paxter.core.parser import Parser
from paxter.core.transformer import Transformer

__all__ = ['BaseAtom', 'BaseFragment', 'FragmentList', 'Identifier', 'Literal',
           'Node', 'PaxterMacro', 'PaxterFunc', 'PaxterPhrase', 'Text',
           'PaxterBaseException', 'PaxterConfigError', 'PaxterSyntaxError',
           'Lexer', 'Parser', 'Transformer']

# Disable all docstrings for classes and functions at this level
__pdoc__ = {item: False for item in __all__}
