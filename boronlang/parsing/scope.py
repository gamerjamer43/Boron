class Scope:
    def __init__(self):
        self.imports = {}
        self.scopes = [{}]

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
        else:
            raise RuntimeError("Cannot exit global scope")

    def declare_variable(self, name, var_type):
        if name in self.scopes[-1]:
            raise SyntaxError(f"Variable '{name}' already declared in this scope.")
        self.scopes[-1][name] = var_type
    
    def declare_import(self, name, alias):
        if name in self.imports:
            raise SyntaxError(f"Import '{name}' already imported.")
        self.imports[name] = alias
    
    def is_declared(self, name):
        return any(name in scope for scope in reversed(self.scopes))
    
    def is_imported(self, name):
        return any(name == imp for imp in reversed(self.imports))

    def get_variable_type(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise NameError(f"Variable '{name}' not declared.")