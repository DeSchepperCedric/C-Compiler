from antlr_files.CVisitor import CVisitor
from antlr_files.CLexer import CLexer
from antlr_files.CListener import CListener
from antlr_files.CParser import CParser
from ASTTreeNodes import *

import sys

class ParserVisitor(CVisitor):

    def manuallyVisitChild(self, child_node):
        return child_node.accept(self)

    # END

    # Visit a parse tree produced by CParser#program.
    def visitProgram(self, ctx: CParser.ProgramContext):
        
        program_node = ProgramNode()

        # add each top-level-instruction as a child
        for child in ctx.getChildren():
            # skip EOF (hacky solution)
            if child.getText() == "<EOF>":
                continue

            child_result = self.manuallyVisitChild(child)
            if isinstance(child_result, list):
                for c in child_result:
                    program_node.addChild(c)
            else:
                program_node.addChild(child_result)

        print("Toplevel nodes:",program_node.children)

        return program_node
    # END

    # Visit a parse tree produced by CParser#top_level_node.
    def visitTop_level_node(self, ctx: CParser.Top_level_nodeContext):
        # top level node has
        #	include: one child
        #   func def: one child
        #   declaration: two children, only first one is useful
        # ==> take first child (#0), and return to parent.

        return self.manuallyVisitChild(ctx.getChild(0))
    # END

    # Visit a parse tree produced by CParser#include.
    def visitInclude(self, ctx: CParser.IncludeContext):
        return IncludeNode()

    # END

    # Visit a parse tree produced by CParser#declaration.
    def visitDeclaration(self, ctx: CParser.DeclarationContext):

        # retrieve type: child #0
        decl_type = self.manuallyVisitChild(ctx.getChild(0))

        # retrieve decl list: child #1-n
        #    these are declarations separated by ','
        #    visit each of these and add to list, but skip commas
        #
        raw_decltr_list = list(ctx.getChildren())[1:]

        declarators = [child for child in raw_decltr_list if child.getText() != ","]

        print("type:",decl_type)

        # turn the parse tree nodes into AST nodes by visiting them
        ast_node_list = [self.manuallyVisitChild(decltr) for decltr in declarators]

        # hack: manually add the type since here we have the type
        for decl_node in ast_node_list:
            decl_node.symbol_type = decl_type

        for decl_node in ast_node_list:
            print("dcl type:",decl_node.getType())
            print("id:",decl_node.getID())

        return ast_node_list
    # END

    # Visit a parse tree produced by CParser#funcDecl.
    def visitFuncDecl(self, ctx: CParser.FuncDeclContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#varDeclSimple.
    def visitVarDeclSimple(self, ctx: CParser.VarDeclSimpleContext):
        id_with_ptr = self.manuallyVisitChild(ctx.getChild(0))

        return VarDeclDefault(None, id_with_ptr)
    # ENDCLASS

    # Visit a parse tree produced by CParser#varDeclArray.
    def visitVarDeclArray(self, ctx: CParser.VarDeclArrayContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#varDeclInit.
    def visitVarDeclInit(self, ctx: CParser.VarDeclInitContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#param.
    def visitParam(self, ctx: CParser.ParamContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#func_def.
    def visitFunc_def(self, ctx: CParser.Func_defContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#statement.
    def visitStatement(self, ctx: CParser.StatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#if_statement.
    def visitIf_statement(self, ctx: CParser.If_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#forLoop.
    def visitForLoop(self, ctx: CParser.ForLoopContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#whileLoop.
    def visitWhileLoop(self, ctx: CParser.WhileLoopContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#forCondWithDecl.
    def visitForCondWithDecl(self, ctx: CParser.ForCondWithDeclContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#forCondNoDecl.
    def visitForCondNoDecl(self, ctx: CParser.ForCondNoDeclContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#compound_statement.
    def visitCompound_statement(self, ctx: CParser.Compound_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#block_item.
    def visitBlock_item(self, ctx: CParser.Block_itemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#jumpReturn.
    def visitJumpReturn(self, ctx: CParser.JumpReturnContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#jumpBreak.
    def visitJumpBreak(self, ctx: CParser.JumpBreakContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#jumpContinue.
    def visitJumpContinue(self, ctx: CParser.JumpContinueContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#expression_statement.
    def visitExpression_statement(self, ctx: CParser.Expression_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#expression.
    def visitExpression(self, ctx: CParser.ExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#assignment_eoonxpr.
    def visitAssignment_expr(self, ctx: CParser.Assignment_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#assignment_operator.
    def visitAssignment_operator(self, ctx: CParser.Assignment_operatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#logical_or_expr.
    def visitLogical_or_expr(self, ctx: CParser.Logical_or_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#logical_and_expr.
    def visitLogical_and_expr(self, ctx: CParser.Logical_and_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#equality_expr.
    def visitEquality_expr(self, ctx: CParser.Equality_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#relational_expr.
    def visitRelational_expr(self, ctx: CParser.Relational_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#additive_expr.
    def visitAdditive_expr(self, ctx: CParser.Additive_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#multiplicative_expr.
    def visitMultiplicative_expr(self, ctx: CParser.Multiplicative_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#cast_expr.
    def visitCast_expr(self, ctx: CParser.Cast_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#unaryAsPostfix.
    def visitUnaryAsPostfix(self, ctx: CParser.UnaryAsPostfixContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#prefixDec.
    def visitPrefixDec(self, ctx: CParser.PrefixDecContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#prefixInc.
    def visitPrefixInc(self, ctx: CParser.PrefixIncContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#unaryOp.
    def visitUnaryOp(self, ctx: CParser.UnaryOpContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#unary_operator.
    def visitUnary_operator(self, ctx: CParser.Unary_operatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#arrayAccesExpr.
    def visitArrayAccesExpr(self, ctx: CParser.ArrayAccesExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#postfixDec.
    def visitPostfixDec(self, ctx: CParser.PostfixDecContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#primitiveExpr.
    def visitPrimitiveExpr(self, ctx: CParser.PrimitiveExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#funcCall.
    def visitFuncCall(self, ctx: CParser.FuncCallContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#postfixInc.
    def visitPostfixInc(self, ctx: CParser.PostfixIncContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#parenExpr.
    def visitParenExpr(self, ctx: CParser.ParenExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#simpleId.
    def visitSimpleId(self, ctx: CParser.SimpleIdContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#constantExpr.
    def visitConstantExpr(self, ctx: CParser.ConstantExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#prim_type.
    def visitPrim_type(self, ctx: CParser.Prim_typeContext):
        # skip this node and just return the child.
        return self.manuallyVisitChild(ctx.getChild(0)) 

    # Visit a parse tree produced by CParser#type_int.
    def visitType_int(self, ctx: CParser.Type_intContext):
        return TypeInt()

    # Visit a parse tree produced by CParser#type_float.
    def visitType_float(self, ctx: CParser.Type_floatContext):
        return TypeFloat()

    # Visit a parse tree produced by CParser#type_char.
    def visitType_char(self, ctx: CParser.Type_charContext):
        return TypeChar()

    # Visit a parse tree produced by CParser#type_void.
    def visitType_void(self, ctx: CParser.Type_voidContext):
        return TypeVoid()

    # Visit a parse tree produced by CParser#type_bool.
    def visitType_bool(self, ctx: CParser.Type_boolContext):
        return TypeBool()

    # Visit a parse tree produced by CParser#id_with_ptr.
    def visitId_with_ptr(self, ctx: CParser.Id_with_ptrContext):
        pointer_amount = len(list(ctx.getChildren())) - 1  # -1 because of identifier

        # take child that contains the identifier
        identifier_child = ctx.getChild(pointer_amount)

        # process child into AST node.
        identifier = self.manuallyVisitChild(identifier_child)

        return IdWithPtr(identifier, pointer_amount)

    # Visit a parse tree produced by CParser#identifier.
    def visitIdentifier(self, ctx: CParser.IdentifierContext):
        return IdentifierNode(ctx.getText())

    # Visit a parse tree produced by CParser#pointer.
    def visitPointer(self, ctx: CParser.PointerContext):
        pass

    # Visit a parse tree produced by CParser#constant.
    def visitConstant(self, ctx: CParser.ConstantContext):
        return self.manuallyVisitChild(ctx.getChild(0))

    # Visit a parse tree produced by CParser#int_constant.
    def visitInt_constant(self, ctx: CParser.Int_constantContext):
        return IntegerConstantExpr(ctx.getText())

    # Visit a parse tree produced by CParser#float_constant.
    def visitFloat_constant(self, ctx: CParser.Float_constantContext):
        return FloatConstantExpr(ctx.getText())

    # Visit a parse tree produced by CParser#str_constant.
    def visitStr_constant(self, ctx: CParser.Str_constantContext):
        return StringConstantExpr(ctx.getText())

    # Visit a parse tree produced by CParser#char_constant.
    def visitChar_constant(self, ctx: CParser.Char_constantContext):
        return CharConstantExpr(ctx.getText())

    # Visit a parse tree produced by CParser#bool_constant.
    def visitBool_constant(self, ctx: CParser.Bool_constantContext):
        return BoolConstantExpr(ctx.getText())
