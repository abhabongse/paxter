"""
Base parsed tree transformer.
"""
from typing import Any

from paxter.data import (FragmentList, Identifier, Literal,
                         Node, PaxterFunc, PaxterMacro, PaxterPhrase, Text)


class Transformer:
    """
    Simple bottom-up parsed tree transformer for Paxter language.
    """

    def visit(self, env: dict, node: Node):
        """
        Generic node visitor method; dispatch tp a more specific method.
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
        raise RuntimeError("unrecognized parsed tree node")

    def visit_identifier(self, env: dict, node: Identifier) -> Any:
        raise RuntimeError("unexpected visit to identifier node")

    def visit_literal(self, env: dict, node: Literal) -> Any:
        return str(node.value)

    def visit_fragment_list(self, env: dict, node: FragmentList) -> Any:
        return ''.join(str(self.visit(env, child)) for child in node.children)

    def visit_paxter_macro(self, env: dict, node: PaxterMacro) -> Any:
        func = env[node.id.name]
        arg = node.text.string
        return func(env, arg)

    def visit_paxter_func(self, env: dict, node: PaxterFunc) -> Any:
        func = env[node.id.name]
        arg = self.visit(env, node.fragments)
        return func(arg)

    def visit_paxter_phrase(self, env: dict, node: PaxterPhrase) -> Any:
        return env[node.phrase.string]

    def visit_text(self, env: dict, node: Text) -> Any:
        return node.string
