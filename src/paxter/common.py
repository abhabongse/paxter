"""
A collection of Paxter common functions.
"""
from typing import Any, Optional

from paxter.evaluator.context import EvaluateContext
from paxter.parser import ParseContext


def run_paxter(input_text: str, env: Optional[dict] = None) -> Any:
    """
    Parses the input source text written in Paxter language
    and evaluates it using standard python environment.
    The given environment may be modified in-place during evaluation.
    """
    parse_context = ParseContext(input_text)
    env = env or {}
    evaluate_context = EvaluateContext(input_text, env, parse_context.tree)
    return evaluate_context.rendered
