"""
Transformer utility class to transform parsed tree into other formats
"""
from typing import Any

from paxter.core.data import (FragmentList, Identifier, Literal,
                              Node, PaxterFunc, PaxterMacro, PaxterPhrase, Text)

__all__ = ['BaseTransformer']


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
