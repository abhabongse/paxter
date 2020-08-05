"""
A collection of Paxter common functions.
"""
from typing import Any, Optional

from paxter.authoring.document import Document
from paxter.authoring.environ import create_document_env, create_simple_env
from paxter.evaluator.context import EvaluateContext
from paxter.parser import ParseContext


def run_simple_paxter(input_text: str, env: Optional[dict] = None) -> Any:
    """
    Parses the input source text written in Paxter language
    and evaluates it using standard python environment.
    This function returns the result of evaluation
    and may modify the given environment in-place as well.
    """
    parse_context = ParseContext(input_text)
    env = env or create_simple_env()
    evaluate_context = EvaluateContext(input_text, env, parse_context.tree)
    return evaluate_context.rendered


def run_document_paxter(input_text: str, env: Optional[dict] = None) -> Document:
    """
    Similar to run_simple_paxter,
    but uses specialized environment suitable for writing documents.
    The result is wrapped under Document data class.
    """
    parse_context = ParseContext(input_text)
    env = env or create_document_env()
    evaluate_context = EvaluateContext(input_text, env, parse_context.tree)
    return Document(evaluate_context.rendered)
