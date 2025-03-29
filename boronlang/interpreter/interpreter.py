# tokentype from my lexer and all ASTNodes from parser
from lexer.lexer import TokenType, Token
from parsing.astnodes import *

# decimal import for better precision, fuck floats no floats in my language
from decimal import Decimal
# importlib and os for package support
import importlib.util, os, sys
from rich import print  # colored prints

# builtin functions
from interpreter.builtins import BUILTINS

class Interpreter:
    def __init__(self, args=[]):
        # initialize a global scope and the package folder (locally for right now)
        self.global_scope = {}
        self.package_folder = "C:\\Users\\fuzio\\Downloads\\programs\\showcase\\Boron\\packages"
        self.global_scope.update(BUILTINS)

        # figure out how to do something with these
        self.cliargs = args

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
    
    def create_callback(self, func_node):
        def callback():
            func_name = func_node.name.value if hasattr(func_node.name, "value") else func_node.name
            function_call_node = FunctionCall(func_name, [], {})
            self.evaluate_function_call(function_call_node)
        return callback

    # loading for packages, packages are just .py files for right now, full python libraries soon
    def evaluate_import(self, node):
        module_name = node.module
        package_path = os.path.join(self.package_folder, module_name)

        # Check if it's a package with an __init__.py
        init_path = os.path.join(package_path, "__init__.py")
        single_file_path = os.path.join(self.package_folder, f"{module_name}.py")

        if os.path.isdir(package_path) and os.path.exists(init_path):
            # Import as a package (folder with __init__.py)
            spec = importlib.util.spec_from_file_location(module_name, init_path)
        elif os.path.exists(single_file_path):
            # Import as a single-file module (Package.py)
            spec = importlib.util.spec_from_file_location(module_name, single_file_path)
        else:
            raise ImportError(f"Package '{module_name}' not found in '{self.package_folder}'.")

        # Load and execute the module
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module  # Ensure it's registered in sys.modules
        spec.loader.exec_module(module)

        # Handle aliasing (if any)
        module_name = node.alias or module_name
        self.global_scope[module_name] = module

        # Add all classes and functions from the module to the global scope
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) or callable(attr):  # Classes & functions
                self.global_scope[attr_name] = attr
    
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
        evaluated_args = [self.evaluate(arg) for arg in node.parameters]
        evaluated_kwargs = {key: self.evaluate(value) for key, value in node.kwargs.items()} if hasattr(node, 'kwargs') else {}

        evaluated_args = [
                self.create_callback(arg) if hasattr(arg, "parameters") and hasattr(arg, "body") else arg
                for arg in evaluated_args
            ]

        for key, value in evaluated_kwargs.items():
            if key == "command" and hasattr(value, "parameters") and hasattr(value, "body"):
                evaluated_kwargs[key] = self.create_callback(value)

        # If it's a native Python function, call it with both args and kwargs.
        if not hasattr(function, "parameters"):
            return function(*evaluated_args, **evaluated_kwargs)
        
        # Otherwise, assume it's a user-defined function.
        local_scope = {}
        param_names = [param.name for param in function.parameters]
        # Bind positional arguments first, then keyword arguments.
        for i, param in enumerate(function.parameters):
            if i < len(evaluated_args):
                local_scope[param.name] = evaluated_args[i]
            elif param.name in evaluated_kwargs:
                local_scope[param.name] = evaluated_kwargs[param.name]
            else:
                raise TypeError(f"Missing argument for parameter '{param.name}'")
        # Check for any unexpected keyword arguments.
        for key in evaluated_kwargs:
            if key not in param_names:
                raise TypeError(f"Unexpected keyword argument '{key}'")
        
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
        evaluated_args = [self.evaluate(arg) for arg in node.arguments]
        evaluated_kwargs = {key: self.evaluate(value) for key, value in node.kwargs.items()} if hasattr(node, 'kwargs') else {}

        evaluated_args = [
            self.create_callback(arg) if hasattr(arg, "parameters") and hasattr(arg, "body") else arg
            for arg in evaluated_args
        ]
                
        for key, value in evaluated_kwargs.items():
            if key == "command" and hasattr(value, "parameters") and hasattr(value, "body"):
                evaluated_kwargs[key] = self.create_callback(value)

        # For native Python classes, instantiate with both args and kwargs.
        if isinstance(class_literal, type):
            instance = class_literal(*evaluated_args, **evaluated_kwargs)
            self.global_scope[name] = instance
            return instance

        # Otherwise, assume it's a language-defined class.
        instance = {
            '__class__': class_literal,
            'fields': dict(class_literal.env)
        }
        
        # Call the initializer (__init__) if defined.
        if '__init__' in class_literal.env:
            init_method = class_literal.env['__init__']
            local_scope = {}
            local_scope[init_method.parameters[0].name] = instance

            param_names = [param.name for param in init_method.parameters]
            # Bind positional and keyword arguments for __init__ (skip the first parameter, typically self).
            for i, param in enumerate(init_method.parameters[1:]):
                if i < len(evaluated_args):
                    local_scope[param.name] = evaluated_args[i]
                elif param.name in evaluated_kwargs:
                    local_scope[param.name] = evaluated_kwargs[param.name]
                else:
                    raise TypeError(f"Missing argument for parameter '{param.name}' in __init__")
            for key in evaluated_kwargs:
                if key not in param_names:
                    raise TypeError(f"Unexpected keyword argument '{key}' in __init__")
            
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
            evaluated_kwargs = {key: self.evaluate(value) for key, value in node.kwargs.items()} if hasattr(node, 'kwargs') else {}

            evaluated_args = [
                self.create_callback(arg) if hasattr(arg, "parameters") and hasattr(arg, "body") else arg
                for arg in evaluated_args
            ]

            for key, value in evaluated_kwargs.items():
                if key == "command" and hasattr(value, "parameters") and hasattr(value, "body"):
                    evaluated_kwargs[key] = self.create_callback(value)

            local_scope = {}
            local_scope[method_node.parameters[0].name] = parent_obj
            param_names = [param.name for param in method_node.parameters]
            # Bind positional and keyword arguments (skip the first parameter which is self).
            for i, param in enumerate(method_node.parameters[1:]):
                if i < len(evaluated_args):
                    local_scope[param.name] = evaluated_args[i]
                elif param.name in evaluated_kwargs:
                    local_scope[param.name] = evaluated_kwargs[param.name]
                else:
                    raise TypeError(f"Missing argument for parameter '{param.name}' in method '{method_name}'")
            for key in evaluated_kwargs:
                if key not in param_names:
                    raise TypeError(f"Unexpected keyword argument '{key}' in method '{method_name}'")
            
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
            kwargs = {key: self.evaluate(value) for key, value in node.kwargs.items()} if hasattr(node, 'kwargs') else {}
            return method_func(*args, **kwargs)

    
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