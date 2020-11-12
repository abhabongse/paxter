"""
This paxter subpackage supplements a set of utilities
to be used to authoring a document via parsed tree evaluation.
"""
from __future__ import annotations

from paxter.authoring.environ import create_document_env, create_simple_env
from paxter.authoring.preset import run_document_paxter, run_simple_paxter

__all__ = [
    'create_document_env', 'create_simple_env',
    'run_document_paxter', 'run_simple_paxter',
]
