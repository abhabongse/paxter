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
    This function returns the result of evaluation
    and may modify the given environment in-place as well.
    """
    parse_context = ParseContext(input_text)
    env = env or {}
    evaluate_context = EvaluateContext(input_text, env, parse_context.tree)
    return evaluate_context.rendered
