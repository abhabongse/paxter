"""
A collection of pre-defined execution environment.
"""
from typing import Optional

from paxter.renderers.unsafe.funcs import flatten, flatten_and_join, phrase_eval, \
    python_exec


def create_env(data: Optional[dict] = None):
    data = data or {}
    return {
        '_phrase_eval_': phrase_eval,
        'python': python_exec,
        'flatten': flatten,
        'flatten_and_join': flatten_and_join,
        **data,
    }
