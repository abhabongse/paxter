"""
Implements a flavor of tree transformer called **Simple Snake**.
It allows python code to be embedded within the input document text itself.
"""
import re
from typing import Any, Tuple, Union

from paxter.core import (BaseTransformer, FragmentList, Identifier, Literal, PaxterFunc,
                         PaxterMacro, PaxterPhrase, Text)
from paxter.flavors.simple_snake.functions import default_env


__all__ = ['SimpleSnakeTransformer']

__pdoc__ = {
    'SimpleSnakeTransformer.BACKSLASH_NEWLINE_RE': False,
    'SimpleSnakeTransformer.visit_identifier': False,
    'SimpleSnakeTransformer.visit_literal': False,
    'SimpleSnakeTransformer.visit_fragment_list': False,
    'SimpleSnakeTransformer.visit_paxter_macro': False,
    'SimpleSnakeTransformer.visit_paxter_func': False,
    'SimpleSnakeTransformer.visit_paxter_phrase': False,
    'SimpleSnakeTransformer.visit_text': False,
}


class SimpleSnakeTransformer(BaseTransformer):
    """
    **Simple Snake.** Transformer of Paxter parsed tree which allows python code
    to be embedded within the input document text itself.

    ## Interpretation of Parsed Tree

    ### Node Transformations

    - Each `paxter.core.data.PaxterPhrase` evaluates its main text as python expression.
      Result of the evaluation will be output to the transformed text.
    - Each `paxter.core.data.PaxterFunc` will be a function application
      of a function (which is indicated by its identifier part)
      with the main text part as the only positional argument.
      Specified options will be passed to the same function call as keyword arguments.
    - Each `paxter.core.data.PaxterMacro` will be a function application
      of a function (which is indicated by its identifier ending with a `!`)
      with two positional arguments: the environment dict and the main text respectively.

    ### Starting Environments

    The environment dict _initially_ contains the following data
    (may be overridden by the input environment dict):

    - A single `!` macro function simply executes the main text as python code.
      However, there will no output to the transformed text whatsoever.
    - Three JSON-literal constants: `null`, `true`, and `false`.
    - `__builtins__` may be introduced automatically due to usage of
      `eval` and `exec` built-in functions in this transformer.

    ### Post-processing

    At the end of the transformation, if a line ends with a backslash,
    then the newline at the end of that line will be removed from the output text.

    ## TODO

    - Introduce special print-function that will allow text outputting into document
      which would be useful for python code inside single `!` macro function.
    """
    BACKSLASH_NEWLINE_RE = re.compile(r'\\\n')

    def transform(self, env: dict, node: FragmentList) -> Tuple[dict, str]:
        """
        Transforms the given parsed tree into text output
        using a copy of the provided environment dict,
        and returns a tuple pair of the final environment dict state
        and the rendered text output.
        """
        env = default_env.clone_and_adapt(env)
        output_text = self.visit(env, node)
        output_text = self._remove_backslash_newline(output_text)
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
        return self._python_eval(env, node.phrase.string)

    def visit_text(self, env: dict, node: Text) -> str:
        return node.string

    @classmethod
    def _remove_backslash_newline(cls, text: str) -> str:
        """
        Remove all occurrences of r'\\\n' from the given text.
        """
        return cls.BACKSLASH_NEWLINE_RE.sub('', text)

    @staticmethod
    def _python_eval(env: dict, expression: str) -> str:
        """
        Invoke the given python expression
        and return its result casted as a string.
        """
        return eval(expression, env)
