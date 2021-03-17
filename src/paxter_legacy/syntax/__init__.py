"""
This paxter_legacy subpackage implements
the syntax functionality for Paxter language.
"""
from __future__ import annotations

from paxter.syntax.charloc import CharLoc
from paxter.syntax.enclosing import EnclosingPattern, GlobalEnclosingPattern
from paxter.syntax.nodetypes import (
    Command, Fragment, FragmentSeq, Identifier, Number, Operator, Text, Token, TokenSeq,
)
from paxter.syntax.parser import Parser

__all__ = [
    'CharLoc',
    'Command', 'Fragment', 'FragmentSeq', 'Identifier',
    'Number', 'Operator', 'Text', 'Token', 'TokenSeq',
    'EnclosingPattern', 'GlobalEnclosingPattern',
    'Parser',
]
