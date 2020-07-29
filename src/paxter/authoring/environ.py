"""
A collection of pre-defined execution environment.
"""
from typing import Optional

from paxter.authoring.controls import for_statement, if_statement
from paxter.authoring.document import (
    Blockquote, Bold, BulletedList, Code,
    HairSpace, Heading1, Heading2, Heading3, Heading4, Heading5, Heading6,
    HorizontalRule, Image, Italic, LineBreak, Link, NonBreakingSpace, NumberedList,
    Paragraph, RawElement, ThinSpace, Underline,
)
from paxter.authoring.standards import (
    flatten, python_unsafe_exec, starter_unsafe_eval, verbatim,
)


def create_simple_env(data: Optional[dict] = None):
    """
    Creates an string environment data for Paxter source code evaluation
    in Python authoring mode.
    """
    data = data or {}
    return {
        '_starter_eval_': starter_unsafe_eval,
        'for': for_statement,
        'if': if_statement,
        'python': python_unsafe_exec,
        'verb': verbatim,
        'flatten': flatten,
        **data,
    }


def create_document_env(data: Optional[dict] = None):
    """
    Creates an string environment data for Paxter source code evaluation
    in Python authoring mode, specializes in constructing documents.
    """
    data = data or {}
    symbols = data.pop('_symbols_', {})
    symbols = {
        '!': '',
        '@': '@',
        '.': HairSpace,
        ',': ThinSpace,
        '%': NonBreakingSpace,
        **symbols,
    }
    return create_simple_env({
        '_symbols_': symbols,
        'raw': RawElement,
        'break': LineBreak,
        'hrule': HorizontalRule,
        'nbsp': NonBreakingSpace,
        'hairsp': HairSpace,
        'thinsp': ThinSpace,
        'paragraph': Paragraph,
        'h1': Heading1,
        'h2': Heading2,
        'h3': Heading3,
        'h4': Heading4,
        'h5': Heading5,
        'h6': Heading6,
        'bold': Bold,
        'italic': Italic,
        'uline': Underline,
        'code': Code,
        'blockquote': Blockquote,
        'link': Link,
        'image': Image,
        'numbered_list': NumberedList,
        'bulleted_list': BulletedList,
        **data,
    })
