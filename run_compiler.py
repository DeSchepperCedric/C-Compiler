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
from MipsGenerator import MipsGenerator

def run_compiler(source_file_path, output_name, target_language):
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
    ast_tree.constantFolding(dict())

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

    if target_language == "llvm":
        with open("./output/" + output_name + ".ll", 'w') as llvm_file:
            llvm_code = LLVMGenerator().astNodeToLLVM(ast_tree)
            llvm_file.write(llvm_code)
    elif target_language == "mips":
        with open("./output/" + output_name + ".ll", 'w') as mips_file:
            mips_code = MipsGenerator().astNodeToLLVM(ast_tree)
            mips_file.write(mips_code)




def main(argv):
    target_language = argv[1].lower()
    # the name that will be used to form output files
    output_name = os.path.basename(argv[2])
    output_name = "".join(output_name.split(".")[:-1])

    if target_language not in ["llvm", "mips"]:
        raise Exception("Invalid target language {}. Must be llvm or mips.".format(target_language))

    try:
        run_compiler(source_file_path = argv[2], output_name=output_name, target_language=target_language)
    except CompilerException as e:
        Logger.error("Compiler was terminated due to errors in the specified C source file.")
    #except Exception as e:
     #   Logger.error("Unexpected error of type '{}': {}".format(type(e), str(e)))

if __name__ == "__main__":
    main(sys.argv)
