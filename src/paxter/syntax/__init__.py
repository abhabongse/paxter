r"""
This subpackage provides a utility to parse document source text written in
Paxter surface syntax into an abstract syntax tree for further processing.

Here is the rough grammar for Paxter surface syntax.

```ebnf
start: piece*
piece: TEXT_WITHOUT_SWITCH | SWITCH command
command:
    | identifier_call_command           // shadows identifier token
    | COMMAND_SYMBOL                    // shadows operator token and nested command switch
    | command_compatible_token
identifier_call_command: IDENTIFIER call_suffix
token: command_compatible_token | other_token
command_compatible_token:
    | phrase_call_command
    | wrapped_pieces
    | wrapped_text
    | token_list
    | NUMBER
other_token:
    | SWITCH command
    | IDENTIFIER
    | OPERATOR
phrase_call_command: wrapped_head call_suffix
call_suffix:
    | extras? body
    | extras NEGATIVE_BODY_START
    | NEGATIVE_EXTRAS_START NEGATIVE_BODY_START
body: wrapped_pieces | wrapped_text
extras: token_list
token_list: "[" token* "]"              // whitespace ignored
wrapped_pieces: "{" piece* "}" | "#" wrapped_pieces "#"
wrapped_text: "\"" TEXT "\"" | "#" wrapped_text "#"
wrapped_head: "`" TEXT "`" | "#" wrapped_head "#"

TEXT: /.*?/
SWITCH: "$"
TEXT_WITHOUT_SWITCH: /[^$]*?/
IDENTIFIER: /[_\p{Lu,Ll,Lt,Lm,Lo,Nl}][_\p{Lu,Ll,Lt,Lm,Lo,Mn,Mc,Nd,Nl,Pc}]*/
NUMBER: /-?(?:[1-9][0-9]*|0)(?:\.[0-9]+)?(?:[Ee][+-]?[0-9]+)?/
OPERATOR: /[\p{Pd,Po,Sc,Sk,Sm,So}&&[^@#"]]+/        // "[" and "{" implicitly excluded
COMMAND_SYMBOL: /[\p{Ps,Pe,Pi,Pf,Pd,Po,Sc,Sk,Sm,So}&&[^#`"{\[]]+/

NEGATIVE_BODY_START: /(?!#*["{])/
NEGATIVE_EXTRAS_START: /(?!#*\[)/
```
"""
