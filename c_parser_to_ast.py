from antlr4 import *
import sys

from antlr_files.CLexer import CLexer
from antlr_files.CParser import CParser

from ParserVisitor import ParserVisitor
from SymbolTable import print_symbol_table_to_dot


def main(argv):
    in_stream = FileStream(argv[1])
    lexer = CLexer(in_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    parse_tree = parser.program()
    visitor = ParserVisitor()
    ast_tree = visitor.visitProgram(parse_tree)


    ast_dot_repr = ast_tree.toDot(add_open_close=True)[1]
    print(ast_dot_repr)
    symbol_table = ast_tree.getSymbolTable()
    #print_symbol_table_to_dot(symbol_table)


if __name__ == "__main__":
    main(sys.argv)
