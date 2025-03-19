# tokentype from my lexer and all ASTNodes from parser
from lexer.lexer import TokenType, Token
from parsing.astnodes import *

# decimal import for better precision, fuck floats no floats in my language
from decimal import Decimal
# importlib and os for package support
import importlib.util, os
from rich import print  # colored prints

# builtin functions
from interpreter.builtins import BUILTINS

class Interpreter:
    def __init__(self):
        # initialize a global scope and the package folder (locally for right now)
        self.global_scope = {}
        self.package_folder = "C:\\Users\\fuzio\\Downloads\\programs\\showcase\\Boron\\packages"
        self.global_scope.update(BUILTINS)

        self.dispatch = {
            Program: self.evaluate_program,
            Import: self.evaluate_import,
            VariableDeclaration: self.evaluate_variable_declaration,
            BinaryOperation: self.evaluate_binary_operation,
            UnaryOperation: self.evaluate_unary_operation,
            IfStatement: self.evaluate_if_statement,
            ForLoop: self.evaluate_for_loop,
            WhileLoop: self.evaluate_while_loop,
            DoWhileLoop: self.evaluate_do_while_loop,
            Function: self.evaluate_function,
            FunctionCall: self.evaluate_function_call,
            ReturnStatement: self.evaluate_return_statement,
            Identifier: self.evaluate_identifier,
            IntLiteral: lambda node: int(node.value),
            DecLiteral: lambda node: Decimal(node.value),
            StringLiteral: lambda node: str(node.value),
            BooleanLiteral: lambda node: node.value.lower() == "true",
            ListLiteral: lambda node: [self.evaluate(el) for el in node.elements],
            ArrayLiteral: self.evaluate_array_literal,
            VectorLiteral: self.evaluate_vector_literal,
            RangeLiteral: lambda node: range(
                self.evaluate(node.start),
                self.evaluate(node.stop),
                self.evaluate(node.increment)
            ),
            ClassLiteral: self.evaluate_class_literal,
            ClassInstantiation: self.evaluate_class_instantiation,
            FieldAssignment: self.evaluate_field_assignment,
            FieldAccess: self.evaluate_field_access,
            MethodCall: self.evaluate_method_call,
            IndexAccess: self.evaluate_index_access,
            IndexAssignment: self.evaluate_index_assignment,
            NoneObject: lambda node: None,
            EndOfFile: lambda node: None,
        }

    # the main evaluation function for the program. every node will go through this
    def evaluate(self, node):
        func = self.dispatch.get(type(node))
        if func is None:
            raise NotImplementedError(f"Evaluation for {node} not implemented.")
        return func(node)

    # wrapper to push the entire program through evaluation
    def evaluate_program(self, program):
        for statement in program.statements:
            try:
                self.evaluate(statement)
            except KeyboardInterrupt:
                print("[red]KeyboardInterrupt[/red]")

    # enforces type against the following for right now: integer, decimal, boolean, string, array (WIP)
    def enforce_type(self, expected_type, value):
        # ensure integers are whole numbers
        if expected_type is TokenType.INTEGER:
            if isinstance(value, Decimal):
                if value % 1 != 0:
                    raise ValueError("Cannot assign non-integer value {} to an integer.".format(value))
                return int(value)
            if isinstance(value, int):
                return value
            raise ValueError("Expected integer, got {} with value {}.".format(type(value), value))

        # ensure decimals are stored as Decimal
        elif expected_type is TokenType.DECIMAL:
            if isinstance(value, (Decimal, int)):
                return Decimal(value)
            raise ValueError("Expected decimal, got {} with value {}.".format(type(value), value))

        # ensure booleans are actual booleans
        elif expected_type is TokenType.BOOLEAN:
            if isinstance(value, bool):
                return value
            raise ValueError("Expected boolean, got {} with value {}.".format(type(value), value))

        # ensure strings are proper string literals
        elif expected_type is TokenType.STR:
            if isinstance(value, str):
                return value
            raise ValueError("Expected string, got {} with value {}.".format(type(value), value))

        return value

    # loading for packages, packages are just .py files for right now, full python libraries soon
    def evaluate_import(self, node):
        # get name from node, get path from name
        module_name = node.module
        package_path = os.path.join(self.package_folder, f"{module_name}.py")

        # if it doesn't exist raise an import error
        if not os.path.exists(package_path):
            raise ImportError(f"Package '{module_name}' not found in '{self.package_folder}'.")

        # get spec from file location, get module from spec, and execute the module
        spec = importlib.util.spec_from_file_location(module_name, package_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module_name = node.alias

        # add to global scope
        self.global_scope[module_name] = module
        # print(f"Imported package: {module_name}")
    
    # variable evaluation, checks type with the function below
    def evaluate_variable_declaration(self, node):
        # get name from node by either getting it from the node directly (non identifiers) or going inside (identifiers)
        if isinstance(node.name, str):
            var_name = node.name
        elif hasattr(node.name, 'name'):
            var_name = node.name.name
        elif hasattr(node.name, 'value'):
            var_name = node.name.value
        else:
            raise ValueError("Invalid variable name type.")
        value = self.evaluate(node.value) if node.value else None  # evaluate that afterwards

        # default node values (for initializations)
        if node.value is None:
            if node.var_type == TokenType.INTEGER:
                value = 0
            elif node.var_type == TokenType.DECIMAL:
                value = Decimal(0)
            elif node.var_type == TokenType.BOOLEAN:
                value = False
            elif node.var_type == TokenType.STR:
                value = ""
            else:
                value = None

        # finally enforce type
        # print(f"Enforcing type for {node.var_type}, {node.name}: {value}")
        value = self.enforce_type(node.var_type, value)
        
        # and add to global scope (this is just for logging purposes)
        # if var_name in self.global_scope:
            # print(f"Assigned {var_name} = {value}")
        # else:
            # print(f"Declared {node.var_type} {var_name} = {value}")

        self.global_scope[var_name] = value
        return value

    def evaluate_binary_operation(self, node):
        # evaluate left and right before operating
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        # match operator type
        if node.operator == TokenType.INCREMENT:
            return left + 1
        elif node.operator == TokenType.DECREMENT:
            return left - 1
        elif node.operator == TokenType.INCREASE:
            if isinstance(node.left, Identifier) and node.left.name in self.global_scope:
                self.global_scope[node.left.name] += right
            return self.global_scope[node.left.name]
        elif node.operator == TokenType.DECREASE:
            if isinstance(node.left, Identifier) and node.left.name in self.global_scope:
                self.global_scope[node.left.name] -= right
            return self.global_scope[node.left.name]
        elif node.operator == TokenType.MULTEQ:
            if isinstance(node.left, Identifier) and node.left.name in self.global_scope:
                self.global_scope[node.left.name] *= right
            return self.global_scope[node.left.name]
        elif node.operator == TokenType.DIVEQ:
            if isinstance(node.left, Identifier) and node.left.name in self.global_scope:
                self.global_scope[node.left.name] /= right
            return self.global_scope[node.left.name]
        elif node.operator == TokenType.ADD:
            return left + right
        elif node.operator == TokenType.SUBTRACT:
            return left - right
        elif node.operator == TokenType.MULTIPLY:
            return left * right
        elif node.operator == TokenType.DIVIDE:
            return left / right
        elif node.operator == TokenType.POWER:
            return left ** right
        elif node.operator == TokenType.FLOOR_DIVIDE:
            return left // right
        elif node.operator == TokenType.GREATER_THAN:
            return left > right
        elif node.operator == TokenType.LESS_THAN:
            return left < right
        elif node.operator == TokenType.GREATER_EQUAL:
            return left >= right
        elif node.operator == TokenType.LESS_EQUAL:
            return left <= right
        elif node.operator == TokenType.EQUAL:
            return left == right
        elif node.operator == TokenType.NOT_EQUAL:
            return left != right
        elif node.operator == TokenType.MODULUS:
            return left % right
        elif node.operator == TokenType.AND:
            return left and right
        elif node.operator == TokenType.OR:
            return left or right
        else:
            # if operator not above, throw NotImplementedError (which will be changed to custom error logging soon)
            raise NotImplementedError(f"Binary operator {node.operator} not implemented.")

    # fix nots. this is just for unary operations, ones that only require an operator and a single operand
    def evaluate_unary_operation(self, node):
        # get said operand
        operand = self.evaluate(node.operand)

        # if not (FIX THIS)
        if node.operator == TokenType.NOT:
            if isinstance(node.operand, Identifier):
                identifier_name = node.operand.name
                
                if identifier_name in self.global_scope:
                    value = self.global_scope[identifier_name]
                    if isinstance(value, bool):
                        # negate the boolean value in the global scope
                        self.global_scope[identifier_name] = not value
                        # print(f"Negated {identifier_name}: {not value}")
                        return not value
                    else:
                        raise TypeError(f"'{identifier_name}' is not a boolean and cannot be negated.")
                else:
                    raise ValueError(f"'{identifier_name}' is not defined.")
            else:
                return not operand
        
        # else for increments and decrements
        elif node.operator == TokenType.INCREMENT:
            if isinstance(node.operand, Identifier):
                self.global_scope[node.operand.name] += 1
                # print(f"Incremented {node.operand.name} +1")
                return operand
            return operand + 1
        elif node.operator == TokenType.DECREMENT:
            if isinstance(node.operand, Identifier):
                self.global_scope[node.operand.name] -= 1
                # print(f"Decremented {node.operand.name} -1")
                return operand
            return operand - 1
        else:
            # another NotImplementedError
            raise NotImplementedError(f"Unary operator {node.operator} not implemented.")

    # ...self explanitory
    def evaluate_if_statement(self, node):
        condition = self.evaluate(node.condition)
        if condition:
            for statement in node.if_body:
                self.evaluate(statement)

        elif node.else_body:
            if isinstance(node.else_body, IfStatement):
                self.evaluate_if_statement(node.else_body)

            else:
                for statement in node.else_body:
                    self.evaluate(statement)

    def evaluate_for_loop(self, node):
        self.evaluate(node.initializer)
        while self.evaluate(node.condition):
            for statement in node.body:
                self.evaluate(statement)
            self.evaluate(node.increment)

    def evaluate_while_loop(self, node):
        while True:
            for statement in node.body:
                self.evaluate(statement)
            if not self.evaluate(node.condition):
                break

    def evaluate_do_while_loop(self, node):
        while True:
            for statement in node.body:
                self.evaluate(statement)
            if not self.evaluate(node.condition):
                break

    def evaluate_function(self, node):
        self.global_scope[node.name.value] = node
        # print(f"Defined function: {node.name.value}")

    def evaluate_function_call(self, node):
        func_name = node.name
        if func_name not in self.global_scope:
            raise NameError(f"Function '{func_name}' is not defined.")
        
        function = self.global_scope[func_name]
        arguments = [self.evaluate(arg) for arg in node.parameters]

        if not hasattr(function, "parameters"):
            return function(*arguments)

        local_scope = {}
        for param, arg in zip(function.parameters, arguments):
            local_scope[param.name] = arg

        previous_scope = self.global_scope.copy()
        combined_scope = {**self.global_scope, **local_scope}
        self.global_scope = combined_scope

        result = None
        try:
            for statement in function.body:
                self.evaluate(statement)
        except ReturnException as ret:
            result = ret.value

        self.global_scope = previous_scope
        return result

    def evaluate_return_statement(self, node):
        value = self.evaluate(node.values[0]) if node.values else None
        raise ReturnException(value)

    def evaluate_identifier(self, node):
        if node.name not in self.global_scope:
            raise ValueError(f"'{node.name}' is not defined or has not been imported. Did you forget to import a library or create a class?")
        return self.global_scope[node.name]

    def evaluate_array_literal(self, node):
        # evaluate each element in the node
        elements = [self.evaluate(element) for element in node.elements]

        # check if larger than size
        if len(elements) > int(node.size):
            raise ValueError(f"Array size mismatch: expected {node.size}, got {len(elements)}")
        
        # afterwards, enforce type
        # print(f"Enforcing type for array: {elements}")
        for element in elements:
            self.enforce_type(node.type, element)

        return elements
    
    def evaluate_vector_literal(self, node):
        # evaluate each element in the node
        elements = [self.evaluate(element) for element in node.elements]
        
        # enforce type, dwb size
        # print(f"Enforcing type for array: {elements}")
        for element in elements:
            self.enforce_type(node.type, element)

        return elements

    def evaluate_class_literal(self, node):
        if node.parent:
            parent_class = self.evaluate(node.parent)
            node.env = dict(getattr(parent_class, 'env', {}))
        else:
            node.env = {}

        for field in node.fields:
            node.env[field.name] = None

        for method in node.methods:
            node.env[method.name.value] = method

        for stmt in node.body:
            self.evaluate(stmt)

        return node

    def evaluate_class_instantiation(self, node):
        typ = node.typ.value
        name = node.name.value
        if typ not in self.global_scope:
            raise NameError(f"Class '{typ}' not defined.")
        
        class_literal = self.global_scope[typ]
        instance = {
            '__class__': class_literal,
            'fields': dict(class_literal.env)
        }
        evaluated_args = [self.evaluate(arg) for arg in node.arguments]
        
        # if an initializer (__init__) is defined in the class, call it.
        if '__init__' in class_literal.env:
            init_method = class_literal.env['__init__']
            local_scope = {}
            local_scope[init_method.parameters[0].name] = instance

            for param, arg in zip(init_method.parameters[1:], evaluated_args):
                local_scope[param.name] = arg

            previous_scope = self.global_scope.copy()
            self.global_scope.update(local_scope)
            
            try:
                for stmt in init_method.body:
                    self.evaluate(stmt)
            except ReturnException as ret:
                pass
            self.global_scope = previous_scope

        self.global_scope[name] = instance
        return instance

    def evaluate_field_assignment(self, node):
        # Check if the parent is a Token; if so, handle it as an identifier.
        if isinstance(node.parent, Token):
            key = node.parent.value
            if key not in self.global_scope:
                raise ValueError(f"'{key}' is not defined.")
            instance = self.global_scope[key]
        else:
            instance = self.evaluate(node.parent)
        
        new_value = self.evaluate(node.value)
        
        # Extract the field name from the assignment.
        field_name = node.field.value if hasattr(node.field, "value") else node.field
        
        # Ensure the instance is a valid object (in our design, a dict with a 'fields' key).
        if not (isinstance(instance, dict) and "fields" in instance):
            raise TypeError("Field assignment target is not a valid instance.")
        
        instance["fields"][field_name] = new_value
        return new_value

    def evaluate_field_access(self, node):
        # Evaluate the parent node to get the instance.
        instance = self.evaluate(node.parent)
        # Ensure the instance is a valid object (in our design, a dict with a 'fields' key).
        if not (isinstance(instance, dict) and 'fields' in instance):
            raise TypeError("Field access target is not a valid instance.")
        
        # Determine the field name.
        if hasattr(node.field, 'name'):
            field_name = node.field.name  # For Identifier nodes.
        else:
            field_name = node.field  # For tokens.
        
        # Return the field's value, or None if not found.
        return instance['fields'].get(field_name, None)
    
    def evaluate_method_call(self, node):
        parent_obj = self.evaluate(node.parent)
        method_name = node.name.value if hasattr(node.name, "value") else node.name

        if isinstance(parent_obj, dict) and '__class__' in parent_obj:
            class_obj = parent_obj['__class__']
            if method_name not in class_obj.env:
                raise AttributeError(f"Class '{class_obj}' does not have a method '{method_name}'.")
            method_node = class_obj.env[method_name]
            evaluated_args = [self.evaluate(arg) for arg in node.parameters]

            local_scope = {}
            local_scope[method_node.parameters[0].name] = parent_obj

            for param, arg in zip(method_node.parameters[1:], evaluated_args):
                local_scope[param.name] = arg

            previous_scope = self.global_scope.copy()
            self.global_scope.update(local_scope)
            
            result = None
            try:
                for stmt in method_node.body:
                    result = self.evaluate(stmt)
            except ReturnException as ret:
                result = ret.value

            self.global_scope = previous_scope
            return result
        
        else:
            if hasattr(node.parent, "value"):
                package_name = node.parent.value
            elif hasattr(node.parent, "name"):
                package_name = node.parent.name
            else:
                raise ValueError("Invalid package identifier in MethodCall.")

            try:
                package_obj = self.global_scope[package_name]
            except KeyError:
                raise KeyError(f"Package: {package_name} not found in global scope")

            method_func = getattr(package_obj, method_name, None)
            if method_func is None:
                raise AttributeError(f"Package '{package_name}' does not have a method '{method_name}'.")
            
            args = [self.evaluate(arg) for arg in node.parameters]
            return method_func(*args)
    
    def evaluate_index_access(self, node):
        container = self.evaluate(node.container)
        index = self.evaluate(node.index)
        if not isinstance(container, list) and not isinstance(container, str):
            raise TypeError("Index access is only supported on lists or arrays.")
        try:
            return container[index]
        except IndexError:
            raise IndexError("Index out of range.")

    def evaluate_index_assignment(self, node):
        container = self.evaluate(node.container)
        index = self.evaluate(node.index)
        value = self.evaluate(node.value)
        if not isinstance(container, list):
            raise TypeError("Index access is only supported on lists or arrays.")
        try:
            container[index] = value
            return value
        except IndexError:
            raise IndexError("Index out of range.")