import os
from typing import Tuple

import pytest
from click.testing import CliRunner

from paxter.authoring import create_document_env
from paxter.authoring.document import Document
from paxter.evaluator import EvaluateContext
from paxter.parser import (
    ParseContext,
)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "document")


def get_test_files(stem: str) -> Tuple[str, str]:
    input_file = os.path.join(DATA_DIR, f"{stem}.paxter")
    expected_file = os.path.join(DATA_DIR, f"{stem}.expected")
    return pytest.param(input_file, expected_file, id=stem)


TESTS = [
    get_test_files("blog"),
]


@pytest.mark.parametrize(("input_file", "expected_file"), TESTS)
def test_evaluator_document(input_file, expected_file):
    with open(input_file) as fobj:
        input_text = fobj.read()
    with open(expected_file) as fobj:
        expected_text = fobj.read()

    # Parse input
    parse_context = ParseContext(input_text)

    # Render into output HTML
    env = create_document_env()
    evaluate_context = EvaluateContext(input_text, env, parse_context.tree)
    document = Document(evaluate_context.rendered)

    assert document.html() == expected_text


@pytest.mark.parametrize(("input_file", "expected_file"), TESTS)
def test_cli_document(input_file, expected_file):
    from paxter.__main__ import program

    with open(expected_file) as fobj:
        expected_text = fobj.read()

    runner = CliRunner()
    result = runner.invoke(program, ['html', '-i', input_file])
    assert result.output == expected_text + '\n'
