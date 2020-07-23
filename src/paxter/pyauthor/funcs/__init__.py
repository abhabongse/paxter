"""
Collection of functions to be used within the Python authoring mode.
"""
from paxter.pyauthor.funcs.controls import for_statement, if_statement
from paxter.pyauthor.funcs.document import (
    BareList, Blockquote, Bold, BulletedList,
    Code, Document, Element, ElementList, HairSpace,
    Heading1, Heading2, Heading3, Heading4, Heading5, Heading6,
    HorizontalRule, Image, Italic, LineBreak, Link, NonBreakingSpace,
    NumberedList, Paragraph, RawElement, SimpleElement,
    ThinSpace, Underline,
)
from paxter.pyauthor.funcs.standards import (
    flatten, python_unsafe_exec, starter_unsafe_eval, verb,
)

__all__ = [
    'for_statement', 'if_statement',
    'BareList', 'Blockquote', 'Bold', 'BulletedList',
    'Code', 'Document', 'Element', 'ElementList', 'HairSpace',
    'Heading1', 'Heading2', 'Heading3', 'Heading4', 'Heading5', 'Heading6',
    'HorizontalRule', 'Image', 'Italic', 'LineBreak', 'Link', 'NonBreakingSpace',
    'NumberedList', 'Paragraph', 'RawElement', 'SimpleElement',
    'ThinSpace', 'Underline',
    'flatten', 'python_unsafe_exec', 'starter_unsafe_eval', 'verb',
]
