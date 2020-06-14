"""
Collection of standard functions for Python authoring mode.
"""
import inspect
from typing import Any, Iterator, List, TYPE_CHECKING, Union

from paxter.core import Command, Text
from paxter.core.exceptions import PaxterRenderError
from paxter.pyauthor.wrappers import DirectApply

if TYPE_CHECKING:
    from paxter.pyauthor.visitor import RenderContext


@DirectApply
def python_unsafe_exec(context: 'RenderContext', node: Command):
    """
    Unsafely executes pyauthor code within the main argument.
    """
    if node.options:
        raise PaxterRenderError("expected empty options section")
    if not isinstance(node.main_arg, Text):
        raise PaxterRenderError("expected raw text")
    code = inspect.cleandoc(node.main_arg.inner)
    exec(code, context.env)


def intro_unsafe_eval(phrase: str, env: dict) -> Any:
    """
    Unsafely evaluates the given paxter phrase.
    However, if the phrase is within the _symbols_ mappings,
    its mapped value will be returned instead.
    """
    if phrase in env:
        return env[phrase]
    symbols = env.get('_symbols_', {})
    if phrase in symbols:
        return symbols[phrase]
    return eval(phrase, env)


def flatten(data, is_joined: bool = True) -> Union[List[str], str]:
    """
    Flattens the nested list of elements by unrolling them into a single list.
    Unless the ``is_joined`` option is disabled,
    all elements will be combined to a single string.

    >>> flatten(["Hello", ",", " ", "World", "!"])
    "Hello, World!"
    >>> flatten(["Hello", [",", " "], ["World"], "!"])
    "Hello, World!"
    >>> flatten(["Hello", [",", " "], ["World"], "!"], is_joined=False)
    ["Hello", ",", " ", "World", "!"]
    >>> flatten("Hello, World!")
    "Hello, World!"
    >>> flatten("Hello, World!", is_joined=False)
    ["Hello, World!"]
    """
    seq = _rec_flatten_tokenize(data)
    if is_joined:
        return ''.join(str(element) for element in seq)
    else:
        return list(seq)


def _rec_flatten_tokenize(data) -> Iterator:
    if isinstance(data, list):
        for element in data:
            yield from _rec_flatten_tokenize(element)
    else:
        yield data
