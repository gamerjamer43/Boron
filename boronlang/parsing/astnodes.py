# astnodes.py
class ASTNode:
    pass

# main program node
class Program(ASTNode):
    def __init__(self):
        self.statements = []

    def __repr__(self):
        return f'''Program({self.statements})'''

# import node
class Import(ASTNode):
    def __init__(self, module, alias):
        self.module = module
        self.alias = alias

    def __repr__(self):
        return f'''Import({self.module}, {self.alias})'''
    
# function/method nodes
# lines 23-56
class Function(ASTNode):
    def __init__(self, name, parameters, return_type, body):
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.body = body
    
    def __repr__(self):
        return f'''Function({self.name}, {self.parameters}, {self.return_type}, {self.body})'''

class FunctionCall(ASTNode):
    def __init__(self, name, parameters, kwargs=None):
        self.name = name
        self.parameters = parameters
        self.kwargs = kwargs if kwargs is not None else {}
    
    def __repr__(self):
        return f'''FunctionCall({self.name}, {self.parameters})'''

class Parameter(ASTNode):
    def __init__(self, param_type, name):
        self.param_type = param_type
        self.name = name
    
    def __repr__(self):
        return f'''Parameter({self.param_type}, {self.name})'''

class MethodCall(ASTNode):
    def __init__(self, parent, name, parameters, kwargs=None):
        self.parent = parent
        self.name = name
        self.parameters = parameters
        self.kwargs = kwargs if kwargs is not None else {}
    
    def __repr__(self):
        return f'''MethodCall({self.parent}, {self.name}, {self.parameters})'''

# declare variable node
class VariableDeclaration(ASTNode):
    def __init__(self, var_type, name, value):
        self.var_type = var_type
        self.name = name
        self.value = value
    
    def __repr__(self):
        return f'''VariableDeclaration({self.var_type}, {self.name}, {self.value})'''

# operation nodes
# lines 70-94
class BinaryOperation(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def __repr__(self):
        return f'BinaryOperation({self.left}, {self.operator}, {self.right})'

class LogicalOperation(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def __repr__(self):
        return f'LogicalOperation({self.left}, {self.operator}, {self.right})'

class UnaryOperation(ASTNode):
    def __init__(self, operand, operator):
        self.operand = operand
        self.operator = operator
    
    def __repr__(self):
        return f'UnaryOperation({self.operator}, {self.operand})'

# control flow
# lines 98-131
class IfStatement(ASTNode):
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body
    
    def __repr__(self):
        return f'IfStatement({self.condition}, {self.if_body}, {self.else_body})'
    
class ForLoop(ASTNode):
    def __init__(self, initializer, condition, increment, body):
        self.initializer = initializer
        self.condition = condition
        self.increment = increment
        self.body = body
    
    def __repr__(self):
        return f'ForLoop({self.initializer}, {self.condition}, {self.increment}, {self.body})'

class WhileLoop(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    
    def __repr__(self):
        return f'WhileLoop({self.condition}, {self.body})'

class DoWhileLoop(ASTNode):
    def __init__(self, body, condition):
        self.body = body
        self.condition = condition
    
    def __repr__(self):
        return f'DoWhileLoop({self.body}, {self.condition})'

# literals
# lines 135-217
class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f'Identifier({self.name})'
    
class StringLiteral(ASTNode):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f'StringLiteral({self.value})'

class BooleanLiteral(ASTNode):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f'BooleanLiteral({self.value})'

class IntLiteral(ASTNode):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f'IntLiteral({self.value})'

class DecLiteral(ASTNode):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f'DecLiteral({self.value})'

class ListLiteral(ASTNode):
    def __init__(self, elements):
        self.elements = elements
    
    def __repr__(self):
        return f'ListLiteral({self.elements})'

class ArrayLiteral(ASTNode):
    def __init__(self, typ, size, elements):
        self.type = typ
        self.size = size
        self.elements = elements
    
    def __repr__(self):
        return f'ArrayLiteral({self.size}, {self.type}, {self.elements})'
    
class VectorLiteral(ASTNode):
    def __init__(self, typ, elements):
        self.type = typ
        self.elements = elements
    
    def __repr__(self):
        return f'VectorLiteral({self.type}, {self.elements})'
    
class RangeLiteral(ASTNode):
    def __init__(self, start, stop, increment):
        self.start = start
        self.stop = stop
        self.increment = increment
    
    def __repr__(self):
        return f'RangeLiteral({self.start}, {self.stop}, {self.increment})'

class ClassLiteral(ASTNode):
    def __init__(self, name, parent, sub, fields, methods, body):
        self.name = name
        self.parent = parent
        self.sub = sub
        self.fields = fields
        self.methods = methods
        self.body = body  # might remove

    def __repr__(self):
        return f'ClassLiteral({self.parent}, {self.sub}, {self.fields}, {self.methods}, {self.body}'

class NoneObject(ASTNode):
    def __init__(self):
        self.value = "None"
    
    def __repr__(self):
        return f'NoneObject({self.value})'

# index related nodes
class IndexAccess:
    def __init__(self, container, index):
        self.container = container
        self.index = index

    def __repr__(self):
        return f"IndexAccess({repr(self.container)}, {repr(self.index)})"
    
class IndexAssignment:
    def __init__(self, container, index, value):
        self.container = container
        self.index = index
        self.value = value

    def __repr__(self):
        return f"IndexAssignment({repr(self.container)}, {repr(self.index)}, {repr(self.value)})"

# instancing related nodes
class ClassInstantiation(ASTNode):
    def __init__(self, typ, name, arguments, kwargs=None):
        self.typ = typ
        self.name = name
        self.arguments = arguments
        self.kwargs = kwargs if kwargs is not None else {}

    def __repr__(self):
        return f"ClassInstantiation({self.typ}, {self.name}, {self.arguments}, {self.kwarguments})"

class FieldAccess(ASTNode):
    def __init__(self, parent, field):
        self.parent = parent
        self.field = field

    def __repr__(self):
        return f'FieldAccess({self.parent}, {self.field})'

class FieldAssignment(ASTNode):
    def __init__(self, parent, field, value):
        self.parent = parent
        self.field = field
        self.value = value

    def __repr__(self):
        return f'FieldAssignment({self.parent}, {self.field}, {self.value})'

# return nodes
class ReturnStatement(ASTNode):
    def __init__(self, values):
        self.values = values
    
    def __repr__(self):
        return f'ReturnStatement({self.values})'
    
# return exception for catching returns (break cases)
class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

# eof
class EndOfFile(ASTNode):
    def __init__(self):
        self.value = "EOF"
    
    def __repr__(self):
        return f'EndOfFile({self.value})'