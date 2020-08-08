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
        return FragmentList(FragmentList.__flatten_tokenize(self))

    @staticmethod
    def __flatten_tokenize(data):
        if isinstance(data, FragmentList):
            for element in data:
                yield from FragmentList.__flatten_tokenize(element)
        else:
            yield data
