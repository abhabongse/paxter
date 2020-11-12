from __future__ import annotations

import os
from typing import Tuple

import pytest
from click.testing import CliRunner

from paxter.author import create_document_env
from paxter.author.elements import Document
from paxter.interpret import InterpreterContext
from paxter.parsing import parse

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "document")


def get_test_files(stem: str) -> Tuple[str, str]:
    input_file = os.path.join(DATA_DIR, f"{stem}.paxter")
    expected_file = os.path.join(DATA_DIR, f"{stem}.expected")
    return pytest.param(input_file, expected_file, id=stem)


TESTS = [
    get_test_files("blog"),
    get_test_files("table"),
]


@pytest.mark.parametrize(("src_file", "expected_file"), TESTS)
def test_evaluator_document(src_file, expected_file):
    with open(src_file) as fobj:
        input_text = fobj.read()
    with open(expected_file) as fobj:
        expected_text = fobj.read()

    # Parse input
    parsed_tree = parse(input_text)

    # Render into output HTML
    env = create_document_env()
    evaluate_context = InterpreterContext(input_text, env, parsed_tree)
    document = Document.from_fragments(evaluate_context.rendered)

    assert document.html() == expected_text


@pytest.mark.parametrize(("src_file", "expected_file"), TESTS)
def test_cli_document(src_file, expected_file):
    from paxter.__main__ import program

    with open(expected_file) as fobj:
        expected_text = fobj.read()

    runner = CliRunner()
    result = runner.invoke(program, ['html', '-i', src_file])
    assert result.output == expected_text + '\n'
