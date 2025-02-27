from lexer.lexer import Lexer
from parsing.parser import Parser
from interpreter.interpreter import Interpreter
import os

def assemble(filename):
    try:
        with open(filename, "r") as file:
            # read code from file
            code = file.read()

            # tokenize code
            tokens = Lexer(code).tokenize()

            # optionally print tokens
            print("\nTokens:")
            for token in tokens:
                print(token)

            # print for __repr__ which i will remove as i am more comfortable with debugging
            print("\n__repr__:")
            
            # parse ast
            ast = Parser(tokens).parse()

            # optionally print ast
            print("\nAST:")
            print(str(ast) + "\n")

            # run it through the interpreter
            Interpreter().evaluate(ast)

    # file not found error lol
    except FileNotFoundError: 
        print("error. file not found")
        os._exit(0)