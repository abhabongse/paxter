"""
Collections of utility functions to process fragment lists.
"""
from __future__ import annotations

import re
from collections.abc import Sequence
from typing import Union

from paxter.exceptions import PaxterRenderError
from paxter.interpreting.data import FragmentList

PARAGRAPH_SPLIT_RE = re.compile(r'\n(?:[ \t\r\f\v]*\n)+')


def split_into_paragraphs(fragments: Union[str, FragmentList]) -> list[FragmentList]:
    """
    Splits a given fragment list into a list of multiple paragraphs
    where each paragraph is a fragment list.
    """
    # Special case: when the input fragment list is just a string,
    # we treat them as a single element in one paragraph.
    if isinstance(fragments, str):
        return [FragmentList([fragments])]
    if not isinstance(fragments, FragmentList):
        raise PaxterRenderError("expected a string or a fragment list")

    # Clean up fragment list by merging consecutive strings
    # and trimming whitespaces
    fragments = _strip_paragraph(_merge_strings(fragments))

    # Iterate through each fragment and arrange them
    # into a list of paragraphs.
    paragraphs = []
    para = []  # list of elements
    for piece in fragments:
        if isinstance(piece, str):
            particles = PARAGRAPH_SPLIT_RE.split(piece)
            if len(particles) >= 2:
                if particles[0].strip():
                    para.append(particles[0])
                paragraphs.append(para)
                for p in particles[1:-1]:
                    paragraphs.append([p])
                para = []
                if particles[-1].strip():
                    para.append(particles[-1])
            else:
                para.append(piece)
        else:
            para.append(piece)
    if para:
        paragraphs.append(para)

    # Clean up each paragraph by stripping
    paragraphs = [
        _strip_paragraph(paragraph)
        for paragraph in paragraphs
    ]
    return paragraphs


def _merge_strings(fragments: FragmentList) -> list:
    """
    Merge consecutive strings in fragment list into one string.
    """
    # First pass: group consecutive strings together
    groups = []
    for frag in fragments.flatten():
        if isinstance(frag, str):
            if groups and isinstance(groups[-1], FragmentList):
                groups[-1].append(frag)
            else:
                groups.append(FragmentList([frag]))
        else:
            groups.append(frag)
    # Second pass: merge each group consecutive strings into one string
    fragments = []
    for grp in groups:
        if isinstance(grp, FragmentList):
            fragments.append(''.join(grp))
        else:
            fragments.append(grp)
    return fragments


def _strip_paragraph(paragraph: Sequence) -> FragmentList:
    """
    Trim whitespaces before and after the paragraph.
    """
    paragraph = list(paragraph)  # make copy
    # Left-strip first paragraph
    if paragraph and isinstance(paragraph[0], str):
        paragraph[0] = paragraph[0].lstrip()
        if not paragraph[0]:
            paragraph = paragraph[1:]
    # Right-strip last paragraph
    if paragraph and isinstance(paragraph[-1], str):
        paragraph[-1] = paragraph[-1].rstrip()
        if not paragraph[-1]:
            paragraph = paragraph[:-1]
    return FragmentList(paragraph)
