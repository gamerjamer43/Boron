from lexer.lexer import Lexer
from parsing.parser import Parser
from interpreter.interpreter import Interpreter
from os import _exit
from time import time

def assemble(filename, args) -> None:
    try:
        # open file
        with open(filename, "r") as file:
            code = file.read()

        # tokenization time
        start = time()
        tokens = Lexer(code).tokenize()
        end = time()
        print(f"Tokenization completed in {(end - start) * 1000:.3f} ms\n") # print in ms

        # print tokens
        print("\nTokens:")
        for token in tokens:
            print(token)

        # parsing time
        start = time()
        ast = Parser(tokens).parse()
        end_parse = time() # we have to use this one a minute later fuck
        print(f"\nParsing completed in {(end_parse - start) * 1000:.3f} ms") # print in ms

        # print AST
        print("\nAST:")
        print(str(ast) + "\n")

        # interpretation timing
        start = time()
        Interpreter().evaluate(ast)
        end = time()

        # execution delay and time in milliseconds
        print(f"\nExecution delay: {(start - end_parse) * 1000:.3f} ms")
        print(f"Execution completed in {(end - start) * 1000:.3f} ms\n")

        if args:
            print(args)

    except FileNotFoundError: 
        print("Error: File not found")
        _exit(0)