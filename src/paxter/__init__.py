r"""
Paxter is a document-first, text pre-processing language toolchain,
loosely inspired by @-expressions in Racket

Here is the rough grammar for Paxter document syntax.

```ebnf
start: piece*
piece: TEXT_WITHOUT_SWITCH | SWITCH command
command: regular_command | NEGATIVE_COMMAND_START SYMBOLIC_COMMAND
regular_command: head extras? body
               | head extras NEGATIVE_BODY_START
               | head NEGATIVE_EXTRAS_START NEGATIVE_BODY_START
head: IDENTIFIER | wrapped_head
extras: "[" token* "]"      // ignoring whitespaces between tokens
token: SWITCH command
     | IDENTIFIER
     | NUMBER
     | wrapped_pieces
     | wrapped_text
     | extras
     | OPERATOR
body: wrapped_pieces | wrapped_text
wrapped_pieces: "{" piece* "}" | "#" wrapped_pieces "#"
wrapped_text: "\"" TEXT "\"" | "#" wrapped_text "#"
wrapped_head: "`" TEXT "`" | "#" wrapped_head "#"

TEXT: /.*?/
SWITCH: /@/                 // or exchange with another one from OPERATOR
TEXT_WITHOUT_SWITCH: /[^@]*?/
IDENTIFIER: /\p{Lu,Ll,Lt,Lm,Lo,Nl}\p{Lu,Ll,Lt,Lm,Lo,Mn,Mc,Nd,Nl,Pc}*/
SYMBOLIC_COMMAND: /\p{Ps,Pe,Pi,Pf,Pd,Po,Sc,Sk,Sm,So}/
NUMBER: /-?(?:[1-9][0-9]*|0)(?:\.[0-9]+)?(?:[Ee][+-]?[0-9]+)?/
OPERATOR: /[\p{Pd,Po,Sc,Sk,Sm,So}&&[^@#"-]]+/

NEGATIVE_COMMAND_START: /(?!#*`)/
NEGATIVE_BODY_START: /(?!#*["{])/
NEGATIVE_EXTRAS_START: /(?!#*\[)/
```
"""
from __future__ import annotations

import json
import os

__all__ = []

this_dir = os.path.dirname(os.path.abspath(__file__))
metadata_file = os.path.join(this_dir, 'meta.json')

try:
    with open(metadata_file) as fobj:
        metadata = json.load(fobj)
except Exception:  # pragma: no cover
    metadata = {}

__author__ = metadata.get('author')
__version__ = metadata.get('version')
__status__ = metadata.get('status')
__license__ = metadata.get('license')
__maintainers__ = metadata.get('maintainers')
