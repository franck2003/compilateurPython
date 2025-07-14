class Memory:
    def __init__(self):
        self.variables = {}

    def set(self, name, expr):
        self.variables[name] = expr

    def get(self, name):
        return self.variables.get(name, None)

    def dump(self):
        return self.variables
