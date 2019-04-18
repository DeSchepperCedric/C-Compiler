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


    # Enter a parse tree produced by CParser#top_level_node.
    def enterTop_level_node(self, ctx:CParser.Top_level_nodeContext):
        pass

    # Exit a parse tree produced by CParser#top_level_node.
    def exitTop_level_node(self, ctx:CParser.Top_level_nodeContext):
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


    # Enter a parse tree produced by CParser#funcDecl.
    def enterFuncDecl(self, ctx:CParser.FuncDeclContext):
        pass

    # Exit a parse tree produced by CParser#funcDecl.
    def exitFuncDecl(self, ctx:CParser.FuncDeclContext):
        pass


    # Enter a parse tree produced by CParser#varDeclSimple.
    def enterVarDeclSimple(self, ctx:CParser.VarDeclSimpleContext):
        pass

    # Exit a parse tree produced by CParser#varDeclSimple.
    def exitVarDeclSimple(self, ctx:CParser.VarDeclSimpleContext):
        pass


    # Enter a parse tree produced by CParser#varDeclArray.
    def enterVarDeclArray(self, ctx:CParser.VarDeclArrayContext):
        pass

    # Exit a parse tree produced by CParser#varDeclArray.
    def exitVarDeclArray(self, ctx:CParser.VarDeclArrayContext):
        pass


    # Enter a parse tree produced by CParser#varDeclInit.
    def enterVarDeclInit(self, ctx:CParser.VarDeclInitContext):
        pass

    # Exit a parse tree produced by CParser#varDeclInit.
    def exitVarDeclInit(self, ctx:CParser.VarDeclInitContext):
        pass


    # Enter a parse tree produced by CParser#param.
    def enterParam(self, ctx:CParser.ParamContext):
        pass

    # Exit a parse tree produced by CParser#param.
    def exitParam(self, ctx:CParser.ParamContext):
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


    # Enter a parse tree produced by CParser#forLoop.
    def enterForLoop(self, ctx:CParser.ForLoopContext):
        pass

    # Exit a parse tree produced by CParser#forLoop.
    def exitForLoop(self, ctx:CParser.ForLoopContext):
        pass


    # Enter a parse tree produced by CParser#whileLoop.
    def enterWhileLoop(self, ctx:CParser.WhileLoopContext):
        pass

    # Exit a parse tree produced by CParser#whileLoop.
    def exitWhileLoop(self, ctx:CParser.WhileLoopContext):
        pass


    # Enter a parse tree produced by CParser#forCondWithDecl.
    def enterForCondWithDecl(self, ctx:CParser.ForCondWithDeclContext):
        pass

    # Exit a parse tree produced by CParser#forCondWithDecl.
    def exitForCondWithDecl(self, ctx:CParser.ForCondWithDeclContext):
        pass


    # Enter a parse tree produced by CParser#forCondNoDecl.
    def enterForCondNoDecl(self, ctx:CParser.ForCondNoDeclContext):
        pass

    # Exit a parse tree produced by CParser#forCondNoDecl.
    def exitForCondNoDecl(self, ctx:CParser.ForCondNoDeclContext):
        pass


    # Enter a parse tree produced by CParser#compound_statement.
    def enterCompound_statement(self, ctx:CParser.Compound_statementContext):
        pass

    # Exit a parse tree produced by CParser#compound_statement.
    def exitCompound_statement(self, ctx:CParser.Compound_statementContext):
        pass


    # Enter a parse tree produced by CParser#blockItemStatement.
    def enterBlockItemStatement(self, ctx:CParser.BlockItemStatementContext):
        pass

    # Exit a parse tree produced by CParser#blockItemStatement.
    def exitBlockItemStatement(self, ctx:CParser.BlockItemStatementContext):
        pass


    # Enter a parse tree produced by CParser#blockItemDeclaration.
    def enterBlockItemDeclaration(self, ctx:CParser.BlockItemDeclarationContext):
        pass

    # Exit a parse tree produced by CParser#blockItemDeclaration.
    def exitBlockItemDeclaration(self, ctx:CParser.BlockItemDeclarationContext):
        pass


    # Enter a parse tree produced by CParser#jumpReturn.
    def enterJumpReturn(self, ctx:CParser.JumpReturnContext):
        pass

    # Exit a parse tree produced by CParser#jumpReturn.
    def exitJumpReturn(self, ctx:CParser.JumpReturnContext):
        pass


    # Enter a parse tree produced by CParser#jumpBreak.
    def enterJumpBreak(self, ctx:CParser.JumpBreakContext):
        pass

    # Exit a parse tree produced by CParser#jumpBreak.
    def exitJumpBreak(self, ctx:CParser.JumpBreakContext):
        pass


    # Enter a parse tree produced by CParser#jumpContinue.
    def enterJumpContinue(self, ctx:CParser.JumpContinueContext):
        pass

    # Exit a parse tree produced by CParser#jumpContinue.
    def exitJumpContinue(self, ctx:CParser.JumpContinueContext):
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


    # Enter a parse tree produced by CParser#assignment_expr.
    def enterAssignment_expr(self, ctx:CParser.Assignment_exprContext):
        pass

    # Exit a parse tree produced by CParser#assignment_expr.
    def exitAssignment_expr(self, ctx:CParser.Assignment_exprContext):
        pass


    # Enter a parse tree produced by CParser#assignment_operator.
    def enterAssignment_operator(self, ctx:CParser.Assignment_operatorContext):
        pass

    # Exit a parse tree produced by CParser#assignment_operator.
    def exitAssignment_operator(self, ctx:CParser.Assignment_operatorContext):
        pass


    # Enter a parse tree produced by CParser#logical_or_expr.
    def enterLogical_or_expr(self, ctx:CParser.Logical_or_exprContext):
        pass

    # Exit a parse tree produced by CParser#logical_or_expr.
    def exitLogical_or_expr(self, ctx:CParser.Logical_or_exprContext):
        pass


    # Enter a parse tree produced by CParser#logical_and_expr.
    def enterLogical_and_expr(self, ctx:CParser.Logical_and_exprContext):
        pass

    # Exit a parse tree produced by CParser#logical_and_expr.
    def exitLogical_and_expr(self, ctx:CParser.Logical_and_exprContext):
        pass


    # Enter a parse tree produced by CParser#equality_expr.
    def enterEquality_expr(self, ctx:CParser.Equality_exprContext):
        pass

    # Exit a parse tree produced by CParser#equality_expr.
    def exitEquality_expr(self, ctx:CParser.Equality_exprContext):
        pass


    # Enter a parse tree produced by CParser#relational_expr.
    def enterRelational_expr(self, ctx:CParser.Relational_exprContext):
        pass

    # Exit a parse tree produced by CParser#relational_expr.
    def exitRelational_expr(self, ctx:CParser.Relational_exprContext):
        pass


    # Enter a parse tree produced by CParser#additive_expr.
    def enterAdditive_expr(self, ctx:CParser.Additive_exprContext):
        pass

    # Exit a parse tree produced by CParser#additive_expr.
    def exitAdditive_expr(self, ctx:CParser.Additive_exprContext):
        pass


    # Enter a parse tree produced by CParser#multiplicative_expr.
    def enterMultiplicative_expr(self, ctx:CParser.Multiplicative_exprContext):
        pass

    # Exit a parse tree produced by CParser#multiplicative_expr.
    def exitMultiplicative_expr(self, ctx:CParser.Multiplicative_exprContext):
        pass


    # Enter a parse tree produced by CParser#cast_expr.
    def enterCast_expr(self, ctx:CParser.Cast_exprContext):
        pass

    # Exit a parse tree produced by CParser#cast_expr.
    def exitCast_expr(self, ctx:CParser.Cast_exprContext):
        pass


    # Enter a parse tree produced by CParser#unaryAsPostfix.
    def enterUnaryAsPostfix(self, ctx:CParser.UnaryAsPostfixContext):
        pass

    # Exit a parse tree produced by CParser#unaryAsPostfix.
    def exitUnaryAsPostfix(self, ctx:CParser.UnaryAsPostfixContext):
        pass


    # Enter a parse tree produced by CParser#unaryOp.
    def enterUnaryOp(self, ctx:CParser.UnaryOpContext):
        pass

    # Exit a parse tree produced by CParser#unaryOp.
    def exitUnaryOp(self, ctx:CParser.UnaryOpContext):
        pass


    # Enter a parse tree produced by CParser#unary_operator.
    def enterUnary_operator(self, ctx:CParser.Unary_operatorContext):
        pass

    # Exit a parse tree produced by CParser#unary_operator.
    def exitUnary_operator(self, ctx:CParser.Unary_operatorContext):
        pass


    # Enter a parse tree produced by CParser#arrayAccesExpr.
    def enterArrayAccesExpr(self, ctx:CParser.ArrayAccesExprContext):
        pass

    # Exit a parse tree produced by CParser#arrayAccesExpr.
    def exitArrayAccesExpr(self, ctx:CParser.ArrayAccesExprContext):
        pass


    # Enter a parse tree produced by CParser#postfixDec.
    def enterPostfixDec(self, ctx:CParser.PostfixDecContext):
        pass

    # Exit a parse tree produced by CParser#postfixDec.
    def exitPostfixDec(self, ctx:CParser.PostfixDecContext):
        pass


    # Enter a parse tree produced by CParser#primitiveExpr.
    def enterPrimitiveExpr(self, ctx:CParser.PrimitiveExprContext):
        pass

    # Exit a parse tree produced by CParser#primitiveExpr.
    def exitPrimitiveExpr(self, ctx:CParser.PrimitiveExprContext):
        pass


    # Enter a parse tree produced by CParser#funcCall.
    def enterFuncCall(self, ctx:CParser.FuncCallContext):
        pass

    # Exit a parse tree produced by CParser#funcCall.
    def exitFuncCall(self, ctx:CParser.FuncCallContext):
        pass


    # Enter a parse tree produced by CParser#postfixInc.
    def enterPostfixInc(self, ctx:CParser.PostfixIncContext):
        pass

    # Exit a parse tree produced by CParser#postfixInc.
    def exitPostfixInc(self, ctx:CParser.PostfixIncContext):
        pass


    # Enter a parse tree produced by CParser#parenExpr.
    def enterParenExpr(self, ctx:CParser.ParenExprContext):
        pass

    # Exit a parse tree produced by CParser#parenExpr.
    def exitParenExpr(self, ctx:CParser.ParenExprContext):
        pass


    # Enter a parse tree produced by CParser#idExpr.
    def enterIdExpr(self, ctx:CParser.IdExprContext):
        pass

    # Exit a parse tree produced by CParser#idExpr.
    def exitIdExpr(self, ctx:CParser.IdExprContext):
        pass


    # Enter a parse tree produced by CParser#constantExpr.
    def enterConstantExpr(self, ctx:CParser.ConstantExprContext):
        pass

    # Exit a parse tree produced by CParser#constantExpr.
    def exitConstantExpr(self, ctx:CParser.ConstantExprContext):
        pass


    # Enter a parse tree produced by CParser#prim_type.
    def enterPrim_type(self, ctx:CParser.Prim_typeContext):
        pass

    # Exit a parse tree produced by CParser#prim_type.
    def exitPrim_type(self, ctx:CParser.Prim_typeContext):
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


    # Enter a parse tree produced by CParser#type_bool.
    def enterType_bool(self, ctx:CParser.Type_boolContext):
        pass

    # Exit a parse tree produced by CParser#type_bool.
    def exitType_bool(self, ctx:CParser.Type_boolContext):
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


    # Enter a parse tree produced by CParser#int_constant.
    def enterInt_constant(self, ctx:CParser.Int_constantContext):
        pass

    # Exit a parse tree produced by CParser#int_constant.
    def exitInt_constant(self, ctx:CParser.Int_constantContext):
        pass


    # Enter a parse tree produced by CParser#float_constant.
    def enterFloat_constant(self, ctx:CParser.Float_constantContext):
        pass

    # Exit a parse tree produced by CParser#float_constant.
    def exitFloat_constant(self, ctx:CParser.Float_constantContext):
        pass


    # Enter a parse tree produced by CParser#str_constant.
    def enterStr_constant(self, ctx:CParser.Str_constantContext):
        pass

    # Exit a parse tree produced by CParser#str_constant.
    def exitStr_constant(self, ctx:CParser.Str_constantContext):
        pass


    # Enter a parse tree produced by CParser#char_constant.
    def enterChar_constant(self, ctx:CParser.Char_constantContext):
        pass

    # Exit a parse tree produced by CParser#char_constant.
    def exitChar_constant(self, ctx:CParser.Char_constantContext):
        pass


    # Enter a parse tree produced by CParser#bool_constant.
    def enterBool_constant(self, ctx:CParser.Bool_constantContext):
        pass

    # Exit a parse tree produced by CParser#bool_constant.
    def exitBool_constant(self, ctx:CParser.Bool_constantContext):
        pass


