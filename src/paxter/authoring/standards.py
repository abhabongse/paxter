"""
Collection of standard functions for Python authoring mode.
"""
import inspect
from typing import Any, Iterator, List, TYPE_CHECKING, Union

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


def starter_unsafe_eval(starter: str, env: dict) -> Any:
    """
    Unsafely evaluates the given paxter phrase.
    """
    if starter in env:
        return env[starter]
    return eval(starter, env)


def verbatim(text: Any) -> str:
    """
    Returns the main string argument as-is.

    >>> verbatim("Hello")
    "Hello"
    >>> verbatim("me@example.com")
    "me@example.com"
    """
    if not isinstance(text, str):
        raise TypeError("argument to verbatim must be string")
    return text


def flatten(data, join: bool = False) -> Union[List[str], str]:
    """
    Flattens the nested list of elements by unrolling them into a single list.
    Unless the ``is_joined`` option is disabled,
    all elements will be combined to a single string.

    >>> flatten(["Hello", ",", " ", "World", "!"], join=True)
    "Hello, World!"
    >>> flatten(["Hello", [",", " "], ["World"], "!"], join=True)
    "Hello, World!"
    >>> flatten(["Hello", [",", " "], ["World"], "!"])
    ["Hello", ",", " ", "World", "!"]
    >>> flatten("Hello, World!", join=True)
    "Hello, World!"
    >>> flatten("Hello, World!")
    ["Hello, World!"]
    """
    seq = _rec_flatten_tokenize(data)
    if join:
        return ''.join(str(element) for element in seq)
    else:
        return list(seq)


def _rec_flatten_tokenize(data) -> Iterator:
    if isinstance(data, list):
        for element in data:
            yield from _rec_flatten_tokenize(element)
    else:
        yield data
