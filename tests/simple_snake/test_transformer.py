import pytest
from click.testing import CliRunner

from paxter.commands import program
from paxter.core import Parser
from paxter.flavors import SimpleSnakeTransformer
from tests.simple_snake.loader import all_test_cases


@pytest.mark.parametrize(
    ("env_file", "input_text_file", "expected_file"), all_test_cases,
)
def test_program(env_file, input_text_file, expected_file):
    runner = CliRunner()
    command = ['simple-snake', '-i', input_text_file]
    if env_file:
        command.extend(['-e', env_file])
    result = runner.invoke(program, command)
    assert result.exit_code == 0
    with open(expected_file) as fobj:
        expected_output = fobj.read()
    assert result.output == expected_output


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
