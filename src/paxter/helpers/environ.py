"""
Environment dict builder class.
"""
import functools
from typing import Any, Callable, Dict, Optional


class Environ:
    """
    Environment dict builder class.
    """
    env: Dict[str, Any]

    def __init__(self, starting_env: Optional[Dict[str, Any]] = None):
        self.env = starting_env or {}

    def register_func(
            self, func: Optional[Callable] = None, *,
            name: Optional[str] = None,
    ):
        """
        Decorator which registers the attached function
        to the environment as a PaxterFunc.
        It will receive exactly one positional argument (as the main text)
        and zero or more optional keyword arguments.
        """
        if func is None:
            return functools.partial(self.register_func, name=name)
        name = name or func.__name__
        self.env[name] = func
        return func

    def register_macro(
            self, func: Optional[Callable] = None, *,
            name: Optional[str] = None,
    ):
        """
        Decorator which registers the attached function
        to the environment as a PaxterMacro.
        It will receive exactly two positional arguments:
        the environment dict and the main text.
        """
        if func is None:
            return functools.partial(self.register_macro, name=name)
        name = name or f'{func.__name__}!'
        self.env[name] = func
        return func

    def clone_and_adapt(self, outside_env: Dict[str, Any]) -> Dict[str, Any]:
        """
        Makes a clone of the stored environment dict
        and extend it with the given outside environment dict.
        """
        return {**self.env, **outside_env}
