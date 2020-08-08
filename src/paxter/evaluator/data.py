"""
Data definitions for the result type of evaluation.
"""
from typing import MutableSequence, TypeVar

T = TypeVar('T')


class FragmentList(list, MutableSequence[T]):
    """
    Special subclass of built-in list class
    to store a list of fragments.
    """

    def __repr__(self):
        content = super().__repr__()
        return f"FragmentList({content})"
