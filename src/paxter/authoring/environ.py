"""
A collection of pre-defined execution environment.
"""
from __future__ import annotations

from typing import Optional

from paxter.authoring.controls import for_statement, if_statement
from paxter.authoring.elements import (
    Blockquote, Bold, BulletedList, Code,
    Heading1, Heading2, Heading3, Heading4, Heading5, Heading6,
    Image, Italic, Link, NumberedList, Paragraph, RawElement,
    Table, TableHeader, TableRow, Underline,
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
        '_extras_': {},
        '@': '@',
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
    return create_simple_env({
        'raw': RawElement,
        'paragraph': Paragraph.from_fragments,
        'h1': Heading1.from_fragments,
        'h2': Heading2.from_fragments,
        'h3': Heading3.from_fragments,
        'h4': Heading4.from_fragments,
        'h5': Heading5.from_fragments,
        'h6': Heading6.from_fragments,
        'bold': Bold.from_fragments,
        'italic': Italic.from_fragments,
        'uline': Underline.from_fragments,
        'code': Code.from_fragments,
        'blockquote': Blockquote.from_fragments,
        'link': Link.from_fragments,
        'image': Image,
        'numbered_list': NumberedList.from_direct_args,
        'bulleted_list': BulletedList.from_direct_args,
        'table': Table.from_direct_args,
        'table_header': TableHeader.from_direct_args,
        'table_row': TableRow.from_direct_args,
        'hrule': horizontal_rule,
        'line_break': line_break,
        '\\': line_break,
        'nbsp': non_breaking_space,
        '%': non_breaking_space,
        'hairsp': hair_space,
        '.': hair_space,
        'thinsp': thin_space,
        ',': thin_space,
        **data,
    })
