"""
A collection of pre-defined execution environment.
"""
from typing import Optional

from paxter.pyauthor.funcs import (
    flatten, for_statement, if_statement, starter_unsafe_eval,
    python_unsafe_exec, verbatim,
)


def create_unsafe_env(data: Optional[dict] = None):
    """
    Creates an unsafe environment data for Paxter source code evaluation
    in Python authoring mode.
    """
    data = data or {}
    return {
        '_starter_eval_': starter_unsafe_eval,
        'for': for_statement,
        'if': if_statement,
        'python': python_unsafe_exec,
        'verb': verbatim,
        'flatten': flatten,
        **data,
    }


def create_unsafe_html_env(data: Optional[dict] = None):
    """
    Creates an unsafe environment data for Paxter source code evaluation
    in Python authoring mode, specializes in construction HTML tree.
    """
    ...
