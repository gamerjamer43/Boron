from lexer.lexer import Lexer
from parsing.parser import Parser
from interpreter.interpreter import Interpreter
from os import _exit

global reprenabled
reprenabled = False

def assemble(filename, args) -> None:
    try:
        # open file
        with open(filename, "r") as file:
            code = file.read()

        # lexer
        tokens = Lexer(code).tokenize()
        if reprenabled == True:
            # print tokens
            print("\nTokens:")
            for token in tokens:
                print(token)

        # parser
        ast = Parser(tokens).parse()
        if reprenabled == True:
            # print AST
            print("\nAST:")
            print(str(ast) + "\n")

        # interpreter
        Interpreter(filename, args).evaluate(ast)

    except FileNotFoundError: 
        print("Error: File not found")
        _exit(0)