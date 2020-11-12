"""
This paxter subpackage implements a variant of
parsed tree evaluation for Paxter language.
"""
from __future__ import annotations

from paxter.interpreting.data import FragmentList
from paxter.interpreting.task import InterpretingTask
from paxter.interpreting.wrappers import (
    BaseApply, DirectApply, NormalApply, NormalApplyWithEnv,
)

__all__ = [
    'InterpretingTask', 'FragmentList',
    'BaseApply', 'DirectApply', 'NormalApply', 'NormalApplyWithEnv',
]
