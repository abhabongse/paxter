r"""
Core functionality of Paxter document pre-processing language.

## Language Specification

```bnf
start ::= fragments
fragments ::= fragment*
fragment ::=
    | "@" IDENTIFIER? "!" wrapped_text          /* PaxterMacro */
    | "@" IDENTIFIER opts? wrapped_fragments    /* PaxterFunc */
    | "@" IDENTIFIER                            /* PaxterPhrase (special case) */
    | "@" wrapped_text                          /* PaxterPhrase */
    | "@" wrapped_string                        /* Text (special case) */
    | NON_GREEDY_TEXT                           /* Text */
wrapped_text ::=
    | "#" wrapped_text "#"
    | "<" wrapped_text ">"
    | "{" NON_GREEDY_TEXT "}"
wrapped_string ::=
    | "#" wrapped_string_literal "#"
    | "<" wrapped_string_literal ">"
    | "\"" NON_GREEDY_TEXT "\""
wrapped_fragments ::=
    | "#" wrapped_fragments "#"
    | "<" wrapped_fragments ">"
    | "{" fragments "}"
opts ::= "[" ( opt ( "," opt )* ","? )? "]"    /* space delimited */
opt ::=
    | IDENTIFIER "=" ATOMIC_VALUE
    | ATOMIC_VALUE

NON_GREEDY_TEXT ::= /.*?/
NORMAL_ID ::= ID_START ID_CONT*
MACRO_ID ::= NORMAL_ID? "!"
ATOMIC_VALUE ::= NUMBER | STRING | IDENTIFIER

/* Unicode character class in valid identifiers */
ID_START ::= /[_\p{Lu,Ll,Lt,Lm,Lo,Nl}]/
ID_CONT ::=  /[_\p{Lu,Ll,Lt,Lm,Lo,Nl,Mn,Mc,Nd,Pc}]/
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
from paxter.core.transformer import BaseTransformer

__all__ = ['BaseAtom', 'BaseFragment', 'FragmentList', 'Identifier', 'Literal',
           'Node', 'PaxterMacro', 'PaxterFunc', 'PaxterPhrase', 'Text',
           'PaxterBaseException', 'PaxterConfigError', 'PaxterSyntaxError',
           'Lexer', 'Parser', 'BaseTransformer']

# Disable all docstrings for classes and functions at this level
__pdoc__ = {item: False for item in __all__}
