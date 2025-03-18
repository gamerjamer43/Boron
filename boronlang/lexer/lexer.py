# re for regex/token matching
import re

# enum to hold the token enum
from enum import Enum

class TokenType(Enum):
    # numbers
    NUMBER = ("number", r'-?\b\d+?\b')
    
    # types
    INTEGER = ("int", r'\bint\b')
    DEC = ("dec", r'\bdec\b')
    BOOLEAN = ("bool", r'\bbool\b')
    STR = ("str", r'\bstr\b')
    RANGE = ("range", r'\brange\b')
    TUPLE = ("tuple", r'\btuple\b')
    LIST = ("list", r'\blist\b')
    ARRAY = ("array", r'\barray\b')
    VECTOR = ("vec", r'\bvec\b')
    SET = ("set", r'\bset\b')
    CLASS = ("class", r'\bclass\b')
    DICT = ("dict", r'\bdict\b')
    NONE = ("none", r'\bnone\b')
    TRUE = ("true", r'\btrue\b')
    FALSE = ("false", r'\bfalse\b')
    
    # keywords
    FUNCTION = ("fn", r'\bfn\b')
    GLOBAL = ("global", r'\bglobal\b')
    RETURN = ("->", r'->')
    EXTENDS = ("extends", r"\bextends\b")
    NEW = ("new", r"\bnew\b")
    IF = ("if", r'\bif\b')
    ELSE_IF = ("else if", r'\belse if\b')
    ELSE = ("else", r'\belse\b')
    WHILE = ("while", r'\bwhile\b')
    DO = ("do", r'\bdo\b')
    FOR = ("for", r'\bfor\b')
    IN = ("in", r'\bin\b')
    IMPORT = ("#import", r'#\bimport\b')
    AND = ("and", r'\band\b')
    OR = ("or", r'\bor\b')
    AS = ("as", r'\bas\b')
    
    # operators
    EQUAL = ("==", r'==')
    NOT_EQUAL = ("!=", r'!=')
    NOT = ("!", r'!')
    GREATER_EQUAL = (">=", r'>=')
    LESS_EQUAL = ("<=", r'<=')
    GREATER_THAN = (">", r'>')
    LESS_THAN = ("<", r'<')
    ASSIGN = ("=", r'=')
    INCREASE = ("+=", r'\+=')
    INCREMENT = ("++", r'\+\+')
    ADD = ("+", r'\+')
    DECREASE = ("-=", r'-=')
    DECREMENT = ("--", r'--')
    SUBTRACT = ("-", r'-')
    POWEQ = ("**=", r'\*\*=')
    POWER = ("**", r'\*\*')
    MULTEQ = ("*=", r'\*=')
    MULTIPLY = ("*", r'\*')
    DIVEQ = ("/=", r'/=')
    FLOOREQ = ("//=", r'//=')
    FLOOR_DIVIDE = ("//", r'//')
    DIVIDE = ("/", r'/')
    MODULUS = ("%", r'%')
    
    # comments, identifiers, literals
    COMMENT = ("COMMENT", r'#!.*|##!.*?##!')
    IDENTIFIER = ("identifier", r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')
    STRING = ("string", r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\'')
    UNTERMINATED_STRING = ("unterminated", r'"([^"\\]|\\.)*$|\'([^\'\\]|\\.)*$')
    
    # braces and punctuation marks
    LEFT_BRACKET = ("[", r'\[')
    RIGHT_BRACKET = ("]", r'\]')
    LEFT_BRACE = ("{", r'\{')
    RIGHT_BRACE = ("}", r'\}')
    LEFT_PAREN = ("(", r'\(')
    RIGHT_PAREN = (")", r'\)')
    COMMA = (",", r',')
    SEMICOLON = (";", r';')
    PERIOD = (".", r'\.')
    
    # special tokens (handled separately)
    DECIMAL = ("decimal", None)
    EOF = ("EOF", None)
    EOL = ("EOL", None)

    def __init__(self, label, pattern):
        self.label = label
        self.pattern = pattern

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
            (token_type, token_type.pattern)
            for token_type in TokenType
            if token_type.pattern is not None
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
                if tok_type in [TokenType.FUNCTION, TokenType.INTEGER, TokenType.DEC, TokenType.BOOLEAN, TokenType.STR, TokenType.IMPORT, TokenType.AS, TokenType.TUPLE, 
                                TokenType.SET, TokenType.ARRAY, TokenType.LIST, TokenType.VECTOR, TokenType.RANGE, TokenType.CLASS, TokenType.EXTENDS, TokenType.AS]:
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