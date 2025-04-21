# importing everything individually because i wanna know if its all used
# lexer import
from lexer.lexer import Token, TokenType
# important nodes
from parsing.astnodes import Program, Import, Imports, EndOfFile
# class and function nodes
from parsing.astnodes import Function, NativeFunction, FunctionCall, MethodCall, Parameter, ReturnStatement, FieldAccess, FieldAssignment, ClassInstantiation
# operation nodes
from parsing.astnodes import BinaryOperation, LogicalOperation, UnaryOperation, IndexAccess, IndexAssignment
# control flow nodes
from parsing.astnodes import IfStatement, ForLoop, WhileLoop, DoWhileLoop, Break, TryStatement, CatchStatement, RaiseStatement
# variable nodes
from parsing.astnodes import VariableDeclaration, Identifier, StringLiteral, BooleanLiteral, IntLiteral, DecLiteral, ListLiteral, ArrayLiteral, RangeLiteral, ClassLiteral, VectorLiteral, DictLiteral, NoneObject
# scope
from parsing.scope import Scope

# disable or enable repr
global reprenabled 
reprenabled = False

# the actual parser, also the guts of this shit
class Parser:
    # initialize it with the tokens from the lexer, start the position at 0, and the line at 1
    # also initialize the scope
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.line = 1
        self.scope = Scope()

    # gets the current token from the list of tokens
    def current_token(self):
        return self.tokens[self.pos]

    # gets next token
    def next_token(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    # expects a specific token and if not throws a syntax error
    def expect(self, token_type):
        token = self.current_token()
        if token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, but found {token.type}. Specific token afflicted: {token}")
        self.next_token()
        return token
    
    # peeks at the offset value index, gets token without consuming it
    def peek(self, offset=1):
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return None
    
    # passes all tokens until not eol
    def skipeols(self):
        while self.current_token().type == TokenType.EOL:
            self.next_token()

    # the actual function that parses, recursively feeds tokens thru parse_statement
    def parse(self):
        if reprenabled == True: print("REPR: ")
        program = Program()
        while self.current_token().type != TokenType.EOF:
            program.statements.append(self.parse_statement())
        if reprenabled == True: print()
        return program

    # the function that gets fed through a million times, maps everything to a dispatch (passing eols), and if not raises a syntax error
    def parse_statement(self):
        token = self.current_token()
        while token.type == TokenType.EOL:
            self.line += 1
            token = self.next_token()

        # big boy table that maps everything to each function
        dispatch_table = {
            TokenType.IMPORT: self.parse_import,
            TokenType.INTEGER: self.parse_variable_declaration,
            TokenType.BOOLEAN: self.parse_variable_declaration,
            TokenType.STR: self.parse_variable_declaration,
            TokenType.TUPLE: self.parse_variable_declaration,
            TokenType.LIST: self.parse_variable_declaration,
            TokenType.SET: self.parse_variable_declaration,
            TokenType.DEC: self.parse_variable_declaration,
            TokenType.AUTO: self.parse_variable_declaration,
            TokenType.RANGE: self.parse_range_declaration,
            TokenType.ARRAY: self.parse_array_declaration,
            TokenType.VECTOR: self.parse_vector_declaration,
            TokenType.DICT: self.parse_dictionary_declaration,
            TokenType.CLASS: self.parse_class_declaration,
            TokenType.GLOBAL: self.parse_global_declaration,
            TokenType.IDENTIFIER: self.parse_identifier,
            TokenType.FUNCTION: self.parse_function,
            TokenType.IF: self.parse_if_statement,
            TokenType.FOR: self.parse_for_loop,
            TokenType.WHILE: self.parse_while_loop,
            TokenType.DO: self.parse_do_while_loop,
            TokenType.RETURN: self.parse_return_statement,
            TokenType.NATIVE: self.parse_native_function,
            TokenType.TRY: self.parse_try_statement,
            TokenType.RAISE: self.parse_raise_statement,
            TokenType.CATCH: self.parse_catch_statement,
            TokenType.BREAK: lambda: Break(),
            TokenType.EOF: lambda: EndOfFile()
        }

        if token.type in dispatch_table:
            return dispatch_table[token.type]()
        else:
            raise SyntaxError(f"Unexpected token {token.type}")
  
    
    # parses blocks correctly, will in fact be using
    def parse_block(self):
        self.skipeols()
        self.expect(TokenType.LEFT_BRACE)
        statements = []
        self.skipeols()

        while self.current_token().type != TokenType.RIGHT_BRACE:
            self.skipeols()
            if self.current_token().type == TokenType.RIGHT_BRACE:
                break
            statements.append(self.parse_statement())
            
        self.expect(TokenType.RIGHT_BRACE)
        return statements

    # you guessed it, parses variable declarations
    def parse_variable_declaration(self):
        type_token = self.expect(self.current_token().type)
        var_type = type_token.type
        if not isinstance(type_token.value, Token) or type_token.value.type != TokenType.IDENTIFIER:
            raise SyntaxError(f"Expected an identifier after type declaration, but found {type_token.value}")
        
        name = type_token.value.value
        if self.current_token().type in [TokenType.EOL, TokenType.SEMICOLON]:
            value = None
            self.next_token()
        else: 
            self.expect(TokenType.ASSIGN)
            value = self.parse_expression()

        if self.scope.is_declared(name):
            raise SyntaxError(f"Variable '{name}' already declared in this scope.")

        self.scope.declare_variable(name, var_type)

        if reprenabled == True: print(repr(VariableDeclaration(var_type, name, value)))
        return VariableDeclaration(var_type, name, value)


    def parse_range_declaration(self):
        # add support for variable ranges
        name = self.current_token().value

        if self.scope.is_declared(name):
            raise SyntaxError(f"Variable '{name}' already declared in this scope.")

        self.next_token()
        self.next_token()
        self.expect(TokenType.LEFT_PAREN)
        start = self.expect(TokenType.NUMBER).value
        self.expect(TokenType.COMMA)
        stop = self.expect(TokenType.NUMBER).value
        self.expect(TokenType.COMMA)
        increment = self.expect(TokenType.NUMBER).value
        self.expect(TokenType.RIGHT_PAREN)
        self.scope.declare_variable(name, TokenType.RANGE)

        if reprenabled == True: print(repr(VariableDeclaration(TokenType.RANGE, name, RangeLiteral(IntLiteral(start), IntLiteral(stop), IntLiteral(increment)))))
        return VariableDeclaration(TokenType.RANGE, name, RangeLiteral(IntLiteral(start), IntLiteral(stop), IntLiteral(increment)))
    

    def parse_array_declaration(self):
        elements = []
        name = self.current_token().value.value

        if self.scope.is_declared(name):
            raise SyntaxError(f"Variable '{name}' already declared in this scope.")

        self.scope.declare_variable(name, TokenType.ARRAY)
        arraytype = self.current_token().type
        self.next_token()
        self.expect(TokenType.LEFT_BRACKET)
        typ = self.expect(self.current_token().type).type
        self.expect(TokenType.RIGHT_BRACKET)
        self.expect(TokenType.LEFT_BRACKET)
        size = self.expect(TokenType.NUMBER).value
        self.expect(TokenType.RIGHT_BRACKET)
        self.expect(TokenType.ASSIGN)
        self.expect(TokenType.LEFT_BRACKET)
        while self.current_token().type != TokenType.RIGHT_BRACKET:
            elements.append(self.parse_expression())
            if self.current_token().type == TokenType.COMMA:
                self.next_token()

        self.expect(TokenType.RIGHT_BRACKET)
        if reprenabled == True: print(repr(VariableDeclaration(arraytype, Identifier(name), ArrayLiteral(typ, size, elements))))
        return VariableDeclaration(arraytype, Identifier(name), ArrayLiteral(typ, size, elements))
    

    def parse_vector_declaration(self):
        elements = []
        name = self.current_token().value.value

        if self.scope.is_declared(name):
            raise SyntaxError(f"Variable '{name}' already declared in this scope.")

        self.scope.declare_variable(name, TokenType.VECTOR)
        arraytype = self.current_token().type
        self.next_token()
        self.expect(TokenType.LEFT_BRACKET)
        typ = self.expect(self.current_token().type).type
        self.expect(TokenType.RIGHT_BRACKET)
        self.expect(TokenType.ASSIGN)
        self.expect(TokenType.LEFT_BRACKET)
        while self.current_token().type != TokenType.RIGHT_BRACKET:
            elements.append(self.parse_expression())
            if self.current_token().type == TokenType.COMMA:
                self.next_token()

        self.expect(TokenType.RIGHT_BRACKET)
        if reprenabled == True: print(repr(VariableDeclaration(arraytype, Identifier(name), VectorLiteral(typ, elements))))
        return VariableDeclaration(arraytype, Identifier(name), VectorLiteral(typ, elements))
        

    def parse_identifier(self):
        # add more scope here
        cur = self.current_token()
        name = cur.value
        
        next_token = self.peek()
        
        if next_token:
            if next_token.type in {
                TokenType.INCREASE, TokenType.DECREASE, TokenType.MULTEQ,
                TokenType.DIVEQ, TokenType.POWEQ, TokenType.FLOOREQ,
            }:
                # compound assignments (ex. +=, -=, /=, **=, //=)
                self.next_token()
                operator = next_token.type
                self.next_token()
                new_value = self.parse_expression()
                if isinstance(new_value, Identifier):
                    if reprenabled == True: print(repr(BinaryOperation(name, operator, Identifier(new_value))))
                    return BinaryOperation(name, operator, Identifier(new_value))

                if reprenabled == True: print(repr(BinaryOperation(Identifier(name), operator, new_value)))
                return BinaryOperation(Identifier(name), operator, new_value)
            
            # array/list/vector accesses
            elif next_token.type == TokenType.LEFT_BRACKET:
                self.next_token()
                self.next_token()
                index_expr = self.parse_expression()
                self.expect(TokenType.RIGHT_BRACKET)

                # also check for assignments
                if self.current_token().type == TokenType.ASSIGN:
                    self.next_token()
                    assignment_value = self.parse_expression()
                    return IndexAssignment(Identifier(name), index_expr, assignment_value)
                
                elif self.current_token().type == TokenType.PERIOD:
                    self.next_token()
                    property_or_method = self.current_token().value
                    self.next_token()
                    if self.current_token().type == TokenType.LEFT_PAREN:
                        return MethodCall(IndexAccess(Identifier(name), index_expr), property_or_method, [])
                    else:
                        raise SyntaxError(f"Expected '(' after method name '{property_or_method}'")

                return IndexAccess(Identifier(name), index_expr)
            
            elif next_token.type in [TokenType.INCREMENT, TokenType.DECREMENT]:
                self.next_token()
                operator = next_token.type
                self.next_token()
                if reprenabled == True: print(repr(UnaryOperation(Identifier(name), operator)))
                return UnaryOperation(Identifier(name), operator)
            
            elif next_token.type == TokenType.ASSIGN:
                self.next_token()  # consume the ASSIGN token
                self.next_token()

                if not self.scope.is_declared(name):
                    raise SyntaxError(f"Variable '{name}' not declared in this scope. Declare the variable to operate on it.")
                
                right = self.parse_expression()
                var_type = self.scope.get_variable_type(name)
                
                if reprenabled == True: print(repr(VariableDeclaration(var_type, Identifier(name), right)))
                return VariableDeclaration(var_type, Identifier(name), right)
            
            elif next_token.type == TokenType.PERIOD:
                # Instead of using the raw token, wrap it as an Identifier
                parent = Identifier(self.current_token().value)
                self.next_token()  # Consume the token for the parent
                self.next_token()  # Skip the PERIOD
                property_or_method = self.current_token().value
                self.next_token()  # Consume the method/field name

                if self.current_token().type == TokenType.LEFT_PAREN:
                    self.expect(TokenType.LEFT_PAREN)
                    arguments = []
                    kwargs = {}
                    while self.current_token().type != TokenType.RIGHT_PAREN:
                        # If an identifier is followed by an ASSIGN, treat it as a keyword argument.
                        if self.current_token().type == TokenType.IDENTIFIER:
                            next_token = self.peek()
                            if next_token and next_token.type == TokenType.ASSIGN:
                                key = self.current_token().value
                                self.next_token()  # consume the identifier
                                self.expect(TokenType.ASSIGN)  # consume the '='
                                value = self.parse_expression()
                                kwargs[key] = value
                            else:
                                arguments.append(self.parse_expression())
                        else:
                            arguments.append(self.parse_expression())
                        if self.current_token().type == TokenType.COMMA:
                            self.next_token()
                    self.expect(TokenType.RIGHT_PAREN)
                    if reprenabled == True: 
                        print(repr(MethodCall(parent, property_or_method, arguments, kwargs)))
                    return MethodCall(parent, property_or_method, arguments, kwargs)

                elif self.current_token().type == TokenType.ASSIGN:
                    self.next_token()
                    value = self.parse_expression()
                    if reprenabled == True: print(repr(FieldAssignment(parent, property_or_method, value)))
                    return FieldAssignment(parent, property_or_method, value)

                else:
                    if reprenabled == True: print(repr(FieldAccess(parent, property_or_method)))
                    return FieldAccess(parent, property_or_method)

            elif next_token.type == TokenType.IDENTIFIER:
                typ = self.expect(TokenType.IDENTIFIER)
                name = self.expect(TokenType.IDENTIFIER)
                self.expect(TokenType.ASSIGN)

                # check if the instantiation uses the 'new' keyword.
                if self.current_token().type == TokenType.NEW:
                    self.expect(TokenType.NEW)
                    self.expect(TokenType.IDENTIFIER)  # expect the class identifier after NEW
                    
                    if self.current_token().type == TokenType.LEFT_PAREN:
                        arguments = []
                        kwargs = {}
                        self.expect(TokenType.LEFT_PAREN)

                        while self.current_token().type != TokenType.RIGHT_PAREN:
                            if self.current_token().type == TokenType.IDENTIFIER:
                                next_token = self.peek()
                                if next_token and next_token.type == TokenType.ASSIGN:
                                    key = self.current_token().value
                                    self.next_token()
                                    self.expect(TokenType.ASSIGN)
                                    value = self.parse_expression()
                                    kwargs[key] = value
                                else:
                                    arguments.append(self.parse_expression())
                            else:
                                arguments.append(self.parse_expression())

                            if self.current_token().type == TokenType.COMMA:
                                self.next_token()
                                
                        self.expect(TokenType.RIGHT_PAREN)
                    return ClassInstantiation(typ, name, arguments, kwargs)
                else:
                    # instead of using new, parse the expression normally (e.g., pattern.findall(...))
                    expr = self.parse_expression()
                    return ClassInstantiation(typ, name, [expr], {})

            elif next_token.type == TokenType.LEFT_PAREN:
                self.next_token()
                return self.parse_function_call(name)
            
            elif next_token.type == TokenType.LEFT_BRACKET:
                self.next_token()
                # why is this here
      
        # if no operator follows assume variable reference
        self.next_token()
        if reprenabled == True: print(repr(Identifier(name)))
        return Identifier(name)
    

    def parse_function_call(self, name):
        self.expect(TokenType.LEFT_PAREN)
        arguments = []
        kwargs = {}
        # Parse each argument until we reach the closing parenthesis
        while self.current_token().type != TokenType.RIGHT_PAREN:
            # Check if the argument is a keyword argument (identifier followed by ASSIGN)
            if self.current_token().type == TokenType.IDENTIFIER:
                next_token = self.peek()
                if next_token and next_token.type == TokenType.ASSIGN:
                    key = self.current_token().value  # the keyword name
                    self.next_token()  # consume the identifier
                    self.expect(TokenType.ASSIGN)  # consume the '='
                    value = self.parse_expression()
                    kwargs[key] = value
                else:
                    # Positional argument
                    arguments.append(self.parse_expression())
            else:
                arguments.append(self.parse_expression())
            
            if self.current_token().type == TokenType.COMMA:
                self.next_token()
                
        self.expect(TokenType.RIGHT_PAREN)
        return FunctionCall(name, arguments, kwargs)


    def parse_import(self):
        import_token = self.expect(TokenType.IMPORT)  # Expect IMPORT keyword
        imports = []

        if self.current_token().type == TokenType.LEFT_BRACE:
            self.next_token()  # Consume `{`

            while self.current_token().type != TokenType.RIGHT_BRACE:
                if self.current_token().type != TokenType.IDENTIFIER:
                    raise SyntaxError(f"Invalid import statement: Expected an identifier, found {self.current_token()}")

                module_name = self.current_token().value
                alias = module_name  # Default alias is the same as module

                self.next_token()  # Move to next token

                if self.current_token().type == TokenType.AS:
                    if self.current_token().value.type != TokenType.IDENTIFIER:
                        raise SyntaxError(f"Invalid alias: Expected an identifier after 'as', found {self.current_token()}")

                    alias = self.current_token().value.value
                    self.next_token()  # Move past alias identifier

                imports.append(Import(module_name, alias))  # Store Import object

                if self.current_token().type == TokenType.COMMA:
                    self.next_token()  # Consume `,` and move to the next identifier

            self.expect(TokenType.RIGHT_BRACE)  # Expect closing `}`

            # Declare all imports
            for imp in imports:
                if self.scope.is_imported(imp.module):
                    raise SyntaxError(f"Variable '{imp.module}' already declared in this scope.")
                self.scope.declare_import(imp.module, imp.alias)

            if reprenabled:
                print(repr(Imports(imports)))  # Print list of Import objects

            return Imports(imports)  # Return list of Import nodes
        
        elif self.current_token().type == TokenType.PERIOD:
            self.next_token()
            if self.current_token().type != TokenType.IDENTIFIER:
                raise SyntaxError(f"Invalid import statement: Expected an identifier after '.', found {self.current_token()}")
            
            class_name = self.current_token().value
            alias = class_name

            if self.current_token().type == TokenType.AS:
                if self.current_token().value.type != TokenType.IDENTIFIER:
                    raise SyntaxError(f"Invalid alias: Expected an identifier after 'as', found {self.current_token()}")

                alias = self.current_token().value.value
                self.next_token()

            print(repr(Import(class_name, alias, import_token.value.value)))
            return Import(class_name, alias, import_token.value.value)

        if not isinstance(import_token.value, Token) or import_token.value.type != TokenType.IDENTIFIER:
            raise SyntaxError(f"Invalid import statement: Expected an identifier, found {import_token.value}")

        alias = import_token.value.value
        if self.current_token().type == TokenType.AS:
            if self.current_token().value.type != TokenType.IDENTIFIER:
                raise SyntaxError(f"Invalid alias: Expected an identifier, found {self.current_token()}")
            alias = self.current_token().value.value
            self.next_token()

        module = import_token.value.value
        if self.scope.is_imported(module):
            raise SyntaxError(f"Variable '{module}' already declared in this scope.")

        self.scope.declare_import(module, alias)

        if reprenabled:
            print(repr(Import(module, alias)))

        return Import(module, alias)
    
    def parse_dictionary_declaration(self):
        name = self.expect(TokenType.DICT).value.value
        if self.scope.is_declared(name):
            raise SyntaxError(f"Variable '{name}' already declared in this scope.")
        
        self.scope.declare_variable(name, TokenType.DICT)
        self.expect(TokenType.ASSIGN)
        self.expect(TokenType.LEFT_BRACE)
        elements = {}
        
        while self.current_token().type != TokenType.RIGHT_BRACE:
            if self.current_token().type == TokenType.EOL:
                self.next_token()
            if self.current_token().type in [TokenType.NUMBER, TokenType.STRING]:
                key = self.parse_expression()
                self.expect(TokenType.COLON)
                value = self.parse_expression()
                elements[key] = value

            if self.current_token().type == TokenType.COMMA:
                self.next_token()

        self.expect(TokenType.RIGHT_BRACE)
        if reprenabled == True: print(repr(VariableDeclaration(TokenType.DICT, name, DictLiteral(elements))))
        return VariableDeclaration(TokenType.DICT, name, DictLiteral(elements))


    def parse_class_declaration(self):
        # initialize all of this shit at the top
        extends, children, fields, methods, body = [], [], [], [], []

        name = self.current_token().value
        if self.scope.is_declared(name):
            raise SyntaxError(f"Class '{name}' already declared in this scope.")
        
        self.scope.declare_variable(name, TokenType.CLASS)
        self.next_token()

        # check if next token is an extends token, and get the class inside that
        if self.current_token().type == TokenType.EXTENDS:
            extends.append(self.current_token().value)
            self.next_token()

        # expect opening brace
        self.expect(TokenType.LEFT_BRACE)
        
        # enter a new scope for the class body.
        self.scope.enter_scope()
        
        # process class body until we hit RIGHT_BRACE.
        while self.current_token().type != TokenType.RIGHT_BRACE:
            self.skipeols()
            if self.current_token().type == TokenType.RIGHT_BRACE:
                break

            # parse class members: fields, methods, inner classes, or statements.
            if self.current_token().type in [TokenType.INTEGER, TokenType.BOOLEAN, TokenType.STR, 
                                            TokenType.LIST, TokenType.VECTOR, TokenType.SET, TokenType.TUPLE]:
                fields.append(self.parse_variable_declaration())

            elif self.current_token().type == TokenType.FUNCTION:
                methods.append(self.parse_function())

            elif self.current_token().type == TokenType.CLASS:
                child = self.parse_class_declaration()
                children.append(child)

            else:
                body.append(self.parse_statement())

        # exit class scope.
        self.scope.exit_scope()
        self.expect(TokenType.RIGHT_BRACE)
        
        if reprenabled == True: print(repr(VariableDeclaration(TokenType.CLASS, name, 
            ClassLiteral(name, extends, children, fields, methods, body))))
        return VariableDeclaration(
            TokenType.CLASS, name, 
            ClassLiteral(name, extends, children, fields, methods, body)
        )


    def parse_function(self):
        name = self.expect(TokenType.FUNCTION).value
        if self.scope.is_declared(name):
            raise SyntaxError(f"Function '{name}' already declared in this scope.")
        
        self.scope.declare_variable(name, TokenType.FUNCTION)
        self.scope.enter_scope()
        self.expect(TokenType.LEFT_PAREN)
        parameters = []
        while self.current_token().type != TokenType.RIGHT_PAREN:
            param_token = self.expect(self.current_token().type)
            if not isinstance(param_token.value, Token) or param_token.value.type != TokenType.IDENTIFIER:
                raise SyntaxError(f"Expected parameter with type and identifier, but found {param_token.value}")
            param_type = param_token.type
            param_name = param_token.value.value
            parameters.append(Parameter(param_type, param_name))
            self.scope.declare_variable(param_name, param_type)
            if self.current_token().type == TokenType.COMMA:
                self.next_token()
                
        self.expect(TokenType.RIGHT_PAREN)
        return_type = self.expect(TokenType.RETURN).value
        body = self.parse_block()  # use the block parser
        self.scope.exit_scope()
        return Function(name, parameters, return_type, body)
    

    # actually implement scope on this later, for right now just do this
    def parse_global_declaration(self):
        self.expect(TokenType.GLOBAL)

        if self.current_token().type in [TokenType.INTEGER, TokenType.BOOLEAN, TokenType.STR,
                                        TokenType.TUPLE, TokenType.LIST, TokenType.VECTOR, TokenType.SET, TokenType.DEC]:
            var_decl = self.parse_variable_declaration()
            return var_decl
        else:
            raise SyntaxError("Expected a type declaration after the 'global' keyword.")


    def parse_expression(self):
        # the big boy, parses almost every expression, pretty much as hot as the main function
        # handles literals, identifiers, binary operations, and logical operations. so literally everything
        def parse_primary():
            # for the primary token, like a number, string, or identifier.
            token = self.current_token()
            if token.type == TokenType.NUMBER:
                self.next_token()
                return IntLiteral(token.value)
            elif token.type == TokenType.DECIMAL:
                self.next_token()
                return DecLiteral(token.value)
            elif token.type == TokenType.STRING:
                self.next_token()
                return StringLiteral(token.value)
            elif token.type in [TokenType.TRUE, TokenType.FALSE]:
                value = token.value
                self.next_token()
                return BooleanLiteral(value)
            elif token.type == TokenType.IDENTIFIER:
                return self.parse_identifier()
            elif token.type == TokenType.LEFT_BRACKET:
                return self.parse_list_literal()
            elif token.type == TokenType.NOT:
                operator = token.type
                self.next_token()
                operand = parse_primary()
                return UnaryOperation(operand, operator)
            elif token.type == TokenType.LEFT_PAREN:
                self.next_token()
                expr = self.parse_expression()
                self.expect(TokenType.RIGHT_PAREN)
                return expr
            elif token.type == TokenType.UNTERMINATED_STRING:
                raise SyntaxError(f"Unterminated string: {token.value}")
            elif token.type == TokenType.NONE:
                self.next_token()
                return NoneObject()
            else:
                raise SyntaxError(f"Unexpected token in expression: {token.type}")


        def parse_binary(left, precedence=0):
            while True:
                operator = self.current_token().type
                if operator in [TokenType.EOL, TokenType.SEMICOLON, None]:
                    return left

                if operator in [TokenType.ADD, TokenType.SUBTRACT]:
                    current_precedence = 10
                elif operator in [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.FLOOR_DIVIDE, TokenType.MODULUS]:
                    current_precedence = 20
                elif operator == TokenType.POWER:
                    current_precedence = 30
                elif operator in [TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.GREATER_THAN, TokenType.LESS_THAN, TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL]:
                    current_precedence = 5
                elif operator == TokenType.AND:
                    current_precedence = 3
                elif operator == TokenType.OR:
                    current_precedence = 2
                else:
                    break

                if current_precedence < precedence:
                    return left

                self.next_token()
                right = parse_primary()

                while self.current_token().type not in [TokenType.EOL, TokenType.SEMICOLON, None]:
                    next_operator = self.current_token().type
                    if next_operator in [TokenType.ADD, TokenType.SUBTRACT]:
                        next_precedence = 10
                    elif next_operator in [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.FLOOR_DIVIDE, TokenType.MODULUS]:
                        next_precedence = 20
                    elif next_operator == TokenType.POWER:
                        next_precedence = 30
                    elif next_operator in [TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.GREATER_THAN, TokenType.LESS_THAN, TokenType.LESS_THAN, TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL]:
                        next_precedence = 5
                    elif next_operator == TokenType.AND:
                        next_precedence = 3
                    elif next_operator == TokenType.OR:
                        next_precedence = 2
                    else:
                        break

                    if next_precedence > current_precedence:
                        right = parse_binary(right, next_precedence)
                    else:
                        break

                left = BinaryOperation(left, operator, right)
            return left

        primary = parse_primary()
        return parse_binary(primary, precedence=0)


    def parse_if_statement(self):
        self.expect(TokenType.IF)
        condition = self.parse_expression()
        if_body = self.parse_block()  # reuse parse_block for the if body

        else_body = None
        last_else_if = None
        self.skipeols()

        while self.current_token().type == TokenType.ELSE_IF:
            self.next_token()
            else_if_condition = self.parse_expression()
            else_if_body = self.parse_block()
            else_if_statement = IfStatement(else_if_condition, else_if_body, None)
            if last_else_if:
                last_else_if.else_body = else_if_statement
            else:
                else_body = else_if_statement
            last_else_if = else_if_statement
            self.skipeols()
        
        self.skipeols()

        if self.current_token().type == TokenType.ELSE:
            self.skipeols()
            self.next_token()
            final_else_body = self.parse_block()
            if last_else_if:
                last_else_if.else_body = final_else_body
            else:
                else_body = final_else_body

        return IfStatement(condition, if_body, else_body)


    def parse_for_loop(self):
        self.expect(TokenType.FOR)

        """
        if self.peek().type == TokenType.IDENTIFIER:
            if self.scope.is_declared(self.peek().value):
                pass
            else:
                raise SyntaxError(f"Variable '{self.peek().value}' not declared in this scope. Declare the variable to use it as a range.")
        """
        self.expect(TokenType.LEFT_PAREN)
        self.scope.enter_scope()

        initializer = self.parse_statement()
        self.expect(TokenType.SEMICOLON)

        condition = self.parse_expression()
        self.expect(TokenType.SEMICOLON)

        increment = self.parse_expression()
        self.expect(TokenType.RIGHT_PAREN)
        body = self.parse_block()

        self.scope.exit_scope()
        if reprenabled == True: print(repr(ForLoop(initializer, condition, increment, body)))
        return ForLoop(initializer, condition, increment, body)


    def parse_while_loop(self):
        self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        body = self.parse_block()
        if reprenabled == True: print(repr(WhileLoop(condition, body)))
        return WhileLoop(condition, body)


    def parse_do_while_loop(self):
        self.expect(TokenType.DO)
        body = self.parse_block()
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LEFT_PAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RIGHT_PAREN)
        if reprenabled == True: print(repr(DoWhileLoop(body, condition)))
        return DoWhileLoop(body, condition)


    def parse_list_literal(self):
        elements = []
        self.expect(TokenType.LEFT_BRACKET)
        
        # reused
        while self.current_token().type != TokenType.RIGHT_BRACKET:
            elements.append(self.parse_expression())
            if self.current_token().type == TokenType.COMMA:
                self.next_token()

        self.expect(TokenType.RIGHT_BRACKET)
        if reprenabled == True: print(repr(ListLiteral(elements)))
        return ListLiteral(elements)


    def parse_return_statement(self):
        self.expect(TokenType.RETURN)
        values = []
        if self.current_token().type not in (TokenType.SEMICOLON, TokenType.EOL):
            while True:
                values.append(self.parse_expression())
                if self.current_token().type != TokenType.COMMA:
                    break
                self.expect(TokenType.COMMA)
        
        if self.current_token().type in (TokenType.SEMICOLON, TokenType.EOL):
            self.next_token()
        
        if reprenabled == True: print(repr(ReturnStatement(values)))
        return ReturnStatement(values)
    

    def parse_native_function(self):
        self.expect(TokenType.NATIVE)
        name = self.expect(TokenType.IDENTIFIER).value

        if self.scope.is_declared(name):
            raise SyntaxError(f"Function '{name}' already declared in this scope.")
        
        self.scope.declare_variable(name, TokenType.NATIVE)
        self.expect(TokenType.LEFT_PAREN)

        parameters = []
        while self.current_token().type != TokenType.RIGHT_PAREN:
            param_token = self.expect(self.current_token().type)
            if not isinstance(param_token.value, Token) or param_token.value.type != TokenType.IDENTIFIER:
                raise SyntaxError(f"Expected parameter with type and identifier, but found {param_token.value}")
            param_type = param_token.type
            param_name = param_token.value.value
            parameters.append(Parameter(param_type, param_name))
            if self.current_token().type == TokenType.COMMA:
                self.next_token()

        self.expect(TokenType.RIGHT_PAREN)
        return_type = self.expect(TokenType.RETURN).value
        body = self.parse_block()
        if reprenabled == True: print(repr(NativeFunction(name, parameters, return_type, body)))
        return NativeFunction(name, parameters, return_type, body)
    
    def parse_try_statement(self):
        self.expect(TokenType.TRY)
        try_body = self.parse_block()  # Parse the try block

        self.skipeols()

        catch_map = {}
        while self.current_token().type == TokenType.CATCH:
            self.expect(TokenType.CATCH)
            catch_condition = self.parse_expression()
            catch_body = self.parse_block()
            name = catch_condition.name     # or however you extract the string
            catch_map[name] = CatchStatement(catch_condition, catch_body)
            self.skipeols()

        if reprenabled == True: print(repr(TryStatement(try_body, catch_map)))
        return TryStatement(try_body, catch_map)
        

    def parse_raise_statement(self):
        self.expect(TokenType.RAISE)
        tok = self.expect(TokenType.IDENTIFIER).value
        message = None
        if self.current_token().type == TokenType.LEFT_PAREN:
            self.expect(TokenType.LEFT_PAREN)
            message = self.parse_expression().value
            self.expect(TokenType.RIGHT_PAREN)
        return RaiseStatement(tok, message)

    def parse_catch_statement(self):
        pass