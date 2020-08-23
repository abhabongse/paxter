"""
Variable collection of character sets as defined by Paxter language.
They are used to construct tokenizers for language parsing.
"""
import re
import sys
import unicodedata

ID_START_CATEGORIES = ['Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl']
ID_CONT_CATEGORIES = ID_START_CATEGORIES + ['Mn', 'Mc', 'Nd', 'Pc']
SYMBOL_CATEGORIES = ['Ps', 'Pe', 'Pi', 'Pf', 'Pd', 'Po', 'Sc', 'Sk', 'Sm', 'So']
OP_CATEGORIES = ['Pd', 'Po', 'Sc', 'Sk', 'Sm', 'So']
OP_BANNED_CHARS = [',', ';', '@', '#', '"']

ID_START_CHARS = ''.join(
    c for c in map(chr, range(sys.maxunicode + 1))
    if unicodedata.category(c) in ID_START_CATEGORIES or c == '_'
)
ID_CONT_CHARS = ''.join(
    c for c in map(chr, range(sys.maxunicode + 1))
    if unicodedata.category(c) in ID_CONT_CATEGORIES or c == '_'
)
SYMBOL_CHARS = ''.join(
    c for c in map(chr, range(sys.maxunicode + 1))
    if unicodedata.category(c) in SYMBOL_CATEGORIES
)
OP_CHARS = ''.join(
    c for c in map(chr, range(sys.maxunicode + 1))
    if unicodedata.category(c) in OP_CATEGORIES and c not in OP_BANNED_CHARS
)

IDENTIFIER_PATTERN = f'[{re.escape(ID_START_CHARS)}][{re.escape(ID_CONT_CHARS)}]*'
SYMBOL_PATTERN = f'[{re.escape(SYMBOL_CHARS)}]'
OPERATOR_PATTERN = f'[,;]|[{re.escape(OP_CHARS)}]+'

__all__ = [
    'ID_START_CHARS', 'ID_CONT_CHARS', 'SYMBOL_CHARS', 'OP_CHARS',
    'IDENTIFIER_PATTERN', 'SYMBOL_PATTERN', 'OPERATOR_PATTERN',
]
