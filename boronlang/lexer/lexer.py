# re for regex/token matching
import re

# enum to hold the token enum
from enum import Enum

# the token type enum, which holds a list of ALL the tokentypes
class TokenType(Enum):
    # types
    INTEGER = "int"
    DEC = "dec"
    BOOLEAN = "bool"
    STR = "str"
    RANGE = "range"
    TUPLE = "tuple"
    LIST = "list"
    ARRAY = "array"
    VECTOR = "vec"
    SET = "set"
    CLASS = "class"
    DICT = "dict"
    NONE = "none"

    # keywords
    FUNCTION = "fn"
    GLOBAL = "global"
    RETURN = "->"
    IF = "if"
    ELSE_IF = "else if"
    ELSE = "else"
    WHILE = "while"
    DO = "do"
    FOR = "for"
    IMPORT = "#import"
    IN = "in"
    
    # operators
    TRUE = "true"
    FALSE = "false"
    OR = "or"
    AND = "and"
    EQUAL = "=="
    NOT_EQUAL = "!="
    NOT = "!"
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    ASSIGN = "="
    INCREASE = "+="
    ADD = "+"
    INCREMENT = "++"
    DECREASE = "-="
    SUBTRACT = "-"
    DECREMENT = "--"
    MULTEQ = "*="
    MULTIPLY = "*"
    DIVEQ = "/="
    DIVIDE = "/"
    POWEQ = "**="
    POWER = "**"
    FLOOREQ = "//="
    FLOOR_DIVIDE = "//"
    MODULUS = "%"
    
    # braces and punctuation marks
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    COMMA = ","
    SEMICOLON = ";"
    PERIOD = "."
    
    # comments, idenitifiers, literals, eof, eol
    COMMENT = "COMMENT"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    DECIMAL = "DECIMAL"
    UNTERMINATED_STRING = "UNTERMINATED_STRING"
    EOF = "EOF"
    EOL = "EOL"

# the token class, which defines it's type, value, and it's position on both line and column
class Token:
    def __init__(self, type_, value, line, position):
        self.type = type_
        self.value = value
        self.line = line
        self.position = position
    
    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)})"

