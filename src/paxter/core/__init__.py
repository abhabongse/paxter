r"""
Core functionality of Paxter document pre-processing language.

## Language Specification

Here is the rough grammar of Paxter language in Backus–Naur Form.

```bnf
start ::= fragments
fragments ::= fragment*
fragment ::=
    | "@" NORMAL_ID? "!" options? wrapped_text  /* PaxterMacro */
    | "@" NORMAL_ID options? wrapped_fragments  /* PaxterFunc */
    | "@" NORMAL_ID                             /* PaxterPhrase (special) */
    | "@" wrapped_text                          /* PaxterPhrase */
    | "@" wrapped_string                        /* Text (special) */
    | NON_GREEDY_TEXT                           /* Text */
wrapped_text ::=
    | "#" wrapped_text "#"
    | "<" wrapped_text ">"
    | "{" NON_GREEDY_TEXT "}"
wrapped_string ::=
    | "#" wrapped_string "#"
    | "<" wrapped_string ">"
    | "\"" NON_GREEDY_TEXT "\""
wrapped_fragments ::=
    | "#" wrapped_fragments "#"
    | "<" wrapped_fragments ">"
    | "{" fragments "}"
options ::= "[" ( kv_pair ( "," kv_pair )* ","? )? "]"
kv_pair ::= ( NORMAL_ID "=" )? ATOMIC_VALUE

NON_GREEDY_TEXT ::= /.*?/
NORMAL_ID ::= ID_START ID_CONT*
MACRO_ID ::= NORMAL_ID? "!"
ATOMIC_VALUE ::= JSON_NUMBER | JSON_STRING | NORMAL_ID
```

### Notes

- Please consult `paxter.core.data` module for definitions of all node types.
- `ID_START` represents a subset of characters (for regular expression)
  that is allowed to be the first character of an identifier,
  consisting of an underscore (`_`) plus Unicode character classes
  `Lu`, `Ll`, `Lt`, `Lm`, `Lo`, and `Nl`.
- `ID_CONT` represents a subset of characters (for regular expression)
  that is allowed to be the subsequent characters of an identifier,
  consisting of all characters from `ID_START` plus Unicode character classes
  `Mn`, `Mc`, `Nd`, and `Pc`.
- Parsing `JSON_NUMBER` and `JSON_STRING` tokens will strictly follow
  the [JSON specification](https://www.json.org/json-en.html).
  and the value in the parsed tree will be recognized by `json.loads` function.
- While parsing Paxter language input, white space will **not** be ignored
  **except** for within the options list.
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
