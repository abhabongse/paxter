"""
Data definitions for the result type of evaluation.
"""
from collections import UserList
from typing import MutableSequence, TypeVar

T = TypeVar('T')


class Fragments(UserList, MutableSequence[T]):
    """
    Special subclass of built-in list class
    to store a list of fragments.
    """

    def __repr__(self):
        content = super().__repr__()
        return f"Fragments({content})"

    def flatten(self):
        """
        Flattens out the members of fragment list
        but without nested fragment list.
        """
        return Fragments(Fragments.__flatten_tokenize(self))

    @staticmethod
    def __flatten_tokenize(data):
        if isinstance(data, Fragments):
            for element in data:
                yield from Fragments.__flatten_tokenize(element)
        else:
            yield data
