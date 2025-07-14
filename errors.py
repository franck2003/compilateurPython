class SymbaException(Exception):
    """Exception de base pour toutes les erreurs du langage SymbA."""
    def __init__(self, message, line=None):
        if line is not None:
            message += f" (ligne {line})"
        super().__init__(message)
        self.line = line


class SymbaSyntaxError(SymbaException):
    """Erreur de syntaxe dans le code source."""
    def __init__(self, description, line=None):
        super().__init__(f"Erreur de syntaxe : {description}", line)


class SymbaUnknownVariable(SymbaException):
    """Une variable est utilisée sans avoir été initialisée."""
    def __init__(self, var, line=None):
        super().__init__(f"Variable inconnue : {var}", line)


class SymbaDivisionByZero(SymbaException):
    """Une division par zéro a été tentée pendant l'évaluation."""
    def __init__(self, line=None):
        super().__init__("Division par zéro détectée", line)


class SymbaInvalidOperation(SymbaException):
    """Une opération invalide a été tentée (type incompatible, etc.)."""
    def __init__(self, description, line=None):
        super().__init__(f"Opération invalide : {description}", line)
