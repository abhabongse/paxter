"""
Unicode helper module.
"""
import sys

import unicodedata

__all__ = ['ID_START_CHARS', 'ID_CONT_CHARS', 'ID_PATTERN']

ID_START_CATEGORIES = ['Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl']
ID_CONT_CATEGORIES = ID_START_CATEGORIES + ['Mn', 'Mc', 'Nd', 'Pc']
ID_START_CHARS = ''.join(
    c for c in map(chr, range(sys.maxunicode + 1))
    if unicodedata.category(c) in ID_START_CATEGORIES or c == '_'
)
ID_CONT_CHARS = ''.join(
    c for c in map(chr, range(sys.maxunicode + 1))
    if unicodedata.category(c) in ID_CONT_CATEGORIES or c == '_'
)
ID_PATTERN = f'[{ID_START_CHARS}][{ID_CONT_CHARS}]*'
