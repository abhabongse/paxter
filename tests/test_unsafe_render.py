import os
from typing import Tuple

import pytest
from click.testing import CliRunner

from paxter.core.parser import ParseContext
from paxter.pyauthor import RenderContext, create_unsafe_env
from paxter.pyauthor.funcs import flatten

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unsafe")


def get_test_files(stem: str) -> Tuple[str, str]:
    input_file = os.path.join(DATA_DIR, f"{stem}.paxter")
    expected_file = os.path.join(DATA_DIR, f"{stem}.expected")
    return pytest.param(input_file, expected_file, id=stem)


TESTS = [
    get_test_files("calls"),
    get_test_files("delimiters"),
    get_test_files("greetings"),
    get_test_files("lookup_and_call"),
    get_test_files("loops_and_conds"),
    get_test_files("phrase_symbols"),
]


@pytest.mark.parametrize(("input_file", "expected_file"), TESTS)
def test_rendering(input_file, expected_file):

    # Read test file contents
    with open(input_file) as fobj:
        input_text = fobj.read()
    with open(expected_file) as fobj:
        expected_text = fobj.read()

    # Parse input
    tree = ParseContext(input_text).tree

    # Render into output using python authoring mode
    env = create_unsafe_env()
    output = RenderContext(input_text, env, tree).rendered
    output_text = flatten(output)

    assert output_text == expected_text


@pytest.mark.parametrize(("input_file", "expected_file"), TESTS)
def test_cli_render(input_file, expected_file):
    from paxter.__main__ import program

    with open(expected_file) as fobj:
        expected_text = fobj.read()

    runner = CliRunner()
    result = runner.invoke(program, ['pyauthor', '-i', input_file])
    assert result.output == expected_text
