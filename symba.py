import argparse
from lark import Lark, UnexpectedInput
from SymbaInterpreter import SymbaInterpreter
from errors import SymbaException

def main():
    parser = argparse.ArgumentParser(description="Interpréteur Symba avec opérateur @")
    parser.add_argument("filename", help="Fichier source Symba à interpréter")
    parser.add_argument("-m", "--memory", action="store_true", help="Afficher le contenu de la mémoire après exécution")
    args = parser.parse_args()

    # Charge la grammaire depuis le fichier symba.lark
    with open("symba.lark", encoding="utf-8") as f:
        grammar = f.read()

    # Lit le code source
    try:
        with open(args.filename, encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Fichier introuvable : {args.filename}")
        return

    # Parse le code avec Lark
    try:
        lark_parser = Lark(grammar, parser="lalr", start="start")
        expr_parser = Lark(grammar, parser="lalr", start="expr")  # ✅ nouveau parser pour les expressions seulement

        tree = lark_parser.parse(code)
    except UnexpectedInput as e:
        print(f"Erreur de syntaxe à la ligne {e.line}")
        return

    # Interprète le code
    try:
        interpreter = SymbaInterpreter(expr_parser)
        interpreter.visit(tree)

        if args.memory:
            print("\n--- Mémoire ---")
            for var, expr in interpreter.memory.dump().items():
                expr_str = interpreter._expr_to_string(expr)
                print(f"{var} : {expr_str}")

    except SymbaException as e:
        print(f"[Symba] {e}")

if __name__ == "__main__":
    main()
