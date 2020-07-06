"""
Collection of functions to be used within the Python authoring mode.
"""
from paxter.pyauthor.funcs.controls import for_statement, if_statement
from paxter.pyauthor.funcs.standards import (
    flatten, starter_unsafe_eval, python_unsafe_exec, verbatim,
)

__all__ = [
    'for_statement', 'if_statement',
    'flatten', 'starter_unsafe_eval', 'python_unsafe_exec', 'verbatim',
]
