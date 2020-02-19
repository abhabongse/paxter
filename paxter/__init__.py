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
    | "@" IDENTIFIER "!" delimited_macro_at_expr
    | "@" "!" delimited_macro_at_expr  /* typically for python stmt */
    | "@" IDENTIFIER options delimited_normal_at_expr
    | "@" IDENTIFIER delimited_normal_at_expr
    | "@" delimited_normal_at_expr  /* typically for python expr */
    | "@" IDENTIFIER
    | NON_GREEDY_RAW_TEXT
delimited_macro_at_expr ::=
    | "#" delimited_macro_at_expr "#"
    | "<" delimited_macro_at_expr ">"
    | "{" NON_GREEDY_RAW_TEXT "}"
options ::= ( option ( "," option )* )?
option ::=
    | /\\s*/ IDENTIFIER /\\s*/ "=" /\\s*/ ATOMIC_VALUE /\\s*/
    | /\\s*/ ATOMIC_VALUE /\\s*/
delimited_normal_at_expr ::=
    | "#" delimited_normal_at_expr "#"
    | "<" delimited_normal_at_expr ">"
    | "{" fragments "}"

RAW_TEXT ::= /.*?/
IDENTIFIER ::= /[A-Za-z_][A-Za-z0-9_]*/
ATOMIC_VALUE ::=
    | NUMBER
    | ESCAPED_STRING
    | NORMAL_IDENTIFIER     /* includes bool and null tokens */
```
"""
