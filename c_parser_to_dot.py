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
    printer = PrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

def rec_visit(cur_node, cur_id):
    i = cur_id
    if cur_node.getChildCount() > 0:
        for child in cur_node.getChildren():
            print(cur_id,"->",i+1,";")
            i = rec_visit(child, i+1)
            
        # ENDFOR
    else:
        print(cur_id, "[label=\"",cur_node.getText(), "\"];")
    # ENDIF

    return i
# ENDFUNCTION

class PrintListener(CListener):
    def enterProgram(self, ctx:CParser.ProgramContext):
        # iterate over the children.
        #print(list(ctx.getChildren()))

        rec_visit(ctx, 0)
        
        print("Program")

    # Exit a parse tree produced by CParser#program.
    def exitProgram(self, ctx:CParser.ProgramContext):
        pass


    # Enter a parse tree produced by CParser#declaration.
    def enterDeclaration(self, ctx:CParser.DeclarationContext):
        print("Decl")

    # Exit a parse tree produced by CParser#declaration.
    def exitDeclaration(self, ctx:CParser.DeclarationContext):
        pass


    # Enter a parse tree produced by CParser#init_decltr_list.
    def enterInit_decltr_list(self, ctx:CParser.Init_decltr_listContext):
        print("init_decltr_list")

    # Exit a parse tree produced by CParser#init_decltr_list.
    def exitInit_decltr_list(self, ctx:CParser.Init_decltr_listContext):
        pass


    # Enter a parse tree produced by CParser#declarator.
    def enterDeclarator(self, ctx:CParser.DeclaratorContext):
        print("declarator")

    # Exit a parse tree produced by CParser#declarator.
    def exitDeclarator(self, ctx:CParser.DeclaratorContext):
        pass


    # Enter a parse tree produced by CParser#var_decltr.
    def enterVar_decltr(self, ctx:CParser.Var_decltrContext):
        print("var_decltr")

    # Exit a parse tree produced by CParser#var_decltr.
    def exitVar_decltr(self, ctx:CParser.Var_decltrContext):
        pass


    # Enter a parse tree produced by CParser#func_decltr.
    def enterFunc_decltr(self, ctx:CParser.Func_decltrContext):
        print("func_decltr")

    # Exit a parse tree produced by CParser#func_decltr.
    def exitFunc_decltr(self, ctx:CParser.Func_decltrContext):
        pass


    # Enter a parse tree produced by CParser#param_spec.
    def enterParam_spec(self, ctx:CParser.Param_specContext):
        print("param_spec")

    # Exit a parse tree produced by CParser#param_spec.
    def exitParam_spec(self, ctx:CParser.Param_specContext):
        pass


    # Enter a parse tree produced by CParser#param_list.
    def enterParam_list(self, ctx:CParser.Param_listContext):
        print("param_list")

    # Exit a parse tree produced by CParser#param_list.
    def exitParam_list(self, ctx:CParser.Param_listContext):
        pass


    # Enter a parse tree produced by CParser#param.
    def enterParam(self, ctx:CParser.ParamContext):
        print("param")

    # Exit a parse tree produced by CParser#param.
    def exitParam(self, ctx:CParser.ParamContext):
        pass


    # Enter a parse tree produced by CParser#simpl_expr.
    def enterSimpl_expr(self, ctx:CParser.Simpl_exprContext):
        print("simpl_expr")

    # Exit a parse tree produced by CParser#simpl_expr.
    def exitSimpl_expr(self, ctx:CParser.Simpl_exprContext):
        pass


    # Enter a parse tree produced by CParser#types.
    def enterTypes(self, ctx:CParser.TypesContext):
        print("types")

    # Exit a parse tree produced by CParser#types.
    def exitTypes(self, ctx:CParser.TypesContext):
        pass


    # Enter a parse tree produced by CParser#var_decltr_id.
    def enterVar_decltr_id(self, ctx:CParser.Var_decltr_idContext):
        print("var_decltr_id")

    # Exit a parse tree produced by CParser#var_decltr_id.
    def exitVar_decltr_id(self, ctx:CParser.Var_decltr_idContext):
        pass


    # Enter a parse tree produced by CParser#constant.
    def enterConstant(self, ctx:CParser.ConstantContext):
        print("constant")

    # Exit a parse tree produced by CParser#constant.
    def exitConstant(self, ctx:CParser.ConstantContext):
        pass

if __name__ == "__main__":
    main(sys.argv)
