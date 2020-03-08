"""
Standard collection of useful transformers in various contexts.
"""
from paxter.standard.simple_python import SimplePythonTransformer

__all__ = ['SimplePythonTransformer']

# Disable all docstrings for classes and functions at this level
__pdoc__ = {item: False for item in __all__}
