"""
Collection of standard functions for Python authoring mode.
"""
import inspect
from typing import Any, Iterator, TYPE_CHECKING

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


def flatten(data, keep_levels: int = 0) -> Any:
    """
    Flattens the nested lists by unrolling them
    but keep the first few specified number of levels.
    """
    if not isinstance(data, list):
        return data
    if keep_levels >= 1:
        return [
            flatten(element, keep_levels - 1)
            for element in data
        ]
    return ''.join(
        str(element) for element in _rec_flatten_tokenize(data)
        if element is not None
    )


def _rec_flatten_tokenize(data) -> Iterator:
    if isinstance(data, list):
        for element in data:
            yield from _rec_flatten_tokenize(element)
    else:
        yield data
