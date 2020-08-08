"""
A collection of pre-defined execution environment.
"""
from typing import Optional

from paxter.authoring.controls import for_statement, if_statement
from paxter.authoring.document import (
    Blockquote, Bold, BulletedList, Code,
    Heading1, Heading2, Heading3, Heading4, Heading5, Heading6,
    Image, Italic, Link, NumberedList,
    Paragraph, RawElement, Underline,
    hair_space, horizontal_rule, line_break,
    non_breaking_space, thin_space,
)
from paxter.authoring.standards import phrase_unsafe_eval, python_unsafe_exec, verbatim


def create_simple_env(data: Optional[dict] = None):
    """
    Creates an string environment data for Paxter source code evaluation
    in Python authoring mode.
    """
    data = data or {}
    return {
        '_phrase_eval_': phrase_unsafe_eval,
        'for': for_statement,
        'if': if_statement,
        'python': python_unsafe_exec,
        'verb': verbatim,
        **data,
    }


def create_document_env(data: Optional[dict] = None):
    """
    Creates an string environment data for Paxter source code evaluation
    in Python authoring mode, specializes in constructing documents.
    """
    data = data or {}
    others = data.pop('_others_', {})
    others = {
        '@': '@',
        '.': hair_space,
        ',': thin_space,
        '%': non_breaking_space,
        **others,
    }
    return create_simple_env({
        '_others_': others,
        'raw': RawElement,
        'break': line_break,
        'hrule': horizontal_rule,
        'nbsp': non_breaking_space,
        'hairsp': hair_space,
        'thinsp': thin_space,
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
