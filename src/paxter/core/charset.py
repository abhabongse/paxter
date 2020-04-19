"""
Collection of character sets.
"""
import re
import sys
import unicodedata

ID_START_CATEGORIES = ['Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl']
ID_CONT_CATEGORIES = ID_START_CATEGORIES + ['Mn', 'Mc', 'Nd', 'Pc']
OP_CATEGORIES = ['Po', 'Sc', 'Sk', 'Sm', 'So']

ID_START_CHARS = ''.join(
    c for c in map(chr, range(sys.maxunicode + 1))
    if unicodedata.category(c) in ID_START_CATEGORIES or c == '_'
)
ID_CONT_CHARS = ''.join(
    c for c in map(chr, range(sys.maxunicode + 1))
    if unicodedata.category(c) in ID_CONT_CATEGORIES or c == '_'
)
OP_CHARS = ''.join(
    c for c in map(chr, range(sys.maxunicode + 1))
    if unicodedata.category(c) in OP_CATEGORIES and c != ',' and c != ';'
)

IDENTIFIER_PATTERN = f'[{re.escape(ID_START_CHARS)}][{re.compile(ID_CONT_CHARS)}]*'
OPERATOR_PATTERN = f'[,;]|[{re.escape(OP_CHARS)}]+'
