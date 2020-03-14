"""
Utility decorators and classes.
"""

import functools
from typing import Any, Callable, Dict, Optional, TYPE_CHECKING

from paxter.core import Node

if TYPE_CHECKING:
    from paxter.flavors.simple_snake._transformer import SimpleSnakeTransformer


class with_env:
    """
    Decorator which allows the attached function to accept
    the environment dict as the very first argument
    before all other usual arguments in @-expressions macro or function
    like `paxter.core.data.PaxterMacro` or `paxter.core.data.PaxterFunc`.
    """

    def __init__(self, wrapped: Callable):
        self.__wrapped__ = wrapped

    def get_callable(self, env: dict):
        @functools.wraps(self.__wrapped__)
        def func(*args, **kwargs):
            return self.__wrapped__(env, *args, **kwargs)

        return func

    def __call__(self, *args, **kwargs):
        return self.__wrapped__(*args, **kwargs)


class with_node:
    """
    Decorator which allows the attached function to accept
    the transformer instance, the environment dict,
    and the node data as the three arguments into macro or function
    like `paxter.core.data.PaxterMacro` or `paxter.core.data.PaxterFunc`.
    """

    def __init__(self, wrapped: Callable):
        self.__wrapped__ = wrapped

    def call(self, transformer: 'SimpleSnakeTransformer', env: dict, node: Node):
        """
        Make a call to wrapped function with provided input arguments.
        """
        return self.__wrapped__(transformer, env, node)

    def __call__(self, transformer: 'SimpleSnakeTransformer', env: dict, node: Node):
        return self.call(transformer, env, node)


class DefinitionSet:
    """
    Helper class to gather functions and values to a dictionary.
    """
    data: Dict[str, Any]

    def __init__(self, data: Optional[Dict[str, Any]] = None):
        self.data = data or {}

    def register(
            self, value_or_func: Optional[Any] = None, *,
            name: Optional[str] = None,
    ):
        """
        Decorator which registers the given value or function
        to the data dictionary.
        """
        if value_or_func is None:
            return functools.partial(self.register, name=name)
        name = name or value_or_func.__name__
        self.data[name] = value_or_func
        return value_or_func

    def get_copy(self):
        """
        Obtains a copy of data dict.
        """
        return self.data.copy()
