from lark.visitors import Visitor_Recursive
from lark import Tree, Token, Lark
from memory import Memory
from errors import *

class SymbaInterpreter(Visitor_Recursive):
    def __init__(self, expr_parser):
        self.memory = Memory()
        self.expr_parser = expr_parser  # Ajoute le parser d'expressions


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
            if e.line is None and line is not None:
                raise SymbaException(str(e), line)
            raise

    def _expr_to_string(self, node):

        if isinstance(node, Tree):

            if node.data == "vadd":
                left = self._expr_to_string(node.children[0])
                right = self._expr_to_string(node.children[1])
                return f"{left} !+ {right}"

            if node.data == "neg":
                value = self._expr_to_string(node.children[0])
                return f"-{value}"


            elif node.data == "vsub":
                left = self._expr_to_string(node.children[0])
                right = self._expr_to_string(node.children[1])
                return f"{left} !- {right}"

            elif node.data == "vmul":
                left = self._expr_to_string(node.children[0])
                right = self._expr_to_string(node.children[1])
                return f"{left} !* {right}"

            elif node.data == "vdiv":
                left_node = node.children[0]
                right_node = node.children[1]

                # Vérifie si le dénominateur est zéro
                if isinstance(right_node, Tree) and right_node.data == "number":
                    if right_node.children[0] == Token("NUMBER", "0"):
                        raise SymbaDivisionByZero(self._get_line(right_node))

                # Génération de la chaîne comme d’habitude
                left = self._expr_to_string(left_node)
                right = self._expr_to_string(right_node)
                return f"{left} !/ {right}"

            elif node.data == "add":
                left = self._expr_to_string(node.children[0])
                right = self._expr_to_string(node.children[1])
                return f"{left} + {right}"

            elif node.data == "sub":
                left = self._expr_to_string(node.children[0])
                right = self._expr_to_string(node.children[1])
                return f"{left} - {right}"

            elif node.data == "eval_expr":
                value = self._eval_expr(node.children[0])
                return str(value)


            elif node.data == "mul":
                left = self._expr_to_string(node.children[0])
                right = self._expr_to_string(node.children[1])
                return f"{left} * {right}"

            elif node.data == "div":
                left_node = node.children[0]
                right_node = node.children[1]

                # Vérifie si le dénominateur est zéro
                if isinstance(right_node, Tree) and right_node.data == "number":
                    if right_node.children[0] == Token("NUMBER", "0"):
                        raise SymbaDivisionByZero(self._get_line(right_node))

                left = self._expr_to_string(left_node)
                right = self._expr_to_string(right_node)
                return f"{left} / {right}"

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

    def eval_expr(self, tree):
        """
        Gère l'opérateur @ expr :
        1) Substitution récursive des variables
        2) Re-parsing de la chaîne pour corriger la priorité
        3) Évaluation finale
        """
        expr = tree.children[0]
        substituted_expr = self._recursive_substitute(expr)
        expr_str = self._expr_to_string(substituted_expr)
        print(expr_str)

        try:
            new_tree = self.expr_parser.parse(expr_str)
            print(new_tree)

        except Exception as e:
            raise SymbaException(f"Erreur lors du parsing de l'expression substituée : {expr_str}\nDétail : {e}",
                                 self._get_line(expr))

        result = self._eval_expr(new_tree)
        return result

    def _recursive_substitute(self, node):

        """
        Retourne un nouvel arbre où toutes les variables sont remplacées
        par leur expression dans la mémoire, récursivement.
        """
        if isinstance(node, Tree):
            if node.data == "var":
                var_token = node.children[0]
                var_name = var_token.value
                value = self.memory.get(var_name)
                if value is None:
                    line = getattr(var_token, "line", None)
                    raise SymbaUnknownVariable(var_name, line)
                # Recurse sur l'expression associée à la variable
                return self._recursive_substitute(value)

            # Sinon, copie récursive de l'arbre
            new_children = [self._recursive_substitute(child) for child in node.children]
            return Tree(node.data, new_children)

        elif isinstance(node, Token):
            return node

        else:
            return node

    def _eval_expr(self, node):
        print(node.data)
        if isinstance(node, Tree):
            if node.data == "number":
                return float(node.children[0])

            elif node.data == "var":
                var_token = node.children[0]
                var_name = var_token.value
                line = getattr(var_token, "line", None)
                value = self.memory.get(var_name)
                if value is None:
                    raise SymbaUnknownVariable(var_name, line)
                return self._eval_expr(value)

            elif node.data == "neg":
                return -self._eval_expr(node.children[0])

            elif node.data in {"add", "vadd"}:
                return self._eval_expr(node.children[0]) + self._eval_expr(node.children[1])

            elif node.data in {"sub", "vsub"}:
                return self._eval_expr(node.children[0]) - self._eval_expr(node.children[1])

            elif node.data in {"mul", "vmul"}:
                return self._eval_expr(node.children[0]) * self._eval_expr(node.children[1])

            elif node.data in {"div", "vdiv"}:
                left = self._eval_expr(node.children[0])
                right = self._eval_expr(node.children[1])
                if right == 0:
                    raise SymbaDivisionByZero(self._get_line(node.children[1]))
                return left / right

            elif node.data == "parens" or node.data == "expr":
                return self._eval_expr(node.children[0])

            elif node.data == "eval_expr":
                substituted = self._recursive_substitute(node.children[0])
                return self._eval_expr(substituted)

            else:
                raise SymbaInvalidOperation(f"Opération inconnue : {node.data}", self._get_line(node))

        elif isinstance(node, Token):
            if node.type == "NUMBER":
                return float(node)

        raise SymbaInvalidOperation("Expression invalide", self._get_line(node))


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
