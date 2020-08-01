"""
Other document authoring functions.
"""
from paxter.authoring.controls import for_statement, if_statement
from paxter.authoring.document import (
    BareList, Blockquote, Bold, BulletedList,
    Code, Document, Element,
    Heading1, Heading2, Heading3, Heading4, Heading5, Heading6,
    Image, Italic, Link, NumberedList, Paragraph,
    RawElement, SimpleElement, Underline,
    hair_space, horizontal_rule, line_break,
    non_breaking_space, thin_space,
)
from paxter.authoring.environ import create_document_env, create_simple_env
from paxter.authoring.standards import flatten

__all__ = [
    'for_statement', 'if_statement',
    'BareList', 'Blockquote', 'Bold', 'BulletedList',
    'Code', 'Document', 'Element',
    'Heading1', 'Heading2', 'Heading3', 'Heading4', 'Heading5', 'Heading6',
    'Image', 'Italic', 'Link', 'NumberedList', 'Paragraph',
    'RawElement', 'SimpleElement', 'Underline',
    'hair_space', 'horizontal_rule', 'line_break',
    'non_breaking_space', 'thin_space',
    'create_document_env', 'create_simple_env',
    'flatten',
]
