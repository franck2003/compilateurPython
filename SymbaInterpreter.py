from lark.visitors import Visitor_Recursive
from lark import Tree, Token
from memory import Memory
from errors import (
    SymbaException,
    SymbaUnknownVariable,
    SymbaSyntaxError,
)

class SymbaInterpreter(Visitor_Recursive):
    def __init__(self):
        self.memory = Memory()

    def assign_stmt(self, tree):
        var_token = tree.children[0]  # Token('NAME', 'x')
        var_name = var_token.value
        expr = tree.children[1]
        line = getattr(var_token, "line", None)

        try:
            self.memory.set(var_name, expr)
        except SymbaException:
            raise
        except Exception as e:
            raise SymbaException(f"Erreur inattendue pendant l'affectation à '{var_name}' : {e}", line)

    def print_stmt(self, tree):
        expr = tree.children[0]
        line = self._get_line(expr)
        try:
            print(self._expr_to_string(expr))
        except SymbaException as e:
            # Si l'erreur n'a pas déjà une ligne, on l'ajoute
            if e.line is None and line is not None:
                raise SymbaException(str(e), line)
            raise

    def _expr_to_string(self, node):
        if isinstance(node, Tree):
            if node.data == "add":
                left = self._expr_to_string(node.children[0])
                right = self._expr_to_string(node.children[1])
                return f"{left} + {right}"

            elif node.data == "parens":
                return f"({self._expr_to_string(node.children[0])})"

            elif node.data == "var":
                var_token = node.children[0]
                var_name = var_token.value
                line = getattr(var_token, "line", None)
                value = self.memory.get(var_name)
                if value is None:
                    raise SymbaUnknownVariable(var_name, line)
                return self._expr_to_string(value)

            elif node.data == "number":
                return str(node.children[0])

            elif node.data == "expr":
                return self._expr_to_string(node.children[0])

            else:
                return f"[Inconnu: {node.data}]"

        elif isinstance(node, Token):
            return str(node)

        return str(node)

    def _get_line(self, node):
        """Cherche récursivement un numéro de ligne dans un Tree ou Token"""
        if isinstance(node, Token):
            return getattr(node, "line", None)
        elif isinstance(node, Tree):
            for child in node.children:
                line = self._get_line(child)
                if line is not None:
                    return line
        return None
