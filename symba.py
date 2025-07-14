import argparse
from lark import Lark, UnexpectedInput
from SymbaInterpreter import SymbaInterpreter
from errors import SymbaException, SymbaSyntaxError

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("-m", "--memory", action="store_true")
    args = parser.parse_args()

    with open("symba.lark", encoding="utf-8") as f:
        grammar = f.read()

    try:
        with open(args.filename, encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Fichier introuvable : {args.filename}")
        return

    try:
        lark_parser = Lark(grammar, parser="lalr", start="start")
        tree = lark_parser.parse(code)
        interpreter = SymbaInterpreter()
        interpreter.visit(tree)

        if args.memory:
            print("\n--- Mémoire ---")
            for var, expr in interpreter.memory.dump().items():
                expr_str = interpreter._expr_to_string(expr)
                print(f"{var} : {expr_str}")

    except UnexpectedInput as e:
        raise SymbaSyntaxError(f"Erreur de syntaxe à la ligne {e.line}")
    except SymbaException as e:
        print(f"[Symba] {e}")

if __name__ == "__main__":
    main()
