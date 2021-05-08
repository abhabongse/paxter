r"""
This subpackage provides a utility to parse document source text written in
Paxter surface syntax into an abstract syntax tree for further processing.

Here is the rough grammar for Paxter surface syntax.

```ebnf
start: piece*
piece: TEXT_WITHOUT_SWITCH | SWITCH command
command: regular_command
       | wrapped_pieces
       | wrapped_text
       | NUMBER
       | NEGATIVE_COMMAND_START NEGATIVE_BODY_START SYMBOLIC_COMMAND
regular_command: head extras? body
               | head extras NEGATIVE_BODY_START
               | head NEGATIVE_EXTRAS_START NEGATIVE_BODY_START
head: IDENTIFIER | wrapped_head
extras: "[" token* "]"      // ignoring whitespaces between tokens
token: SWITCH command
     | IDENTIFIER
     | wrapped_pieces
     | wrapped_text
     | NUMBER
     | extras
     | OPERATOR
body: wrapped_pieces | wrapped_text
wrapped_pieces: "{" piece* "}" | "#" wrapped_pieces "#"
wrapped_text: "\"" TEXT "\"" | "#" wrapped_text "#"
wrapped_head: "`" TEXT "`" | "#" wrapped_head "#"

TEXT: /.*?/
SWITCH: /@/                 // or exchange with another one from OPERATOR
TEXT_WITHOUT_SWITCH: /[^@]*?/
IDENTIFIER: /[_\p{Lu,Ll,Lt,Lm,Lo,Nl}][_\p{Lu,Ll,Lt,Lm,Lo,Mn,Mc,Nd,Nl,Pc}]*/
SYMBOLIC_COMMAND: /\p{Ps,Pe,Pi,Pf,Pd,Po,Sc,Sk,Sm,So}/
NUMBER: /-?(?:[1-9][0-9]*|0)(?:\.[0-9]+)?(?:[Ee][+-]?[0-9]+)?/
OPERATOR: /[\p{Pd,Po,Sc,Sk,Sm,So}&&[^@#"-]]+/

NEGATIVE_COMMAND_START: /(?!#*`)/
NEGATIVE_BODY_START: /(?!#*["{])/
NEGATIVE_EXTRAS_START: /(?!#*\[)/
```
"""
