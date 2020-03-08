"""
Implements `SimplePythonTransformer` which works with
embedded Python expressions and statements.

## Interpretation of Parsed Tree

- Each `paxter.core.data.PaxterPhrase` evaluates its main text as python expression.
  Result of the evaluation will be output to the transformed text.
- Each `paxter.core.data.PaxterFunc` will be a function application
  of a function (which is indicated by its identifier part)
  with the main text part as the only positional argument.
  Specified options will be passed to the same function call as keyword arguments.
- Each `paxter.core.data.PaxterMacro` will be a function application
  of a function (which is indicated by its identifier ending with a `!`)
  with two positional arguments: the environment dict and the main text respectively.

Initially, the environment dict contains the following
(unless overridden by the input environment dict):

- A single `!` macro function simply executes the main text as python code.
  However, there will no output to the transformed text whatsoever.
- Three JSON-literal constants: `null`, `true`, and `false`.
- `__builtins__` may be introduced automatically due to usage of
  `eval` and `exec` built-in functions in this transformer.

## TODO

- Introduce special print-function that will allow text outputting into document
  which would be useful for python code inside single `!` macro function.
"""
from typing import Any, Tuple, Union

from paxter.core import (BaseTransformer, FragmentList, Identifier, Literal, PaxterFunc,
                         PaxterMacro, PaxterPhrase, Text)

__all__ = ['SimplePythonTransformer']


class SimplePythonTransformer(BaseTransformer):
    """
    Transformer of Paxter parsed tree which works with
    embedded Python expressions and statements.
    """

    def transform(self, env: dict, node: FragmentList) -> Tuple[dict, str]:
        """
        Transforms the given global-level fragment list into final string
        using the environment dict cloned from the input
        and with extra goodies added.

        This function returns a tuple pair of the final environment dict state
        and the transformed text output.
        """
        cloned_env = {
            '!': self.python_exec,
            'null': None,
            'true': True,
            'false': False,
            **env,
        }
        result = self.visit(cloned_env, node)
        return cloned_env, result

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
        func = env[node.id.name]
        arg = node.text.string
        result = func(env, arg)

        return result

    def visit_paxter_func(self, env: dict, node: PaxterFunc) -> Any:
        func = env[node.id.name]
        kwargs = {
            k.name: self.visit(env, v)
            for k, v in (node.options or [])
        }
        arg = self.visit_fragment_list(env, node.fragments)
        return func(arg, **kwargs)

    def visit_paxter_phrase(self, env: dict, node: PaxterPhrase) -> Any:
        return self.python_eval(env, node.phrase.string)

    def visit_text(self, env: dict, node: Text) -> str:
        return node.string

    @staticmethod
    def python_eval(env: dict, expression: str) -> str:
        """
        Invoke the given python expression
        and return its result casted as a string.
        """
        return eval(expression, env)

    @staticmethod
    def python_exec(env: dict, statements: str) -> str:
        """
        Invoke the given python statements for effect
        and then return empty string.
        """
        exec(statements, env)
        return ""
