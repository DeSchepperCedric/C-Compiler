from antlr4 import *
import sys

from antlr_files.CLexer import CLexer
from antlr_files.CListener import CListener
from antlr_files.CParser import CParser

from ParserVisitor import ParserVisitor


def main(argv):
    in_stream = FileStream(argv[1])
    lexer = CLexer(in_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.program()
    visitor = ParserVisitor()
    visitor.visitProgram(tree)
    print(visitor.getASTTree().toDot(add_open_close=True)[1])

if __name__ == "__main__":
    main(sys.argv)
