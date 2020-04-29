"""
Collection of `PaxterApply` function wrappers.
"""
import inspect
from typing import Any, Iterator, TYPE_CHECKING

from paxter.core import PaxterApply, Text
from paxter.core.exceptions import PaxterRenderError
from paxter.renderers.python.wrappers import DirectApply

if TYPE_CHECKING:
    from paxter.renderers.python.visitor import RenderContext


@DirectApply
def for_statement(context: 'RenderContext', node: PaxterApply):
    """
    Simulates simple for loops.
    """
    # TODO: implement this
    raise NotImplementedError


@DirectApply
def if_statement(context: 'RenderContext', node: PaxterApply):
    """
    Simulates simple if statement.
    """
    # TODO: implement this
    raise NotImplementedError


@DirectApply
def python_unsafe_exec(context: 'RenderContext', node: PaxterApply):
    """
    Unsafely executes python code within the main argument.
    """
    if node.options:
        raise PaxterRenderError("expected empty options section")
    if not isinstance(node.main_arg, Text):
        raise PaxterRenderError("expected raw text")
    code = inspect.cleandoc(node.main_arg.inner)
    exec(code, context.env)
    return ''


def phrase_unsafe_eval(phrase: str, env: dict) -> Any:
    """
    Unsafely evaluates the given paxter phrase.
    However, if the phrase is within the _symbols_ mappings,
    its mapped value will be returned instead.
    """
    symbols = env.get('_symbols_', {})
    if phrase in symbols:
        return symbols[phrase]
    return eval(phrase, env)


def flatten(data) -> str:
    """
    Flattens the nested lists and join them together into one string.
    """
    return ''.join(str(value) for value in _flatten_tokenize(data))


def _flatten_tokenize(data) -> Iterator:
    """
    Flattens the nested lists.
    """
    if isinstance(data, list):
        for element in data:
            yield from _flatten_tokenize(element)
    else:
        yield data
