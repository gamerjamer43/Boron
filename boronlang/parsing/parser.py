# lexer import
from lexer.lexer import Token, TokenType
# important nodes
from parsing.astnodes import Program, Import, EndOfFile
# class and function nodes
from parsing.astnodes import Function, FunctionCall, MethodCall, Parameter, ReturnStatement, FieldAccess, FieldAssignment, ClassInstantiation
# operation nodes
from parsing.astnodes import BinaryOperation, LogicalOperation, UnaryOperation, IndexAccess, IndexAssignment
# control flow nodes
from parsing.astnodes import IfStatement, ForLoop, WhileLoop, DoWhileLoop
# variable nodes
from parsing.astnodes import VariableDeclaration, Identifier, StringLiteral, BooleanLiteral, IntLiteral, DecLiteral, ListLiteral, ArrayLiteral, RangeLiteral, ClassLiteral, VectorLiteral
# scope
from parsing.scope import Scope

# parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.line = 1
        self.scope = Scope()

    def current_token(self):
        return self.tokens[self.pos]
    
    def current_line(self):
        return self.line

    def next_token(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def expect(self, token_type):
        token = self.current_token()
        if token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, but found {token.type}. Specific token afflicted: {token}")
        self.next_token()
        return token

    def parse(self):
        program = Program()
        while self.current_token().type != TokenType.EOF:
            program.statements.append(self.parse_statement())
        return program

    def parse_statement(self):
        token = self.current_token()
        while token.type == TokenType.EOL:
            self.line += 1
            token = self.next_token()

        dispatch_table = {
            TokenType.IMPORT: self.parse_import,
            TokenType.INTEGER: self.parse_variable_declaration,
            TokenType.BOOLEAN: self.parse_variable_declaration,
            TokenType.STR: self.parse_variable_declaration,
            TokenType.TUPLE: self.parse_variable_declaration,
            TokenType.LIST: self.parse_variable_declaration,
            TokenType.SET: self.parse_variable_declaration,
            TokenType.DEC: self.parse_variable_declaration,
            TokenType.RANGE: self.parse_range_declaration,
            TokenType.ARRAY: self.parse_array_declaration,
            TokenType.VECTOR: self.parse_vector_declaration,
            TokenType.CLASS: self.parse_class_declaration,
            TokenType.GLOBAL: self.parse_global_declaration,
            TokenType.IDENTIFIER: self.parse_identifier,
            TokenType.FUNCTION: self.parse_function,
            TokenType.IF: self.parse_if_statement,
            TokenType.FOR: self.parse_for_loop,
            TokenType.WHILE: self.parse_while_loop,
            TokenType.DO: self.parse_do_while_loop,
            TokenType.RETURN: self.parse_return_statement,
            TokenType.EOF: lambda: EndOfFile()
        }

        if token.type in dispatch_table:
            return dispatch_table[token.type]()
        else:
            raise SyntaxError(f"Unexpected token {token.type}")
  
    
    # wip, hopefully this should parse blocks correctly
    def parse_block(self):
        self.expect(TokenType.LEFT_BRACE)
        statements = []
        # skip any initial EOLs.
        while self.current_token().type == TokenType.EOL:
            self.next_token()
        # parse until right brace.
        while self.current_token().type != TokenType.RIGHT_BRACE:
            # skip extra EOL between statements.
            while self.current_token().type == TokenType.EOL:
                self.next_token()
            if self.current_token().type == TokenType.RIGHT_BRACE:
                break
            statements.append(self.parse_statement())
        self.expect(TokenType.RIGHT_BRACE)
        return statements

        
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

        # print(repr(VariableDeclaration(var_type, name, value)))
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

        # print(repr(VariableDeclaration(TokenType.RANGE, name, RangeLiteral(IntLiteral(start), IntLiteral(stop), IntLiteral(increment)))))
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
        # print(repr(VariableDeclaration(arraytype, Identifier(name), ArrayLiteral(typ, size, elements))))
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
        # print(repr(VariableDeclaration(arraytype, Identifier(name), VectorLiteral(typ, elements))))
        return VariableDeclaration(arraytype, Identifier(name), VectorLiteral(typ, elements))
        

    def parse_identifier(self):
        # add more scope here
        cur = self.current_token()
        name = cur.value
        
        next_token = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
        
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
                    # print(repr(BinaryOperation(name, operator, Identifier(new_value))))
                    return BinaryOperation(name, operator, Identifier(new_value))

                # print(repr(BinaryOperation(Identifier(name), operator, new_value)))
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

                return IndexAccess(Identifier(name), index_expr)
            
            elif next_token.type in [TokenType.INCREMENT, TokenType.DECREMENT]:
                self.next_token()
                operator = next_token.type
                self.next_token()
                # print(repr(UnaryOperation(Identifier(name), operator)))
                return UnaryOperation(Identifier(name), operator)
            
            elif next_token.type == TokenType.ASSIGN:
                self.next_token()  # consume the ASSIGN token
                self.next_token()

                if not self.scope.is_declared(name):
                    raise SyntaxError(f"Variable '{name}' not declared in this scope. Declare the variable to operate on it.")
                
                right = self.parse_expression()
                var_type = self.scope.get_variable_type(name)
                
                # print(repr(VariableDeclaration(var_type, Identifier(name), right)))
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
                    while self.current_token().type != TokenType.RIGHT_PAREN:
                        if self.current_token().type == TokenType.COMMA:
                            self.next_token()
                        arguments.append(self.parse_expression())
                    self.expect(TokenType.RIGHT_PAREN)
                    # print(repr(MethodCall(parent, property_or_method, arguments)))
                    return MethodCall(parent, property_or_method, arguments)

                elif self.current_token().type == TokenType.ASSIGN:
                    self.next_token()
                    value = self.parse_expression()
                    # print(repr(FieldAssignment(parent, property_or_method, value)))
                    return FieldAssignment(parent, property_or_method, value)

                else:
                    # print(repr(FieldAccess(parent, property_or_method)))
                    return FieldAccess(parent, property_or_method)
            
            # wip... make class instantiation work
            elif next_token.type == TokenType.IDENTIFIER:
                typ = self.expect(TokenType.IDENTIFIER)
                name = self.expect(TokenType.IDENTIFIER)
                self.expect(TokenType.ASSIGN)
                self.expect(TokenType.NEW)
                self.expect(TokenType.IDENTIFIER)
                arguments = []

                if self.current_token().type == TokenType.LEFT_PAREN:
                    self.expect(TokenType.LEFT_PAREN)

                    while self.current_token().type != TokenType.RIGHT_PAREN:
                        arguments.append(self.parse_expression())
                        if self.current_token().type == TokenType.COMMA:
                            self.next_token()

                    self.expect(TokenType.RIGHT_PAREN)

                return ClassInstantiation(typ, name, arguments)

            elif next_token.type == TokenType.LEFT_PAREN:
                self.next_token()
                return self.parse_function_call(name)
            
            elif next_token.type == TokenType.LEFT_BRACKET:
                self.next_token()
                # why is this here
      
        # if no operator follows assume variable reference
        self.next_token()
        # print(repr(Identifier(name)))
        return Identifier(name)
    

    def parse_function_call(self, name):
        self.expect(TokenType.LEFT_PAREN)
        arguments = []
        
        # parse arguments separated by commas
        while self.current_token().type != TokenType.RIGHT_PAREN:
            arguments.append(self.parse_expression())
            if self.current_token().type == TokenType.COMMA:
                self.next_token()

        self.expect(TokenType.RIGHT_PAREN) 
        return FunctionCall(name, arguments)


    def parse_import(self):
        import_token = self.expect(TokenType.IMPORT)
        alias = import_token.value.value
        if not isinstance(import_token.value, Token) or import_token.value.type != TokenType.IDENTIFIER:
            raise SyntaxError(f"Invalid import statement: Expected an identifier, found {import_token.value}")
        
        print(self.current_token().type)
        if self.current_token().type == TokenType.AS:
            alias = self.current_token().value.value
            self.next_token()

        module = import_token.value.value
        if self.scope.is_imported(module):
            raise SyntaxError(f"Variable '{module}' already declared in this scope.")

        self.scope.declare_import(module, alias)
        # print(repr(Import(module)))
        return Import(module, alias)

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
            while self.current_token().type == TokenType.EOL:
                self.next_token()

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
        
        # print(repr(VariableDeclaration(TokenType.CLASS, name, 
        #    ClassLiteral(extends, children, fields, methods, body))))
        return VariableDeclaration(
            TokenType.CLASS, name, 
            ClassLiteral(extends, children, fields, methods, body)
        )


    def parse_function(self):
        name = self.expect(TokenType.FUNCTION).value

        if self.scope.is_declared(name):
            raise SyntaxError(f"Function '{name}' already declared in this scope.")
        
        self.scope.declare_variable(name, TokenType.FUNCTION)
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

        body = self.parse_block()  # use the block parser
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

        if self.current_token().type == TokenType.ELSE:
            self.next_token()
            final_else_body = self.parse_block()
            if last_else_if:
                last_else_if.else_body = final_else_body
            else:
                else_body = final_else_body

        return IfStatement(condition, if_body, else_body)


    def parse_for_loop(self):
        self.expect(TokenType.FOR)
        self.expect(TokenType.LEFT_PAREN)
        self.scope.enter_scope()

        initializer = self.parse_statement()
        self.expect(TokenType.SEMICOLON)

        condition = self.parse_expression()
        self.expect(TokenType.SEMICOLON)

        increment = self.parse_expression()
        self.expect(TokenType.RIGHT_PAREN)
        self.expect(TokenType.LEFT_BRACE)
        body = []
        while self.current_token().type != TokenType.RIGHT_BRACE:
            body.append(self.parse_statement())
            self.next_token()
        self.expect(TokenType.RIGHT_BRACE)

        self.scope.exit_scope()
        # print(repr(ForLoop(initializer, condition, increment, body)))
        return ForLoop(initializer, condition, increment, body)


    def parse_while_loop(self):
        self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        self.expect(TokenType.LEFT_BRACE)

        body = []
        while self.current_token().type != TokenType.RIGHT_BRACE:
            body.append(self.parse_statement())
            self.next_token()
        self.expect(TokenType.RIGHT_BRACE)
        # print(repr(WhileLoop(condition, body)))
        return WhileLoop(condition, body)


    def parse_do_while_loop(self):
        self.expect(TokenType.DO)
        self.expect(TokenType.LEFT_BRACE)
        body = []
        while self.current_token().type != TokenType.RIGHT_BRACE:
            body.append(self.parse_statement())
            self.next_token()
        self.expect(TokenType.RIGHT_BRACE)
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LEFT_PAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RIGHT_PAREN)
        # print(repr(DoWhileLoop(body, condition)))
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
        # print(repr(ListLiteral(elements)))
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
        
        # print(repr(ReturnStatement(values)))
        return ReturnStatement(values)