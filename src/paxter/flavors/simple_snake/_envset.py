import functools
from typing import Any, Callable, Dict, Optional


class EnvironSet:
    """
    Helper class to gather an environment dictionary.
    """
    env: Dict[str, Any]

    def __init__(self, start_env: Optional[Dict[str, Any]] = None):
        self.env = start_env or {}

    # TODO: make register_func and register_macro accept env boolean option;
    #       if true, then the attached function will env argument
    #       before the main text argument (or do other solutions)

    def register(
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
            return functools.partial(self.register, name=name)
        name = name or func.__name__
        self.env[name] = func
        return func
