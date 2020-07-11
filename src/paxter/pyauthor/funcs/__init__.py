"""
Collection of functions to be used within the Python authoring mode.
"""
from paxter.pyauthor.funcs.controls import for_statement, if_statement
from paxter.pyauthor.funcs.document import H1
from paxter.pyauthor.funcs.standards import (
    flatten, python_unsafe_exec, starter_unsafe_eval, verb,
)

__all__ = [
    'for_statement', 'if_statement',
    'H1',
    'flatten', 'python_unsafe_exec', 'starter_unsafe_eval', 'verb',
]
