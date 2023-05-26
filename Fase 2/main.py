import antlr4
from sys import argv
from GramaticaLexer import GramaticaLexer
from GramaticaParser import GramaticaParser

def main():
    if (len(argv) < 2):
        print("main.py <PATH>")
        return
    
    path = argv[1]
    input_stream = antlr4.FileStream(path)
    lexer = GramaticaLexer(input_stream)
    token_stream = antlr4.CommonTokenStream(lexer)
    parser = GramaticaParser(token_stream)
    tree = parser.program()
    print(tree.toStringTree())

if __name__ == "__main__":
    main()