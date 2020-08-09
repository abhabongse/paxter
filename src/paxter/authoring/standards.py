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


def phrase_unsafe_eval(phrase: str, env: dict) -> Any:
    """
    Unsafely evaluates the given phrase of a command.
    If performs the evaluation in the following order.

    1. Looks up the value from ``env['_extras_']`` dict using phrase as key
    2. Looks up the value from ``env`` dict using phrase as key
    3. Invokes the built-in function :func:`eval`.
    """
    extras = env.get('_extras_', {})
    if phrase in extras:
        return extras[phrase]
    if phrase in env:
        return env[phrase]
    return eval(phrase, env)


@DirectApply
def python_unsafe_exec(context: 'EvaluateContext', node: Command):
    """
    Unsafely executes the given python code
    using env dict as the namespace.
    """
    if node.options:
        raise PaxterRenderError("expected empty options section")
    if not isinstance(node.main_arg, Text):
        raise PaxterRenderError("expected raw text")
    code = inspect.cleandoc(node.main_arg.inner)
    exec(code, context.env)


def verbatim(text: Any) -> str:
    """
    Returns the main string argument as-is.
    It produces a TypeError if input text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("argument to verbatim must be string")
    return text
