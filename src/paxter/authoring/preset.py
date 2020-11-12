"""
A collection of Paxter common functions.
"""
from __future__ import annotations

from typing import Optional

from paxter.authoring.elements import Document
from paxter.authoring.environ import create_document_env, create_simple_env
from paxter.interpreting import FragmentList
from paxter.interpreting.task import InterpretingTask
from paxter.parsing import ParsingTask


def run_simple_paxter(src_text: str, env: Optional[dict] = None) -> FragmentList:
    """
    Parses the input source text written in Paxter language
    and evaluates it using standard python environment.
    This function returns the result of evaluation
    and may modify the given environment in-place as well.
    """
    parsed_tree = ParsingTask(src_text).parse()
    env = env or create_simple_env()
    rendered = InterpretingTask(src_text, env, parsed_tree).interp()
    return rendered


def run_document_paxter(src_text: str, env: Optional[dict] = None) -> Document:
    """
    Similar to run_simple_paxter,
    but uses specialized environment suitable for writing documents.
    The result is wrapped under Document data class.
    """
    parsed_tree = ParsingTask(src_text).parse()
    env = env or create_document_env()
    rendered = InterpretingTask(src_text, env, parsed_tree).interp()
    return Document.from_fragments(rendered)
