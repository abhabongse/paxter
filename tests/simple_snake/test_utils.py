import ast

import pytest

from paxter.core import Parser
from paxter.flavors.simple_snake import (
    DefinitionSet, SimpleSnakeTransformer, with_env, with_node,
)


@pytest.mark.parametrize(
    ("env", "input_text", "expected"),
    [
        ({'x': 1, 'y': 2}, ' x  ', 1),
        ({'x': 1, 'y': 2}, '  y ', 2),
    ],
)
def test_with_env_call_func(env, input_text, expected):
    @with_env
    def hello(_env, _input_text):
        return _env[_input_text.strip()]

    assert hello(env, input_text) == expected


def test_with_env_with_node():
    parser = Parser()
    env_set = DefinitionSet()

    @env_set.register(name='set_literal!')
    @with_node
    def set_literal(_, env, node):
        id = node.options[0].get_faux_key()
        value = ast.literal_eval(node.text.string)
        env[id] = value
        return ''

    @env_set.register
    @with_env
    def set_black(env, main_text):
        env['black'] = main_text
        return ''

    input_text = """\
    @set_literal![white]{"a"}
    @set_black{@"x"y@"z"}
    """

    tree = parser.parse(input_text)
    transformer = SimpleSnakeTransformer(env_set.get_copy())
    final_env, _ = transformer.transform({}, tree)
    assert final_env['white'] == "a"
    assert final_env['black'] == "xyz"
