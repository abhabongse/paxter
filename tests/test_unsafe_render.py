import os
from typing import Tuple

import pytest

from paxter.core.parser import ParseContext
from paxter.renderers.python import RenderContext, create_unsafe_env

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unsafe")


def get_test_pair(stem: str) -> Tuple[str, str]:
    input_file = os.path.join(DATA_DIR, f"{stem}.paxter")
    expected_file = os.path.join(DATA_DIR, f"{stem}.expected")
    with open(input_file) as fobj:
        input_text = fobj.read()
    with open(expected_file) as fobj:
        expected_text = fobj.read()
    return pytest.param(input_text, expected_text, id=stem)


@pytest.mark.parametrize(
    ("input_text", "expected_text"),
    [
        get_test_pair("calls"),
        get_test_pair("delimiters"),
        get_test_pair("greetings"),
        get_test_pair("loops_and_conds"),
    ],
)
def test_rendering(input_text, expected_text):
    tree = ParseContext(input_text).parse()
    env = create_unsafe_env()
    output_text = RenderContext(input_text, env).visit(tree)
    assert output_text == expected_text
