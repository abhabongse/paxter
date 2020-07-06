"""
Collection of functions to be used within the Python authoring mode.
"""
from paxter.pyauthor.funcs.controls import for_statement, if_statement
from paxter.pyauthor.funcs.standards import (
    flatten, python_unsafe_exec, starter_unsafe_eval, verb,
)

__all__ = [
    'for_statement', 'if_statement',
    'flatten', 'python_unsafe_exec', 'starter_unsafe_eval', 'verb',
]
