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

from MipsGenerator import MipsGenerator


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

    with open("./output/" + output_file, 'w') as mips_file:
        mips_code = MipsGenerator().astNodeToMIPS(ast_tree)
        mips_file.write(mips_code)


def main(argv):
    c_file = argv[1]     # type: str
    mips_file = argv[2]  # type: str
    # the name that will be used to form output files
    output_name = os.path.basename(argv[1])
    output_name = "".join(output_name.split(".")[:-1])

    if not c_file.endswith(".c"):
        c_file += ".c"
    if not mips_file.endswith(".asm"):
        mips_file += ".asm"
    try:
        run_compiler(c_file, mips_file, output_name)
    except CompilerException:
        Logger.error("Compiler was terminated due to errors in the specified C source file.")
    except Exception as e:
        Logger.error("Compiler was terminated due to errors in the specified C source file.")
        Logger.error("Error of type '{}': {}".format(type(e), str(e)))


if __name__ == "__main__":
    main(sys.argv)