# the actual lexer, the guts of this shit
class Lexer:
    # initialize it with the text to lex, start the position at 0, and the line and column at 1
    # also initialize a list of all the tokens that will be added to as we go
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
    
    # the function to turn the text into tokens. i want to just put this inside the enum without breaking anything
    def tokenize(self):
        token_specification = [
            # types
            (TokenType.INTEGER, r'\bint\b'),
            (TokenType.DEC, r'\bdec\b'),
            (TokenType.BOOLEAN, r'\bbool\b'),
            (TokenType.STR, r'\bstr\b'),
            (TokenType.RANGE, r'\brange\b'),
            (TokenType.TUPLE, r'\btuple\b'),
            (TokenType.LIST, r'\blist\b'),
            (TokenType.ARRAY, r'\barray\b'),
            (TokenType.VECTOR, r'\bvec\b'),
            (TokenType.SET, r'\bset\b'),
            (TokenType.CLASS, r'\bclass\b'),
            (TokenType.DICT, r'\bdict\b'),
            (TokenType.NONE, r'\bnone\b'),
            (TokenType.TRUE, r'\btrue\b'),
            (TokenType.FALSE, r'\bfalse\b'),

            # keywords
            (TokenType.FUNCTION, r'\bfn\b'),
            (TokenType.GLOBAL, r'\bglobal\b'),
            (TokenType.RETURN, r'->'),
            (TokenType.IF, r'\bif\b'),
            (TokenType.ELSE_IF, r'\belse if\b'),
            (TokenType.ELSE, r'\belse\b'),
            (TokenType.WHILE, r'\bwhile\b'),
            (TokenType.DO, r'\bdo\b'),
            (TokenType.FOR, r'\bfor\b'),
            (TokenType.IN, r'\bin\b'),
            (TokenType.IMPORT, r'#\bimport\b'),
            (TokenType.AND, r'\band\b'),
            (TokenType.OR, r'\bor\b'),

            # operators
            (TokenType.EQUAL, r'=='),
            (TokenType.NOT_EQUAL, r'!='),
            (TokenType.NOT, r'!'),
            (TokenType.GREATER_EQUAL, r'>='),
            (TokenType.LESS_EQUAL, r'<='),
            (TokenType.GREATER_THAN, r'>'),
            (TokenType.LESS_THAN, r'<'),
            (TokenType.ASSIGN, r'='),
            (TokenType.INCREASE, r'\+='),
            (TokenType.INCREMENT, r'\+\+'),
            (TokenType.ADD, r'\+'),
            (TokenType.DECREASE, r'-='),
            (TokenType.DECREMENT, r'--'),
            (TokenType.SUBTRACT, r'-'),
            (TokenType.POWEQ, r'\*\*='),
            (TokenType.POWER, r'\*\*'),
            (TokenType.MULTEQ, r'\*='),
            (TokenType.MULTIPLY, r'\*'),
            (TokenType.DIVEQ, r'/='),
            (TokenType.FLOOREQ, r'//='),
            (TokenType.FLOOR_DIVIDE, r'//'),
            (TokenType.DIVIDE, r'/'),
            (TokenType.MODULUS, r'%'),

            # comments, identifers, literals
            (TokenType.COMMENT, r'#!.*|##!.*?##!'),
            (TokenType.IDENTIFIER, r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
            (TokenType.NUMBER, r'-?\b\d+?\b'),
            (TokenType.STRING, r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\''),
            (TokenType.UNTERMINATED_STRING, r'"([^"\\]|\\.)*$|\'([^\'\\]|\\.)*$'),
            
            # braces and punctuation marks
            (TokenType.LEFT_BRACKET, r'\['),
            (TokenType.RIGHT_BRACKET, r'\]'),
            (TokenType.LEFT_BRACE, r'\{'),
            (TokenType.RIGHT_BRACE, r'\}'),
            (TokenType.LEFT_PAREN, r'\('),
            (TokenType.RIGHT_PAREN, r'\)'),
            (TokenType.COMMA, r','),
            (TokenType.SEMICOLON, r';'),
            (TokenType.PERIOD, r'\.'),
        ]
        
        # make a regex matcher for each token type and compile it
        token_regex = '|'.join(f'(?P<{tok_type.name}>{pattern})' for tok_type, pattern in token_specification)
        get_token = re.compile(token_regex).match

        # split text by lines
        lines = self.text.splitlines()
        
        # start line count at 1 and iterate through each line
        linenum = 1
        linepos = 0
        for line in lines:
            # whitespace flag, if no content we just skip it. also initialize line position
            content = False
            linepos = 0
            
            # while text in a line
            while line:
                # get the current token, if there is none continue
                mo = get_token(line)
                if not mo:
                    line = line[1:]
                    continue

                # add length of the character to the position
                linepos += (mo.end() - mo.start())
                
                # get type of token from that, and check it against the regex matcher. get the actual token value as well
                typ = mo.lastgroup
                tok_type = TokenType[typ]
                value = mo.group(typ)
                
                # if comment, skip over it
                if tok_type == TokenType.COMMENT:
                    line = line[mo.end():]
                    continue
                
                # if number
                if tok_type == TokenType.NUMBER:
                    # get next character
                    line = line[mo.end():]
                    mo_next = get_token(line)

                    # if next character is a period
                    if mo_next and mo_next.lastgroup == "PERIOD":
                        # check if there is a token after the period
                        line = line[mo_next.end():]
                        mo_decimal = get_token(line)

                        # check if that token is another number
                        if mo_decimal and mo_decimal.lastgroup == "NUMBER":
                            # if it is assume it's a decimal
                            value += '.' + mo_decimal.group("NUMBER")
                            self.tokens.append(Token(TokenType.DECIMAL, value, linenum, linepos))
                            line = line[mo_decimal.end():]
                            continue
                        else:
                            # else just append a number and a period. we don't enforce errors in the lexer
                            self.tokens.append(Token(TokenType.NUMBER, value, linenum, linepos))
                            self.tokens.append(Token(TokenType.PERIOD, ".", linenum, linepos))
                            continue
                    else:
                        # if there isn't anything just append a number and continue
                        self.tokens.append(Token(TokenType.NUMBER, value, linenum, linepos))
                        continue
                
                # if static type definition
                if tok_type in [TokenType.FUNCTION, TokenType.INTEGER, TokenType.DEC, TokenType.BOOLEAN, TokenType.STR, TokenType.IMPORT, TokenType.TUPLE, TokenType.SET, TokenType.ARRAY, TokenType.LIST, TokenType.VECTOR, TokenType.RANGE, TokenType.CLASS]:
                    # get token after that
                    line = line[mo.end():].lstrip()
                    mo_identifier = get_token(line)
                    
                    # if it's an identifier, get it's name, mark content as true, and continue
                    if mo_identifier and mo_identifier.lastgroup == "IDENTIFIER":
                        name = mo_identifier.group("IDENTIFIER")
                        self.tokens.append(Token(tok_type, Token(TokenType.IDENTIFIER, name, linenum, linepos), linenum, linepos))
                        line = line[mo_identifier.end():]
                        content = True
                        continue
                    else:
                        # else append none because we don't enforce shit here
                        self.tokens.append(Token(tok_type, Token(TokenType.NONE, "none", linenum, linepos), linenum, linepos))
                        continue
                
                # if token is return
                if tok_type == TokenType.RETURN:
                    # get value after that token
                    line = line[mo.end():].lstrip()
                    mo_return_value = get_token(line)
                    
                    # if it's a type return, get and append the value and mark content as true
                    if mo_return_value and mo_return_value.lastgroup in ["INTEGER", "DEC", "BOOLEAN", "STR", "TUPLE", "SET", "ARRAY", "LIST", "VECTOR", "RANGE"]:
                        return_value = mo_return_value.group(mo_return_value.lastgroup)
                        self.tokens.append(Token(tok_type, return_value, linenum, linepos))
                        line = line[mo_return_value.end():]
                        content = True
                        continue

                    # else if it's a literal, idk what the fuck this does but it works
                    elif mo_return_value and mo_return_value.lastgroup in ["STRING", "IDENTIFIER", "NUMBER", "TRUE", "FALSE", "NONE"]:
                        return_value = Lexer(mo_return_value.group(mo_return_value.lastgroup)).tokenize()[0]
                        self.tokens.append(Token(tok_type, Token(TokenType.NONE, "none", linenum, linepos), linenum, linepos))
                        self.tokens.append(return_value)
                        line = line[mo_return_value.end():]
                        content = True
                        continue
                    else:
                        # else just append none
                        self.tokens.append(Token(tok_type, Token(TokenType.NONE, "none", linenum, linepos), linenum, linepos))
                        continue
                
                # string literals
                if tok_type == TokenType.STRING:
                    if value[0] == value[-1]:
                        value = value[1:-1]
                    self.tokens.append(Token(tok_type, value, linenum, linepos))
                    line = line[mo.end():]
                    content = True
                    continue
                
                # untermed string (which we errored out in the parser)
                if tok_type == TokenType.UNTERMINATED_STRING:
                    self.tokens.append(Token(tok_type, value, linenum, linepos))
                    line = line[mo.end():]
                    content = True
                    continue
                
                # else just append it's type, value, line number and position
                else:
                    self.tokens.append(Token(tok_type, value, linenum, linepos))
                    line = line[mo.end():]
                    content = True
                    continue

            # if there's content but we're at the end, eol. reset column position and add a line to count
            if content:
                self.tokens.append(Token(TokenType.EOL, "EOL", linenum, linepos))
                self.line += 1
                self.column = 1
                continue
            
            # at the end of lines add a number i guess
            linenum += 1

        # append an eof and return all tokens
        self.tokens.append(Token(TokenType.EOF, "EOF", linenum, linepos))
        return self.tokens