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


    # Enter a parse tree produced by CParser#include.
    def enterInclude(self, ctx:CParser.IncludeContext):
        pass

    # Exit a parse tree produced by CParser#include.
    def exitInclude(self, ctx:CParser.IncludeContext):
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


    # Enter a parse tree produced by CParser#func_def.
    def enterFunc_def(self, ctx:CParser.Func_defContext):
        pass

    # Exit a parse tree produced by CParser#func_def.
    def exitFunc_def(self, ctx:CParser.Func_defContext):
        pass


    # Enter a parse tree produced by CParser#statement.
    def enterStatement(self, ctx:CParser.StatementContext):
        pass

    # Exit a parse tree produced by CParser#statement.
    def exitStatement(self, ctx:CParser.StatementContext):
        pass


    # Enter a parse tree produced by CParser#if_statement.
    def enterIf_statement(self, ctx:CParser.If_statementContext):
        pass

    # Exit a parse tree produced by CParser#if_statement.
    def exitIf_statement(self, ctx:CParser.If_statementContext):
        pass


    # Enter a parse tree produced by CParser#iteration_statement.
    def enterIteration_statement(self, ctx:CParser.Iteration_statementContext):
        pass

    # Exit a parse tree produced by CParser#iteration_statement.
    def exitIteration_statement(self, ctx:CParser.Iteration_statementContext):
        pass


    # Enter a parse tree produced by CParser#compound_statement.
    def enterCompound_statement(self, ctx:CParser.Compound_statementContext):
        pass

    # Exit a parse tree produced by CParser#compound_statement.
    def exitCompound_statement(self, ctx:CParser.Compound_statementContext):
        pass


    # Enter a parse tree produced by CParser#block_item.
    def enterBlock_item(self, ctx:CParser.Block_itemContext):
        pass

    # Exit a parse tree produced by CParser#block_item.
    def exitBlock_item(self, ctx:CParser.Block_itemContext):
        pass


    # Enter a parse tree produced by CParser#expression_statement.
    def enterExpression_statement(self, ctx:CParser.Expression_statementContext):
        pass

    # Exit a parse tree produced by CParser#expression_statement.
    def exitExpression_statement(self, ctx:CParser.Expression_statementContext):
        pass


    # Enter a parse tree produced by CParser#expression.
    def enterExpression(self, ctx:CParser.ExpressionContext):
        pass

    # Exit a parse tree produced by CParser#expression.
    def exitExpression(self, ctx:CParser.ExpressionContext):
        pass


    # Enter a parse tree produced by CParser#types.
    def enterTypes(self, ctx:CParser.TypesContext):
        pass

    # Exit a parse tree produced by CParser#types.
    def exitTypes(self, ctx:CParser.TypesContext):
        pass


    # Enter a parse tree produced by CParser#type_int.
    def enterType_int(self, ctx:CParser.Type_intContext):
        pass

    # Exit a parse tree produced by CParser#type_int.
    def exitType_int(self, ctx:CParser.Type_intContext):
        pass


    # Enter a parse tree produced by CParser#type_float.
    def enterType_float(self, ctx:CParser.Type_floatContext):
        pass

    # Exit a parse tree produced by CParser#type_float.
    def exitType_float(self, ctx:CParser.Type_floatContext):
        pass


    # Enter a parse tree produced by CParser#type_char.
    def enterType_char(self, ctx:CParser.Type_charContext):
        pass

    # Exit a parse tree produced by CParser#type_char.
    def exitType_char(self, ctx:CParser.Type_charContext):
        pass


    # Enter a parse tree produced by CParser#type_void.
    def enterType_void(self, ctx:CParser.Type_voidContext):
        pass

    # Exit a parse tree produced by CParser#type_void.
    def exitType_void(self, ctx:CParser.Type_voidContext):
        pass


    # Enter a parse tree produced by CParser#id_with_ptr.
    def enterId_with_ptr(self, ctx:CParser.Id_with_ptrContext):
        pass

    # Exit a parse tree produced by CParser#id_with_ptr.
    def exitId_with_ptr(self, ctx:CParser.Id_with_ptrContext):
        pass


    # Enter a parse tree produced by CParser#identifier.
    def enterIdentifier(self, ctx:CParser.IdentifierContext):
        pass

    # Exit a parse tree produced by CParser#identifier.
    def exitIdentifier(self, ctx:CParser.IdentifierContext):
        pass


    # Enter a parse tree produced by CParser#pointer.
    def enterPointer(self, ctx:CParser.PointerContext):
        pass

    # Exit a parse tree produced by CParser#pointer.
    def exitPointer(self, ctx:CParser.PointerContext):
        pass


    # Enter a parse tree produced by CParser#constant.
    def enterConstant(self, ctx:CParser.ConstantContext):
        pass

    # Exit a parse tree produced by CParser#constant.
    def exitConstant(self, ctx:CParser.ConstantContext):
        pass


