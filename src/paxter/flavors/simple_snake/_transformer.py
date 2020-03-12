import inspect
import io
import keyword
import re
import warnings
from typing import Any, Dict, List, Optional, Tuple, Union

from paxter.core import (
    BaseTransformer, FragmentList, Identifier, Literal, PaxterFunc, PaxterMacro,
    PaxterPhrase, Text,
)
from paxter.core.data import BaseAtom, KeyValue
from paxter.core.exceptions import PaxterTransformError
from paxter.flavors.simple_snake.functions import (
    base64_set, html_set, string_set,
)

_function_envs = {
    'base64': base64_set,
    'html': html_set,
    'string': string_set,
}


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
            '!': self._python_exec,
            'load!': self._load_functions,
        }
        if start_env:
            self.start_env.update(start_env)
        for k in self.start_env.keys():
            self._verify_not_python_keyword(k)

    def transform(self, env: dict, node: FragmentList) -> Tuple[dict, str]:
        """
        Transforms the given parsed tree into text output
        using a copy of the provided environment dict,
        and returns a tuple pair of the final environment dict state
        and the rendered text output.
        """
        env = {**self.start_env, **env}
        for k in env.keys():
            self._verify_not_python_keyword(k)
        output_text = self.visit(env, node)
        output_text = self._post_process(output_text)
        return env, output_text

    def visit_identifier(self, env: dict, node: Identifier) -> Any:
        return env[node.name]

    def visit_literal(self, env: dict, node: Literal) -> Union[str, int, float]:
        return node.value

    def visit_fragment_list(self, env: dict, node: FragmentList) -> str:
        transformed_fragments = [
            str(self.visit(env, child))
            for child in node.children
        ]
        return ''.join(transformed_fragments)

    def visit_paxter_macro(self, env: dict, node: PaxterMacro) -> Any:
        try:
            func = env[node.id.name]
        except KeyError as exc:
            raise PaxterTransformError(f"unknown macro name {exc.args[0]}") from exc
        arg = node.text.string
        result = func(env, arg)

        return result

    def visit_paxter_func(self, env: dict, node: PaxterFunc) -> Any:
        if node.id.name == 'for':
            return self._for_loop(env, node)
        if node.id.name == 'if':
            return self._if_cond(env, node)

        try:
            func = env[node.id.name]
        except KeyError as exc:
            raise PaxterTransformError(f"unknown function name {exc.args[0]}") from exc
        kwargs = {
            k.name: self.visit(env, v)
            for k, v in (node.options or [])
        }
        arg = self.visit_fragment_list(env, node.fragments)
        return func(arg, **kwargs)

    def visit_paxter_phrase(self, env: dict, node: PaxterPhrase) -> Any:
        expr = node.phrase.string
        return eval(expr, env)

    def visit_text(self, env: dict, node: Text) -> str:
        return node.string

    def _python_exec(self, env: dict, code: str) -> str:
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

    def _load_functions(self, env: dict, name: str) -> str:
        try:
            function_env = _function_envs[name.strip()]
        except KeyError as exc:
            available_list = ', '.join(_function_envs.keys())
            raise PaxterTransformError(
                f"unrecognized function group name: {exc.args[0]}"
                f"(available are {available_list})",
            ) from exc
        env.update(function_env.env)
        return ''

    def _if_cond(self, env: dict, node: PaxterFunc):
        options: List[KeyValue] = node.options or []
        if (len(options) == 0 or len(options) > 2
                or any(v is not None for _, v in options)):
            raise PaxterTransformError(
                "if cond requires exactly two options in the form [item_id,seq]",
            )

        test = eval(options[0].k.name, env)
        if len(options) == 1 or options[1].k.name == 'true':
            target = True
        elif options[1].k.name == 'false':
            target = False
        else:
            raise PaxterTransformError(
                "second arg to if cond must be 'true' or 'false' literal",
            )

        if bool(test) is target:
            return self.visit_fragment_list(env, node.fragments)
        else:
            return ''

    def _for_loop(self, env: dict, node: PaxterFunc):
        options: List[KeyValue] = node.options or []
        if len(options) != 2 or any(v is not None for _, v in options):
            raise PaxterTransformError(
                "for loop requires exactly two options in the form [item_id,seq]",
            )
        item_id = options[0].k.name
        seq = eval(options[1].k.name, env)

        transformed_fragments = []
        for value in seq:
            env[item_id] = value
            transformed = self.visit_fragment_list(env, node.fragments)
            transformed_fragments.append(transformed)

        return ''.join(transformed_fragments)

    def _verify_not_python_keyword(self, k: str):
        if keyword.iskeyword(k):
            warnings.warn(f"python keyword may not be seen in the environment: {k}")

    def _extract_node_by_key(
            self, key_name: str, options: List[KeyValue],
    ) -> Optional[BaseAtom]:
        values = [v for k, v in options if k.name == key_name]
        if len(values) != 1:
            raise PaxterTransformError(
                f"expected exactly one key with name {key_name!r} "
                f"but {len(values)} were found",
            )
        return values[0]

    def _post_process(self, text: str) -> str:
        text = self._BACKSLASH_NEWLINE_RE.sub('', text)
        return text
