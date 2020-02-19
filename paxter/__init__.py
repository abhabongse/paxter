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
    | "@" MACRO_IDENTIFIER delimited_macro_at_expr
    | "@" NORMAL_IDENTIFIER options delimited_normal_at_expr
    | "@" NORMAL_IDENTIFIER delimited_normal_at_expr
    | "@" NORMAL_IDENTIFIER
    | "@" delimited_string_literal
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
delimited_string_literal ::=
    | "#" delimited_string_literal "#"
    | "<" delimited_string_literal ">"
    | "\\"" NON_GREEDY_RAW_TEXT "\\""

RAW_TEXT ::= /.*?/
NORMAL_IDENTIFIER ::= /[A-Za-z_][A-Za-z0-9_]]*/
MACRO_IDENTIFIER ::= NORMAL_IDENTIFIER? "!"
ATOMIC_VALUE ::=
    | NUMBER
    | ESCAPED_STRING
    | NORMAL_IDENTIFIER     // includes interpretation of boolean and null value
```
"""
