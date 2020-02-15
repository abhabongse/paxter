"""
Paxter experimental language parser.
"""
import logging

from lark import Lark

parser = Lark(
    r"""
    ?start: fragments
    fragments: fragment*
    ?fragment: "@" IDENTIFIER wrapped_fragments -> normal_call
            | RAW_CHAR+
    wrapped_fragments: _LHASH wrapped_fragments _RHASH
                     | _LANGB wrapped_fragments _RANGB
                     | _LBRAC fragments _RBRAC
    
    _LHASH: "#"
    _RHASH: "#"
    _LANGB: "<"
    _RANGB: ">"
    _LBRAC: "{"
    _RBRAC: "}"
    
    RAW_CHAR: /[^@]/
    IDENTIFIER: /[A-Za-z_][0-9A-Za-z_]*/
    """,
    parser='lalr',
    debug=True,
)

document = """
Hello, World!
This is a new line!

@bold{Hello}
@bold{Hello, World! @italic{again}}.
"""
# @bold<{You {are} awesome }>.

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    data = parser.parse(document)
    print(data.pretty())
