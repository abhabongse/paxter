import inspect
import io
import keyword
import re
import warnings
from typing import Any, Dict, List, Optional, Tuple, Union

from paxter.core import (
    BaseAtom, BaseTransformer, FragmentList, Identifier, KeyValue, Literal, PaxterFunc,
    PaxterMacro, PaxterPhrase, PaxterTransformError, Text,
)
from paxter.flavors.simple_snake.functions import (
    base64_set, html_set, string_set,
)

_FUNCTION_ENVIRONMENTS = {
    'base64': base64_set,
    'html': html_set,
    'string': string_set,
}


# TODO: Add positions to PaxterTransformError

class SimpleSnakeTransformer(BaseTransformer):
    """
    Implementation of Paxton parsed tree transformer called **Simple Snake**.
    """
    start_env: Dict[str, Any]

    _BACKSLASH_NEWLINE_RE = re.compile(r'\\\n')

    def __init__(self, start_env: Optional[Dict[str, Any]] = None):
        self.start_env = {
            'null': None,
            'true': True,
            'false': False,
            '!': self.python_exec,
            'load!': self.load_functions,
        }
        if start_env:
            self.start_env.update(start_env)
        for k in self.start_env.keys():
            self.not_python_keyword(k)

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

        args, kwargs = node.get_args_and_kwargs()
        args = [self.visit(env, arg) for arg in args]
        kwargs = {k: self.visit(env, v) for k, v in kwargs.items()}
        main_arg = node.text.string

        try:
            result = func(env, main_arg, *args, **kwargs)
        except PaxterTransformError:
            raise
        except Exception as exc:
            raise PaxterTransformError(
                f"macro {node.id.name!r} evaluation error at {{pos}}",
                positions={'pos': node.start_pos},
            ) from exc
        return result

    def visit_paxter_func(self, env: dict, node: PaxterFunc) -> Any:
        if node.id.name == 'if':
            return self.process_if(env, node)
        if node.id.name == 'for':
            return self.process_for(env, node)

        try:
            func = env[node.id.name]
        except KeyError as exc:
            raise PaxterTransformError(
                f"unknown function name {node.id.name!r} as {{pos}}",
                positions={'pos': node.id.start_pos},
            ) from exc

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

    def python_exec(self, env: dict, code: str) -> str:
        # Create a new buffer and inject into environment
        buffer = io.StringIO()
        env['buffer'] = buffer

        # Execute python code
        code = inspect.cleandoc(code)
        exec(code, env)

        # Remove buffer from environment, close it, and return its content
        del env['buffer']
        text = buffer.getvalue()
        buffer.close()
        return text

    def load_functions(self, env: dict, name: str) -> str:
        try:
            function_env = _FUNCTION_ENVIRONMENTS[name.strip()]
        except KeyError as exc:
            available_list = ', '.join(_FUNCTION_ENVIRONMENTS.keys())
            raise PaxterTransformError(
                f"unrecognized function group name: {name.strip()}"
                f"(available are {available_list})",
            ) from exc
        env.update(function_env.env)
        return ''

    def process_if(self, env: dict, node: PaxterFunc):
        options: List[KeyValue] = node.options or []
        if not 1 <= len(options) <= 2:
            raise PaxterTransformError(
                "if condition at {pos} requires 1 or 2 options "
                "in the form [test_id] or [test_id,target_bool]",
                positions={'pos': node.start_pos},
            )

        if len(options) > 1:
            target_literal = options[1].get_faux_key()
            if target_literal == 'true':
                target_bool = True
            elif target_literal == 'false':
                target_bool = False
            else:
                raise PaxterTransformError(
                    "second argument of if condition at {pos} "
                    "must either be 'true' or 'false' literal",
                    positions={'pos': node.start_pos},
                )
        else:
            target_bool = True

        test_id = options[0].get_faux_key()
        test = eval(test_id, env)
        if callable(test):
            test = test()

        if bool(test) is target_bool:
            return self.visit_fragment_list(env, node.fragments)
        else:
            return ''

    def process_for(self, env: dict, node: PaxterFunc):
        options: List[KeyValue] = node.options or []
        if len(options) != 2:
            raise PaxterTransformError(
                "for loop at {pos} requires exactly 2 options "
                "in the form [item_id,seq]",
                positions={'pos': node.start_pos},
            )

        item_id = options[0].get_faux_key()
        seq = eval(options[1].get_faux_key(), env)

        fragments = []
        for value in seq:
            env[item_id] = value
            transformed = self.visit_fragment_list(env, node.fragments)
            fragments.append(transformed)

        return ''.join(fragments)

    def not_python_keyword(self, k: str):
        if keyword.iskeyword(k):
            warnings.warn(f"python keyword may not be seen in the environment: {k}")

    def post_process(self, text: str) -> str:
        text = self._BACKSLASH_NEWLINE_RE.sub('', text)
        return text
