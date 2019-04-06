# Generated from ./C.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

# This class defines a complete listener for a parse tree produced by CParser.
class CListener(ParseTreeListener):

    # Enter a parse tree produced by CParser#program.
    def enterProgram(self, ctx:CParser.ProgramContext):
        pass

    # Exit a parse tree produced by CParser#program.
    def exitProgram(self, ctx:CParser.ProgramContext):
        pass


    # Enter a parse tree produced by CParser#declaration.
    def enterDeclaration(self, ctx:CParser.DeclarationContext):
        pass

    # Exit a parse tree produced by CParser#declaration.
    def exitDeclaration(self, ctx:CParser.DeclarationContext):
        pass


    # Enter a parse tree produced by CParser#init_decltr_list.
    def enterInit_decltr_list(self, ctx:CParser.Init_decltr_listContext):
        pass

    # Exit a parse tree produced by CParser#init_decltr_list.
    def exitInit_decltr_list(self, ctx:CParser.Init_decltr_listContext):
        pass


    # Enter a parse tree produced by CParser#declarator.
    def enterDeclarator(self, ctx:CParser.DeclaratorContext):
        pass

    # Exit a parse tree produced by CParser#declarator.
    def exitDeclarator(self, ctx:CParser.DeclaratorContext):
        pass


    # Enter a parse tree produced by CParser#var_decltr.
    def enterVar_decltr(self, ctx:CParser.Var_decltrContext):
        pass

    # Exit a parse tree produced by CParser#var_decltr.
    def exitVar_decltr(self, ctx:CParser.Var_decltrContext):
        pass


    # Enter a parse tree produced by CParser#func_decltr.
    def enterFunc_decltr(self, ctx:CParser.Func_decltrContext):
        pass

    # Exit a parse tree produced by CParser#func_decltr.
    def exitFunc_decltr(self, ctx:CParser.Func_decltrContext):
        pass


    # Enter a parse tree produced by CParser#param_spec.
    def enterParam_spec(self, ctx:CParser.Param_specContext):
        pass

    # Exit a parse tree produced by CParser#param_spec.
    def exitParam_spec(self, ctx:CParser.Param_specContext):
        pass


    # Enter a parse tree produced by CParser#param_list.
    def enterParam_list(self, ctx:CParser.Param_listContext):
        pass

    # Exit a parse tree produced by CParser#param_list.
    def exitParam_list(self, ctx:CParser.Param_listContext):
        pass


    # Enter a parse tree produced by CParser#param.
    def enterParam(self, ctx:CParser.ParamContext):
        pass

    # Exit a parse tree produced by CParser#param.
    def exitParam(self, ctx:CParser.ParamContext):
        pass


    # Enter a parse tree produced by CParser#simpl_expr.
    def enterSimpl_expr(self, ctx:CParser.Simpl_exprContext):
        pass

    # Exit a parse tree produced by CParser#simpl_expr.
    def exitSimpl_expr(self, ctx:CParser.Simpl_exprContext):
        pass


    # Enter a parse tree produced by CParser#types.
    def enterTypes(self, ctx:CParser.TypesContext):
        pass

    # Exit a parse tree produced by CParser#types.
    def exitTypes(self, ctx:CParser.TypesContext):
        pass


    # Enter a parse tree produced by CParser#var_decltr_id.
    def enterVar_decltr_id(self, ctx:CParser.Var_decltr_idContext):
        pass

    # Exit a parse tree produced by CParser#var_decltr_id.
    def exitVar_decltr_id(self, ctx:CParser.Var_decltr_idContext):
        pass


    # Enter a parse tree produced by CParser#constant.
    def enterConstant(self, ctx:CParser.ConstantContext):
        pass

    # Exit a parse tree produced by CParser#constant.
    def exitConstant(self, ctx:CParser.ConstantContext):
        pass


