import keyword
import re
import warnings
from typing import Any, Dict, Optional, Tuple, Union

from paxter.core import (
    BaseTransformer, FragmentList, Identifier, Literal, PaxterFunc,
    PaxterMacro, PaxterPhrase, PaxterTransformError, Text,
)
from paxter.flavors.simple_snake._defs import main_set
from paxter.flavors.simple_snake._utils import with_env, with_node


class SimpleSnakeTransformer(BaseTransformer):
    """
    Implementation of Paxton parsed tree transformer called **Simple Snake**.
    """
    start_env: Dict[str, Any]

    _BACKSLASH_NEWLINE_RE = re.compile(r'\\\n')

    def __init__(self, start_env: Optional[Dict[str, Any]] = None):
        self.start_env = main_set.get_copy()

        if start_env:
            for k in start_env.keys():
                self.not_python_keyword(k)
            self.start_env.update(start_env)

    def transform(self, env: dict, node: FragmentList) -> Tuple[dict, str]:
        """
        Transforms the given parsed tree into text output
        using a copy of the provided environment dict,
        and returns a tuple pair of the final environment dict state
        and the rendered text output.
        """
        env = {**self.start_env, **env}
        for k in env.keys():
            self.not_python_keyword(k)
        output_text = self.visit(env, node)
        output_text = self.post_process(output_text)
        return env, output_text

    def visit_identifier(self, env: dict, node: Identifier) -> Any:
        try:
            result = env[node.name]
        except KeyError as exc:
            raise PaxterTransformError(
                f"unknown identifier {node.name!r} at {{pos}}",
                positions={'pos': node.start_pos},
            ) from exc
        return result

    def visit_literal(self, env: dict, node: Literal) -> Union[str, int, float]:
        return node.value

    def visit_fragment_list(self, env: dict, node: FragmentList) -> str:
        fragments = [
            str(self.visit(env, child))
            for child in node.children
        ]
        return ''.join(fragments)

    def visit_paxter_macro(self, env: dict, node: PaxterMacro) -> Any:
        try:
            func = env[node.id.name]
        except KeyError as exc:
            raise PaxterTransformError(
                f"unknown macro name {node.id.name!r} at {{pos}}",
                positions={'pos': node.id.start_pos},
            ) from exc
        if isinstance(func, with_node):
            return func(self, env, node)
        if isinstance(func, with_env):
            func = func.get_callable(env)

        args, kwargs = node.get_args_and_kwargs()
        args = [self.visit(env, arg) for arg in args]
        kwargs = {k: self.visit(env, v) for k, v in kwargs.items()}
        main_arg = node.text.string

        try:
            result = func(main_arg, *args, **kwargs)
        except PaxterTransformError:
            raise
        except Exception as exc:
            raise PaxterTransformError(
                f"macro {node.id.name!r} evaluation error at {{pos}}",
                positions={'pos': node.start_pos},
            ) from exc
        return result

    def visit_paxter_func(self, env: dict, node: PaxterFunc) -> Any:
        try:
            func = env[node.id.name]
        except KeyError as exc:
            raise PaxterTransformError(
                f"unknown function name {node.id.name!r} as {{pos}}",
                positions={'pos': node.id.start_pos},
            ) from exc
        if isinstance(func, with_node):
            return func(self, env, node)
        if isinstance(func, with_env):
            func = func.get_callable(env)

        args, kwargs = node.get_args_and_kwargs()
        args = [self.visit(env, arg) for arg in args]
        kwargs = {k: self.visit(env, v) for k, v in kwargs.items()}
        main_arg = self.visit_fragment_list(env, node.fragments)

        try:
            result = func(main_arg, *args, **kwargs)
        except PaxterTransformError:
            raise
        except Exception as exc:
            raise PaxterTransformError(
                f"function {node.id.name!r} evaluation error at {{pos}}",
                positions={'pos': node.start_pos},
            ) from exc
        return result

    def visit_paxter_phrase(self, env: dict, node: PaxterPhrase) -> Any:
        expr = node.phrase.string
        try:
            result = eval(expr, env)
        except PaxterTransformError:
            raise
        except Exception as exc:
            raise PaxterTransformError(
                "phrase evaluation error at {pos}",
                positions={'pos': node.start_pos},
            ) from exc
        return result

    def visit_text(self, env: dict, node: Text) -> str:
        return node.string

    def not_python_keyword(self, k: str):
        if keyword.iskeyword(k):
            warnings.warn(f"python keyword may not be seen in the environment: {k}")

    def post_process(self, text: str) -> str:
        text = self._BACKSLASH_NEWLINE_RE.sub('', text)
        return text
