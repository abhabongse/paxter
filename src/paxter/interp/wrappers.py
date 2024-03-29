"""
Collection of function wrappers in Python quickauthor mode.
"""
from __future__ import annotations

from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Optional, TYPE_CHECKING

from paxter.exceptions import PaxterRenderError
from paxter.syntax import CharLoc, Command, Identifier, Operator, Token, TokenSeq

if TYPE_CHECKING:
    from paxter.interp.task import InterpretingTask


@dataclass
class BaseApply(metaclass=ABCMeta):
    """
    Base class for :class:`Command` function wrapper
    which is intended to be used as a function decorator.
    """

    @abstractmethod
    def call(self, context: InterpretingTask, node: Command) -> Any:
        """
        Performs the evaluation of the given :class:`Command` node
        in any way desired (including macro expansion before evaluation).
        """
        raise NotImplementedError


@dataclass
class DirectApply(BaseApply):
    """
    Special function call where the wrapped function handles
    the environment and the :class:`Command` token directly.
    See the implementation of
    :func:`if_statement <paxter.quickauthor.controls.if_statement>` and
    :func:`for_statement <paxter.quickauthor.controls.for_statement>` and
    to see how this decorator is used.
    """
    wrapped: Callable[[InterpretingTask, Command], Any]

    def __post_init__(self):
        self.__wrapped__ = self.wrapped
        self.__doc__ = getattr(self.wrapped, '__doc__', None)

    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)

    def call(self, context: InterpretingTask, node: Command) -> Any:
        return self.wrapped(context, node)


@dataclass
class NormalApply(BaseApply):
    """
    Normal function call, assuming that the options section
    is a sequence of positional and keyword arguments
    in addition to the main argument section to the function.

    Each argument will be rendered individually in order
    before they are gathered and sent to the wrapped function.
    """
    wrapped: Callable

    def __post_init__(self):
        self.__wrapped__ = self.wrapped
        self.__doc__ = getattr(self.wrapped, '__doc__', None)

    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)

    def call(self, context: InterpretingTask, node: Command) -> Any:
        if node.options:
            args, kwargs = self.extract_args_and_kwargs(context, node.options)
        else:
            args, kwargs = [], {}
        if node.main_arg:
            main_arg = context.transform_token(node.main_arg)
            args = [main_arg] + args
        return self.wrapped(*args, **kwargs)

    def extract_args_and_kwargs(
            self, context: InterpretingTask,
            options: TokenSeq,
    ) -> tuple[list, dict]:
        """
        Returns a pair of positional argument list and keyword argument dict.
        """
        section_flipped = False  # kwargs found
        args = []
        kwargs = {}

        for keyword_name, value_token in self.tokenize_args(context, options):
            if keyword_name is not None:
                section_flipped = True
                if keyword_name in kwargs:
                    raise PaxterRenderError(
                        f"duplicated keyword {keyword_name} at %(pos)s",
                        pos=CharLoc(context.src_text, options.start_pos),
                    )
                kwargs[keyword_name] = context.transform_token(value_token)
            elif section_flipped:
                raise PaxterRenderError(
                    "found positional argument after keyword argument at %(pos)s",
                    pos=CharLoc(context.src_text, options.start_pos),
                )
            else:
                args.append(context.transform_token(value_token))

        return args, kwargs

    @staticmethod
    def tokenize_args(
            context: InterpretingTask,
            options: TokenSeq,
    ) -> tuple[Optional[str], Token]:
        """
        Generates a sequence of arguments, each of which
        is a tuple pair of (argument name, argument value token).
        The first component may be None which indicates positional arguments.
        """
        remains: list[Token] = list(options.children)

        while remains:
            # Checks whether the second token is an '=' operator
            # indicating the existence of keyword argument
            keyword_name = None
            if len(remains) >= 2:
                first_token, second_token = remains[0], remains[1]
                if second_token == Operator.without_pos(symbols='='):
                    # Then the first token must be an identifier
                    if not isinstance(first_token, Identifier):
                        raise PaxterRenderError(
                            "expected an identifier before the '=' sign at %(pos)s",
                            pos=CharLoc(context.src_text, first_token.start_pos),
                        )
                    keyword_name = first_token.name
                    remains = remains[2:]

            # Expects the next value token to exist
            if not remains:
                raise PaxterRenderError(
                    "expected a value after the '=' sign at %(pos)s",
                    pos=CharLoc(context.src_text, options.end_pos),
                )
            value_token = remains[0]
            remains = remains[1:]

            # Yields the next argument
            yield keyword_name, value_token

            # If tokens are still remaining, the next one has to be a ',' operator
            if remains:
                end_token = remains[0]
                if end_token != Operator.without_pos(symbols=','):
                    raise PaxterRenderError(
                        "expected a comma token after the value token at %(pos)s",
                        pos=CharLoc(context.src_text, end_token.start_pos),
                    )
                remains = remains[1:]


class NormalApplyWithEnv(NormalApply):
    """
    Just like normal apply, but the wrapped function will additionally
    receive the environment dict as the very first argument.
    """

    def call(self, context: InterpretingTask, node: Command) -> Any:
        if node.options:
            args, kwargs = self.extract_args_and_kwargs(context, node.options)
        else:
            args, kwargs = [], {}
        if node.main_arg:
            main_arg = context.transform_token(node.main_arg)
            args = [main_arg] + args
        return self.wrapped(context.env, *args, **kwargs)
