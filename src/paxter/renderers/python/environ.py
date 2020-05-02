"""
A collection of pre-defined execution environment.
"""
from typing import Optional

from paxter.renderers.python.funcs import (
    flatten, for_statement, if_statement,
    phrase_sandbox_eval, phrase_unsafe_eval,
    python_sandbox_exec, python_unsafe_exec,
)


def create_sandbox_env(data: Optional[dict] = None):
    """
    Creates a sandboxed environment data
    for Paxter source code evaluation in Python authoring mode.
    """
    from RestrictedPython import limited_builtins, safe_builtins, utility_builtins
    from RestrictedPython.Guards import full_write_guard
    from RestrictedPython.PrintCollector import PrintCollector

    data = data or {}
    builtins = {**safe_builtins, **limited_builtins, **utility_builtins}
    return {
        '__builtins__': builtins,
        '_write_': full_write_guard,
        '_getattr_': getattr,
        '_print_': PrintCollector,
        '_phrase_eval_': phrase_sandbox_eval,
        'for': for_statement,
        'if': if_statement,
        'python': python_sandbox_exec,
        'flatten': flatten,
        **data,
    }


def create_unsafe_env(data: Optional[dict] = None):
    """
    Creates an unsafe environment data
    for Paxter source code evaluation in Python authoring mode.
    """
    data = data or {}
    return {
        '_phrase_eval_': phrase_unsafe_eval,
        'for': for_statement,
        'if': if_statement,
        'python': python_unsafe_exec,
        'flatten': flatten,
        **data,
    }
