import os
import runpy

import pytest

from paxter.core import Parser
from paxter.flavors import SimpleSnakeTransformer

this_dir = os.path.dirname(os.path.abspath(__file__))


def load_test_set(file_prefix):
    input_text_file = os.path.join(this_dir, f"{file_prefix}.in")
    with open(input_text_file) as fobj:
        input_text = fobj.read()

    expected_file = os.path.join(this_dir, f"{file_prefix}.expected")
    with open(expected_file) as fobj:
        expected = fobj.read()

    env_file = os.path.join(this_dir, f"{file_prefix}.py")
    if os.path.isfile(env_file):
        with open(env_file) as fobj:
            env = runpy.run_path(env_file)
    else:
        env = {}

    return pytest.param(env, input_text, expected, id=file_prefix)


@pytest.mark.parametrize(
    ("environment", "input_text", "expected"),
    [
        load_test_set('fst'),
        load_test_set('snd'),
        load_test_set('trd'),
        load_test_set('greetings'),
        load_test_set('loops_and_conds'),
    ],
)
def test_simple_python_transformer(environment, input_text, expected):
    parser = Parser()
    transformer = SimpleSnakeTransformer()
    tree = parser.parse(input_text)
    _, output_text = transformer.transform(environment, tree)
    assert output_text == expected


def test_environment_change():
    parser = Parser()
    transformer = SimpleSnakeTransformer()

    input_env = {'value': 100}
    input_text = """\
@!##{
import itertools

value += 99
counter = itertools.count(start=1)
}##

Hello, World!

@!{a = next(counter)}
@!{b = next(counter)}
@!{c = a + b + next(counter)}
    """
    tree = parser.parse(input_text)
    output_env, _ = transformer.transform(input_env, tree)

    assert output_env['value'] == 199
    assert output_env['a'] == 1
    assert output_env['b'] == 2
    assert output_env['c'] == 6
    assert next(output_env['counter']) == 4
