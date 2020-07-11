"""
A collection of pre-defined execution environment.
"""
from typing import Optional

from paxter.pyauthor.funcs import (
    flatten, for_statement, H1, if_statement,
    python_unsafe_exec, starter_unsafe_eval, verb,
)


def create_unsafe_bare_env(data: Optional[dict] = None):
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
        'verb': verb,
        'flatten': flatten,
        **data,
    }


def create_unsafe_document_env(data: Optional[dict] = None):
    """
    Creates an unsafe environment data for Paxter source code evaluation
    in Python authoring mode, specializes in constructing documents.
    """
    return {
        '_starter_eval_': starter_unsafe_eval,
        'for': for_statement,
        'if': if_statement,
        'python': python_unsafe_exec,
        'verb': verb,
        'flatten': flatten,
        'h1': H1,
        **data,
    }
