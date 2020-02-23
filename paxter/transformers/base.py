"""
Base parsed tree transformer.
"""
from paxter.data import (
    AtExprFunc, AtExprMacro, BaseNode, Fragments, Identifier, RawText,
)


class Transformer:
    """
    Paxter parsed tree transformer.
    """

    @classmethod
    def transform(cls, env: dict, node: BaseNode) -> str:
        transformed_obj = cls()
        return transformed_obj.visit(env, node)

    def visit(self, env: dict, node: BaseNode) -> str:
        """
        Generic node visitor method; dispatch to a more specific method.
        """
        if isinstance(node, Fragments):
            return self.visit_fragments(env, node)
        elif isinstance(node, RawText):
            return self.visit_raw_text(env, node)
        elif isinstance(node, AtExprMacro):
            return self.visit_at_expr_macro(env, node)
        elif isinstance(node, AtExprFunc):
            return self.visit_at_expr_func(env, node)
        else:
            raise RuntimeError("something went wrong")

    def visit_fragments(self, env: dict, node: Fragments) -> str:
        tokens = [str(self.visit(env, child)) for child in node.children]
        return "".join(tokens)

    def visit_raw_text(self, env: dict, node: RawText) -> str:
        return node.string

    def visit_at_expr_macro(self, env: dict, node: AtExprMacro) -> str:
        if node.identifier.name:
            func = env[node.identifier.name]
            arg = node.raw_text.string
            return func(arg)
        else:
            expr = node.raw_text.string
            return eval(expr, env)

    def visit_at_expr_func(self, env: dict, node: AtExprFunc) -> str:
        func = env[node.identifier.name]
        arg = self.visit(env, node.fragments)
        return func(arg)
