"""
A collection of Paxter common functions.
"""
from __future__ import annotations

from typing import Optional

from paxter.author.elements import Document
from paxter.author.environ import create_document_env, create_simple_env
from paxter.interpret import FragmentList
from paxter.interpret.context import InterpreterContext
from paxter.parsing import parse


def run_simple_paxter(src_text: str, env: Optional[dict] = None) -> FragmentList:
    """
    Parses the input source text written in Paxter language
    and evaluates it using standard python environment.
    This function returns the result of evaluation
    and may modify the given environment in-place as well.
    """
    parsed_tree = parse(src_text)
    env = env or create_simple_env()
    evaluate_context = InterpreterContext(src_text, env, parsed_tree)
    return evaluate_context.rendered


def run_document_paxter(src_text: str, env: Optional[dict] = None) -> Document:
    """
    Similar to run_simple_paxter,
    but uses specialized environment suitable for writing documents.
    The result is wrapped under Document data class.
    """
    parsed_tree = parse(src_text)
    env = env or create_document_env()
    evaluate_context = InterpreterContext(src_text, env, parsed_tree)
    return Document.from_fragments(evaluate_context.rendered)
