from antlr4 import *
import sys

from antlr_files.CLexer import CLexer
from antlr_files.CListener import CListener
from antlr_files.CParser import CParser


def main(argv):
    in_stream = FileStream(argv[1])
    lexer = CLexer(in_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.program()
    printer = AstListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)


class AstListener(CListener):

    def __init__(self):
        self.current_node = None
    
    pass

if __name__ == "__main__":
    main(sys.argv)
