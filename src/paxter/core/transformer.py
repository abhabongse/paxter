"""
Transformer utility class to transform parsed tree into other formats
"""
from typing import Any

from paxter.core.data import (FragmentList, Identifier, Literal,
                              Node, PaxterFunc, PaxterMacro, PaxterPhrase, Text)

__all__ = ['BaseTransformer', 'visitor_method_names']

visitor_method_names = ['visit', 'visit_identifier', 'visit_literal',
                        'visit_fragment_list', 'visit_paxter_macro',
                        'visit_paxter_func', 'visit_paxter_phrase', 'visit_text']


class BaseTransformer:
    """
    Simple bottom-up tree transformer parsed from Paxter language source text.

    Each visitor method in this class immediately
    returns the input node as the output of the method.
    Thus it is important that this class **would be subclassed**
    to override the transformation behavior
    for each particular node types.
    """

    def transform(self, env: dict, node: Node) -> Any:
        """
        Start transforming the given node.
        """
        return self.visit(env, node)  # pragma: no cover

    def visit(self, env: dict, node: Node) -> Any:
        """
        Dispatches to a visitor which handles the particular type
        of the input node.
        """
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
        raise RuntimeError("unrecognized parsed tree node")  # pragma: no cover

    def visit_identifier(self, env: dict, node: Identifier) -> Any:
        """
        Handles `paxter.core.data.Identifier` node.
        """
        return node  # pragma: no cover

    def visit_literal(self, env: dict, node: Literal) -> Any:
        """
        Handles `paxter.core.data.Literal` node.
        """
        return node  # pragma: no cover

    def visit_fragment_list(self, env: dict, node: FragmentList) -> Any:
        """
        Handles `paxter.core.data.FragmentList` node.
        """
        return node  # pragma: no cover

    def visit_paxter_macro(self, env: dict, node: PaxterMacro) -> Any:
        """
        Handles `paxter.core.data.PaxterMacro` node.
        """
        return node  # pragma: no cover

    def visit_paxter_func(self, env: dict, node: PaxterFunc) -> Any:
        """
        Handles `paxter.core.data.PaxterFunc` node.
        """
        return node  # pragma: no cover

    def visit_paxter_phrase(self, env: dict, node: PaxterPhrase) -> Any:
        """
        Handles `paxter.core.data.PaxterPhrase` node.
        """
        return node  # pragma: no cover

    def visit_text(self, env: dict, node: Text) -> Any:
        """
        Handles `paxter.core.data.Text` node.
        """
        return node  # pragma: no cover
