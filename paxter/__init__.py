"""
Main package of the project.

## Dependencies

Python dependencies required for this package is stored inside
`"requirements.in"` and (by association) `"requirements.txt"` files.

## Command Line Usage

An example command-line usage for this package would be:

```bash
$ python -m paxter
```

To see help messages, use the following command:
```bash
$ python -m paxter --help
```

## Language Specification

```bnf
start ::= fragments
fragments ::= fragment*
fragment ::=
    | "@" IDENTIFIER? "!" wrapped_macro_text    /* PaxterMacro */
    | "@" IDENTIFIER opts? wrapped_fragments /* PaxterFunc */
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
    | "\"" NON_GREEDY_TEXT "\""
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
from paxter.data import (
    AtExprFunc, AtExprMacro, BaseNode, Fragments, Identifier, RawText,
)
from paxter.parser import Paxter
from paxter.transformer import Transformer

__all__ = [
    'AtExprFunc', 'AtExprMacro', 'BaseNode', 'Fragments', 'Identifier', 'RawText',
    'Paxter', 'Transformer',
]
