"""
Transformer utility class to transform parsed tree into other formats
"""
from typing import Any, Tuple, Union

from paxter.core.data import (FragmentList, Identifier, Literal,
                              Node, PaxterFunc, PaxterMacro, PaxterPhrase, Text)

__all__ = ['BaseTransformer', 'SimplePythonTransformer']


class BaseTransformer:
    """
    Simple bottom-up parsed tree transformer for Paxter language.
    This class should be subclasses to override the transformation behavior
    for each particular node types.
    """

    def transform(self, env: dict, node: Node) -> Any:
        """
        Start transforming the given node.
        """
        return self.visit(env, node)

    def visit(self, env: dict, node: Node) -> Any:
        if isinstance(node, Identifier):
            return self.visit_identifier(env, node)
        if isinstance(node, Literal):
            return self.visit_literal(env, node)
        if isinstance(node, FragmentList):
            return self.visit_fragment_list(env, node)
        if isinstance(node, PaxterMacro):
            return self.visit_paxter_macro(env, node)
        if isinstance(node, PaxterFunc):
            return self.visit_paxter_func(env, node)
        if isinstance(node, PaxterPhrase):
            return self.visit_paxter_phrase(env, node)
        if isinstance(node, Text):
            return self.visit_text(env, node)
        raise RuntimeError("unrecognized parsed tree node")

    def visit_identifier(self, env: dict, node: Identifier) -> Any:
        return node

    def visit_literal(self, env: dict, node: Literal) -> Any:
        return node

    def visit_fragment_list(self, env: dict, node: FragmentList) -> Any:
        return node

    def visit_paxter_macro(self, env: dict, node: PaxterMacro) -> Any:
        return node

    def visit_paxter_func(self, env: dict, node: PaxterFunc) -> Any:
        return node

    def visit_paxter_phrase(self, env: dict, node: PaxterPhrase) -> Any:
        return node

    def visit_text(self, env: dict, node: Text) -> Any:
        return node


class SimplePythonTransformer(BaseTransformer):
    """
    Transformer that does something special with Python.
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
        print("before", id(cloned_env))
        result = self.visit(cloned_env, node)
        print("after", id(cloned_env))
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
