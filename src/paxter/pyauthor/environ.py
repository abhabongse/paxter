"""
A collection of pre-defined execution environment.
"""
from typing import Optional

from paxter.pyauthor.funcs.controls import for_statement, if_statement
from paxter.pyauthor.funcs.document import (
    Blockquote, Bold, BulletedList, Code,
    Heading1, Heading2, Heading3, Heading4, Heading5, Heading6,
    HorizontalRule, Image, Italic, LineBreak, Link, NumberedList,
    Paragraph, Underline,
)
from paxter.pyauthor.funcs.standards import (
    flatten, python_unsafe_exec, starter_unsafe_eval, verb,
)


def create_unsafe_bare_env(data: Optional[dict] = None):
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
        'verb': verb,
        'flatten': flatten,
        **data,
    }


def create_unsafe_document_env(data: Optional[dict] = None):
    """
    Creates an string environment data for Paxter source code evaluation
    in Python authoring mode, specializes in constructing documents.
    """
    return {
        '_starter_eval_': starter_unsafe_eval,
        'for': for_statement,
        'if': if_statement,
        'python': python_unsafe_exec,
        'verb': verb,
        'flatten': flatten,
        'break': LineBreak,
        'hrule': HorizontalRule,
        'paragraph': Paragraph,
        'h1': Heading1,
        'h2': Heading2,
        'h3': Heading3,
        'h4': Heading4,
        'h5': Heading5,
        'h6': Heading6,
        'blockquote': Blockquote,
        'bold': Bold,
        'italic': Italic,
        'underline': Underline,
        'code': Code,
        'link': Link,
        'image': Image,
        'numbered_list': NumberedList,
        'bulleted_list': BulletedList,
        **data,
    }
