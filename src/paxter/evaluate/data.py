"""
Data definitions for the result type of evaluation.
"""
from collections import UserList
from typing import MutableSequence, TypeVar

T = TypeVar('T')


class FragmentList(UserList, MutableSequence[T]):
    """
    Special subclass of built-in list class
    to store a list of fragments.
    """

    def __repr__(self):
        content = super().__repr__()
        return f"FragmentList({content})"

    def flatten(self):
        """
        Flattens out the members of fragment list
        but without nested fragment list.
        """
        if isinstance(self, FragmentList):
            for element in self:
                yield from FragmentList.flatten(element)
        else:
            yield self
