"""
Collection of standard functions for Python authoring mode.
"""
import inspect
from typing import Any, TYPE_CHECKING

from paxter.evaluator import DirectApply
from paxter.exceptions import PaxterRenderError
from paxter.parser import Command, Text

if TYPE_CHECKING:
    from paxter.evaluator.context import EvaluateContext


@DirectApply
def python_unsafe_exec(context: 'EvaluateContext', node: Command):
    """
    Unsafely executes pyauthor code within the main argument.
    """
    if node.option:
        raise PaxterRenderError("expected empty option section")
    if not isinstance(node.main_arg, Text):
        raise PaxterRenderError("expected raw text")
    code = inspect.cleandoc(node.main_arg.inner)
    exec(code, context.env)


def phrase_unsafe_eval(phrase: str, env: dict) -> Any:
    """
    Unsafely evaluates the given phrase of a command.
    If the input phrase is a valid python identifier,
    the env dict lookup using phrase as the key will be performed.
    Otherwise, the dict lookup with be done on the value of ``env['_others_']``.
    As a fallback when dict lookup was failed (key is missing),
    python's eval() built-in function will be invoked.
    """
    if phrase.isidentifier():
        source = env
    else:
        source = env.get('_others_', {})
    if phrase in source:
        return source[phrase]
    return eval(phrase, env)


def verbatim(text: Any) -> str:
    """
    Returns the main string argument as-is.
    It produces a TypeError if input text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("argument to verbatim must be string")
    return text
