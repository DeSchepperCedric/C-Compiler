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


def run_compiler(source_file, output_file, dot_output_file_name,):
    in_stream = FileStream(source_file)
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
    ast_tree = visitor.visitProgram(parse_tree)  # create AST

    ast_tree.genSymbolTable()               # annotate AST with types and symbol table
    ast_tree.optimiseNodes(dict())          # optimisations (constant folding/propagation, null sequences,...)
    ast_tree.pruneDeadCode()                # prune after continue, return and break

    symbol_table = ast_tree.getSymbolTable()

    # create output dir
    os.makedirs("./output/", exist_ok=True)

    with open("./output/" + dot_output_file_name + "_ast.dot", 'w') as ast_dotfile:
        ast_dot_repr = ast_tree.toDot(add_open_close=True)[1]
        ast_dotfile.write(ast_dot_repr)

    with open("./output/" + dot_output_file_name + "_symboltable.dot", 'w') as symboltable_dotfile:
        symboltable_dot_repr = symbol_table.toDot()
        symboltable_dotfile.write(symboltable_dot_repr)

    with open("./output/" + output_file, 'w') as llvm_file:
        llvm_code = LLVMGenerator().astNodeToLLVM(ast_tree)
        llvm_file.write(llvm_code)


def main(argv):
    c_file = argv[1]     # type: str
    llvm_file = argv[2]  # type: str
    # the name that will be used to form output files
    output_name = os.path.basename(argv[1])
    output_name = "".join(output_name.split(".")[:-1])

    if not c_file.endswith(".c"):
        c_file += ".c"
    if not llvm_file.endswith(".ll"):
        llvm_file += ".ll"
    try:
        run_compiler(c_file, llvm_file, output_name)
    except CompilerException:
        Logger.error("Compiler was terminated due to errors in the specified C source file.")
    except Exception as e:
        Logger.error("Compiler was terminated due to errors in the specified C source file.")
        Logger.error("Error of type '{}': {}".format(type(e), str(e)))


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "--help":
        print("usage: <exec> <c_file> <llvm_file>")
    else:
        main(sys.argv)
