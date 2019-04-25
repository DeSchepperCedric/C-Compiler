from antlr4 import *
import sys
import os

from antlr_files.CLexer import CLexer
from antlr_files.CParser import CParser

from ParserVisitor import ParserVisitor
from ParserErrorListener import ParserErrorListener
from Logger import Logger
from CompilerException import CompilerException
from CompilerException import ParserException

from LLVMGenerator import LLVMGenerator

def run_compiler(source_file_path, output_name):
    in_stream = FileStream(source_file_path)
    lexer = CLexer(in_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    error_listener = ParserErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)
    parse_tree = parser.program()

    # if an error occurred, stop the compiling process
    if error_listener.hasErrored():
        raise ParserException()

    visitor = ParserVisitor()
    ast_tree = visitor.visitProgram(parse_tree) # create AST
    ast_tree.pruneDeadCode()                    # prune after continue, return and break
    ast_tree.genSymbolTable()                   # annotate AST with types and symbol table
    symbol_table = ast_tree.getSymbolTable()

    # constant folding
    # pruning

    # create output dir
    os.makedirs("./output/", exist_ok=True)

    with open("./output/" + output_name + "_ast.dot", 'w') as ast_dotfile:
        ast_dot_repr = ast_tree.toDot(add_open_close=True)[1]
        ast_dotfile.write(ast_dot_repr)

    with open("./output/" + output_name + "_symboltable.dot", 'w') as symboltable_dotfile:
        symboltable_dot_repr = symbol_table.toDot()
        symboltable_dotfile.write(symboltable_dot_repr)

    print(LLVMGenerator().astNodeToLLVM(ast_tree))


def main(argv):
    # the name that will be used to form output files
    output_name = os.path.basename(argv[1])

    try:
        run_compiler(source_file_path = argv[1], output_name=output_name)
    except CompilerException as e:
        Logger.error("Compiler was terminated due to errors in the specified C source file.")
    except Exception as e:
        Logger.error("Unexpected error of type '{}': {}".format(type(e), str(e)))

if __name__ == "__main__":
    main(sys.argv)
