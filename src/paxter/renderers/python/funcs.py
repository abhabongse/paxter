"""
Collection of `PaxterApply` function wrappers.
"""
import inspect
from typing import Any, Iterator, TYPE_CHECKING

from paxter.core import CharLoc, Command, FragmentList, Identifier, Text
from paxter.core.exceptions import PaxterRenderError
from paxter.renderers.python.wrappers import DirectApply

if TYPE_CHECKING:
    from paxter.renderers.python.visitor import RenderContext


@DirectApply
def for_statement(context: 'RenderContext', node: Command):
    """
    Simulates simple for loops.
    """

    def raise_error(message):
        raise PaxterRenderError(
            f"{message} in for statement at %(pos)s",
            pos=CharLoc(context.input_text, node.options.start_pos),
        )

    if not (node.options
            and len(node.options.children) >= 1
            and isinstance(node.options.children[0], Identifier)):
        raise_error("expected binding identifier declaration")
    if not (len(node.options.children) >= 2
            and node.options.children[1] == Identifier.without_pos(name='in')):
        raise_error("expected keyword 'in'")
    if len(node.options.children) < 3:
        raise_error("expected iterable clause")
    if len(node.options.children) > 3:
        raise_error("unexpected extra token")
    if node.main_arg is None:
        raise_error("expected main argument body")

    # Obtain sequence
    id_name = node.options.children[0].name
    seq = context.transform_token(node.options.children[2])

    result = []
    for value in seq:
        context.env[id_name] = value
        rendered = context.transform_token(node.main_arg)
        if isinstance(node.main_arg, FragmentList):
            result.extend(rendered)
        else:
            result.append(rendered)

    return result


@DirectApply
def if_statement(context: 'RenderContext', node: Command):  # noqa: C901
    """
    Simulates simple if statement.
    """

    def raise_error(message):
        raise PaxterRenderError(
            f"{message} in if statement at %(pos)s",
            pos=CharLoc(context.input_text, node.options.start_pos),
        )

    target_bool = True
    cond_node = None
    then_node = None
    else_node = None

    if not (node.options and len(node.options.children) >= 1):
        raise_error("expected condition clause")
    if len(node.options.children) == 1:
        if node.main_arg is None:
            raise_error("expected main argument body")
        cond_node = node.options.children[0]
        then_node = node.main_arg
    elif len(node.options.children) == 2:
        if node.options.children[0] != Identifier.without_pos(name='not'):
            raise_error("expected first token to be 'not'")
        if node.main_arg is None:
            raise_error("expected main argument body")
        target_bool = False
        cond_node = node.options.children[1]
        then_node = node.main_arg
    elif len(node.options.children) == 5:
        if node.options.children[1] != Identifier.without_pos(name='then'):
            raise_error("expected keyword 'then'")
        if node.options.children[3] != Identifier.without_pos(name='else'):
            raise_error("expected keyword 'else'")
        if node.main_arg:
            raise_error("unexpected main argument body")
        cond_node = node.options.children[0]
        then_node = node.options.children[2]
        else_node = node.options.children[4]
    else:
        raise_error("ill-formed sequence of tokens")

    # Evaluate conditional clause
    cond = context.transform_token(cond_node)
    if callable(cond):
        cond = cond()

    # Choose and evaluate result clause
    result_node = then_node if bool(cond) is target_bool else else_node
    if result_node is None:
        return
    return context.transform_token(result_node)


@DirectApply
def python_unsafe_exec(context: 'RenderContext', node: Command):
    """
    Unsafely executes python code within the main argument.
    """
    if node.options:
        raise PaxterRenderError("expected empty options section")
    if not isinstance(node.main_arg, Text):
        raise PaxterRenderError("expected raw text")
    code = inspect.cleandoc(node.main_arg.inner)
    exec(code, context.env)


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


def flatten(data, recursive=False) -> str:
    """
    Flattens the list and join them together into one string.
    """
    if isinstance(data, list):
        if recursive:
            data = _rec_flatten_tokenize(data)
        return ''.join(
            str(value) for value in data
            if value is not None
        )
    return str(data)


def _rec_flatten_tokenize(data) -> Iterator:
    """
    Flattens the nested lists.
    """
    if isinstance(data, list):
        for element in data:
            yield from _rec_flatten_tokenize(element)
    else:
        yield data
