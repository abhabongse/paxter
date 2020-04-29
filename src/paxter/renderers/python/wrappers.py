from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, TYPE_CHECKING, Tuple

from paxter.core import Identifier, Operator, PaxterApply, Token, TokenList
from paxter.core.exceptions import PaxterRenderError

if TYPE_CHECKING:
    from paxter.renderers.python.visitor import RenderContext


@dataclass
class BaseApply(metaclass=ABCMeta):
    """
    Base class for `PaxterApply` function wrapper.
    """

    @abstractmethod
    def call(self, context: 'RenderContext', node: PaxterApply) -> Any:
        """
        Performs the evaluation of the given `PaxterApply` node
        in any way desired (including macro expansion before evaluation).
        """
        raise NotImplementedError


@dataclass
class DirectApply(BaseApply):
    """
    Special function call where the wrapped function handles
    the environment and the `PaxterApply` token directly.
    """
    wrapped: Callable[['RenderContext', PaxterApply], Any]

    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)

    def call(self, context: 'RenderContext', node: PaxterApply) -> Any:
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

    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)

    def call(self, context: 'RenderContext', node: PaxterApply) -> Any:
        if node.options:
            args, kwargs = self.extract_args_and_kwargs(context, node.options)
        else:
            args, kwargs = [], {}
        if node.main_arg:
            main_arg = context.visit_fragment(node.main_arg)
            args.insert(0, main_arg)
        return self.wrapped(*args, **kwargs)

    def extract_args_and_kwargs(
            self, context: 'RenderContext',
            options: TokenList,
    ) -> Tuple[list, dict]:
        """
        Returns a pair of positional argument list and keyword argument dict.
        """
        line, col = PaxterRenderError.pos_to_line_col(
            context.input_text, options.pos.start,
        )
        flipped = False  # kwargs found
        args = []
        kwargs = {}

        for keyword_name, value_token in self.tokenize_args(context, options):
            if keyword_name is not None:
                flipped = True
                if keyword_name in kwargs:
                    raise PaxterRenderError(
                        f"duplicated keyword {keyword_name} at line {line} col {col}",
                    )
                kwargs[keyword_name] = context.visit_token(value_token)
            elif flipped:
                raise PaxterRenderError(
                    f"found positional argument after keyword argument "
                    f"at line {line} col {col}",
                )
            else:
                args.append(context.visit_token(value_token))

        return args, kwargs

    @staticmethod
    def tokenize_args(
            context: 'RenderContext',
            options: TokenList,
    ) -> Tuple[Optional[str], Token]:
        """
        Generates a sequence of arguments, each of which
        is a tuple pair of (argument name, argument value token).
        The first component may be None which indicates positional arguments.
        """
        remains: List[Token] = list(options.children)
        while remains:

            # Checks whether the next token is an '=' operator
            # indicating the existence of keyword argument
            keyword_name = None
            if len(remains) >= 2:
                first_token, second_token = remains[0], remains[1]
                if isinstance(second_token, Operator) and second_token.symbol == '=':
                    # Then the first token must be an identifier
                    if not isinstance(first_token, Identifier):
                        line, col = PaxterRenderError.pos_to_line_col(
                            context.input_text, first_token.pos.start,
                        )
                        raise PaxterRenderError(
                            f"expected an identifier before the '=' sign "
                            f"at line {line} col {col}",
                        )
                    keyword_name = first_token.name
                    remains = remains[2:]

            # Expects the next token to be a value token
            if not remains:
                line, col = PaxterRenderError.pos_to_line_col(
                    context.input_text, options.pos.end,
                )
                raise PaxterRenderError(
                    f"expected a value after the '=' sign "
                    f"at line {line} col {col}",
                )
            value_token = remains[0]
            remains = remains[1:]

            # Yields the next argument
            yield keyword_name, value_token

            # If tokens are still remaining, the next one has to be a ',' operator
            if remains:
                end_token = remains[0]
                if not isinstance(end_token, Operator) or end_token.symbol != ',':
                    line, col = PaxterRenderError.pos_to_line_col(
                        context.input_text, end_token.pos.start,
                    )
                    raise PaxterRenderError(
                        f"expected a comma token after the value token "
                        f"at line {line} col {col}",
                    )
                remains = remains[1:]
