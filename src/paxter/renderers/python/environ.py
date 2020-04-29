"""
A collection of pre-defined execution environment.
"""
from typing import Optional

from paxter.renderers.python.funcs import (
    flatten, for_statement, if_statement, phrase_unsafe_eval, python_unsafe_exec,
)


def create_unsafe_env(data: Optional[dict] = None):
    data = data or {}
    return {
        '_phrase_eval_': phrase_unsafe_eval,
        'for': for_statement,
        'if': if_statement,
        'python': python_unsafe_exec,
        'flatten': flatten,
        **data,
    }
