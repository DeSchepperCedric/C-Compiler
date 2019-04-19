from antlr_files.CVisitor import CVisitor
from antlr_files.CParser import CParser
from ASTTreeNodes import *


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

        return program_node

    # END

    # Visit a parse tree produced by CParser#top_level_node.
    def visitTop_level_node(self, ctx: CParser.Top_level_nodeContext):
        # top level node has
        #    include: one child
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
        # this is a string that contains the name of the type.
        decl_type = self.manuallyVisitChild(ctx.getChild(0))

        # retrieve decl list: child #1-n
        #    these are declarations separated by ','
        #    visit each of these and add to list, but skip commas
        #
        raw_decltr_list = list(ctx.getChildren())[1:]

        declarators = [child for child in raw_decltr_list if child.getText() != ","]

        # temporarily give the parse tree nodes type information.
        for decltr_ctx in declarators:
            decltr_ctx.temp_typeName = decl_type

        # turn the parse tree nodes into AST nodes by visiting them
        ast_node_list = [self.manuallyVisitChild(decltr) for decltr in declarators]

        return ast_node_list

    # END

    # Visit a parse tree produced by CParser#funcDecl.
    def visitFuncDecl(self, ctx: CParser.FuncDeclContext):

        func_id, ptr_count = self.manuallyVisitChild(ctx.getChild(0))

        # remove all '(', ')', ','
        param_declarations = [node for node in list(ctx.getChildren())[1:] if not node.getText() in [',', '(', ')']]

        param_list = [self.manuallyVisitChild(decl) for decl in param_declarations]

        return FuncDecl(ctx.temp_typeName, func_id, ptr_count, param_list)

    # Visit a parse tree produced by CParser#varDeclSimple.
    def visitVarDeclSimple(self, ctx: CParser.VarDeclSimpleContext):
        var_id, ptr_count = self.manuallyVisitChild(ctx.getChild(0))

        # temporarily set type to None
        return VarDeclDefault(ctx.temp_typeName, var_id, ptr_count)

    # ENDCLASS

    # Visit a parse tree produced by CParser#varDeclArray.
    def visitVarDeclArray(self, ctx: CParser.VarDeclArrayContext):
        # child 0 is identifier with ptr
        # child 1 is "["
        # child 2 is size_expr
        # child 3 is "]"

        var_id, ptr_count = self.manuallyVisitChild(ctx.getChild(0))
        size_expr = self.manuallyVisitChild(ctx.getChild(2))

        # temporarily set type to None
        return ArrayDecl(ctx.temp_typeName, var_id, ptr_count, size_expr)

    # Visit a parse tree produced by CParser#varDeclInit.
    def visitVarDeclInit(self, ctx: CParser.VarDeclInitContext):
        # child 0 is identifier with ptr
        # child 1 is "="
        # child 2 is init_expr

        var_id, ptr_count = self.manuallyVisitChild(ctx.getChild(0))
        init_expr = self.manuallyVisitChild(ctx.getChild(2))

        # temporarily set type to None
        return VarDeclWithInit(ctx.temp_typeName, var_id, ptr_count, init_expr)

    # Visit a parse tree produced by CParser#param.
    def visitParam(self, ctx: CParser.ParamContext):
        # child 0 is type
        # child 1 is id with ptr

        # string that contains the name of the type
        param_type = self.manuallyVisitChild(ctx.getChild(0))

        # tuple (id, ptr_count)
        param_id, ptr_count = self.manuallyVisitChild(ctx.getChild(1))

        return FuncParam(param_type, param_id, ptr_count)

    # Visit a parse tree produced by CParser#func_def.
    def visitFunc_def(self, ctx: CParser.Func_defContext):
        return_type = self.manuallyVisitChild(ctx.getChild(0))

        # tuple that contains the declared identifier and the pointer count
        func_id, ptr_count = self.manuallyVisitChild(ctx.getChild(1))

        # TODO cleaner algo for parameter extraction
        param_list = list()
        # first parameter
        if ctx.getChildCount() >= 6:
            param_list.append(self.manuallyVisitChild(ctx.getChild(3)))

        if ctx.getChildCount() > 6:
            for i in range(5, ctx.getChildCount() - 6, 2):
                param_list.append(self.manuallyVisitChild(ctx.getChild(i)))

        body = self.manuallyVisitChild(ctx.getChild(ctx.getChildCount() - 1))
        return FuncDef(return_type, func_id, ptr_count, param_list, body)

    # is het Body -> Compountstatement -> statements?
    # of Body -> statements?

    # Visit a parse tree produced by CParser#statement.
    def visitStatement(self, ctx: CParser.StatementContext):
        return self.manuallyVisitChild(ctx.getChild(0))

    # TODO fix this: add Body object
    # Visit a parse tree produced by CParser#if_statement.
    def visitIf_statement(self, ctx: CParser.If_statementContext):
        # if ( expr ) statement
        # if ( expr ) statement else statement
        if_body = None
        else_body = None

        # child #2 = expr
        cond_expr = self.manuallyVisitChild(ctx.getChild(2))

        # child #4 = if-body
        if_body_list = self.manuallyVisitChild(ctx.getChild(4))

        # child #6 can be else-body
        else_body_list = []
        if ctx.getChildCount() == 7:
            else_body_list = self.manuallyVisitChild(ctx.getChild(6))

        # if- and else-body are now (maybe empty) list of statement

        # if it is a single compound statement -> unpack and add contents to body
        # if it is a list of statements -> add to body
        if len(if_body_list) == 1 and isinstance(if_body_list[0], CompoundStmt):
            compound_statement = if_body_list[0]

            if_body = Body(compound_statement.child_list)
        else:
            if_body = Body(if_body_list)

        if len(else_body_list) == 1 and isinstance(else_body_list[0], CompoundStmt):
            compound_statement = if_body_list[0]

            if_body = Body(compound_statement.child_list)
        else:
            else_body = Body(else_body_list)

        return [BranchStmt(cond_expr, if_body, else_body)]

    # TODO finish this
    # Visit a parse tree produced by CParser#forLoop.
    def visitForLoop(self, ctx: CParser.ForLoopContext):
        # TODO init? both for declr and no declr?
        # TODO finish this
        return self.visitChildren(ctx)

    # TODO finish this: add Body object
    # Visit a parse tree produced by CParser#whileLoop.
    def visitWhileLoop(self, ctx: CParser.WhileLoopContext):
        expr = self.manuallyVisitChild(ctx.getChild(2))
        body = self.manuallyVisitChild(ctx.getChild(4))
        return [WhileStmt(expr, body)]

    # Visit a parse tree produced by CParser#forCondWithDecl.
    def visitForCondWithDecl(self, ctx: CParser.ForCondWithDeclContext):
        # TODO how to? own node?
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#forCondNoDecl.
    def visitForCondNoDecl(self, ctx: CParser.ForCondNoDeclContext):
        # TODO how to? own node?
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#compound_statement.
    def visitCompound_statement(self, ctx: CParser.Compound_statementContext):
        # n children
        # each child is a list of either statement or declaration

        block_item_list = [self.manuallyVisitChild(child) for child in ctx.getChildren()]

        # each block_item is a list of statements
        statement_list = [block_item for block_item in block_item_list]

        return [CompoundStmt(statement_list)]

    # Visit a parse tree produced by CParser#blockItemStatement.
    def visitBlockItemStatement(self, ctx: CParser.BlockItemStatementContext):
        # this rule will return to Compound statement, it returns a list
        # child 0 = statement

        processed_children = self.manuallyVisitChild(ctx.getChild(0))

        # each child is a list (this is since expressionStatement in C can have multiple expressions)
        # we extends the statement list with each child

        stat_list = [child for child in processed_children]

        return stat_list

    # Visit a parse tree produced by CParser#blockItemDeclaration.
    def visitBlockItemDeclaration(self, ctx: CParser.BlockItemDeclarationContext):
        # this rule will return to Compound statement, it returns a list
        # child 0 = decls (can be multple -> list of decl)
        # child 1 = SC

        return self.manuallyVisitChild(ctx.getChild(0))

    # Visit a parse tree produced by CParser#jumpReturn.
    def visitJumpReturn(self, ctx: CParser.JumpReturnContext):
        return [ReturnStatement()]

    # Visit a parse tree produced by CParser#jumpBreak.
    def visitJumpBreak(self, ctx: CParser.JumpBreakContext):
        return [BreakStatement()]

    # Visit a parse tree produced by CParser#jumpContinue.
    def visitJumpContinue(self, ctx: CParser.JumpContinueContext):
        return [ContinueStatement()]

    # Visit a parse tree produced by CParser#expression_statement.
    def visitExpression_statement(self, ctx: CParser.Expression_statementContext):
        # only ';' provided -> empty statement
        if ctx.getChildCount() == 1:
            return []

        # retrieve all expressions that are part of the statement
        expr_list = self.manuallyVisitChild(ctx.getChild(0))

        # one statement per expression
        statement_list = [ExpressionStatement(expr) for expr in expr_list]

        # return statements
        return statement_list

    # Visit a parse tree produced by CParser#expression.
    def visitExpression(self, ctx: CParser.ExpressionContext):
        # filter out all useless children.
        expr_children = filter(lambda c: c.getText() != ",", ctx.getChildren())

        expr_list = [self.manuallyVisitChild(child) for child in expr_children]

        return expr_list

    # Visit a parse tree produced by CParser#assignment_eoonxpr.
    def visitAssignment_expr(self, ctx: CParser.Assignment_exprContext):
        # logical or expression
        if ctx.getChildCount() == 1:
            return self.manuallyVisitChild(ctx.getChild(0))

        unary_expr = self.manuallyVisitChild(ctx.getChild(0))
        operator = self.manuallyVisitChild(ctx.getChild(1))  # visits the operator node, and returns string
        assignment_expr = self.manuallyVisitChild(ctx.getChild(2))

        return AssignmentExpr(unary_expr, assignment_expr, operator)

    # Visit a parse tree produced by CParser#assignment_operator.
    def visitAssignment_operator(self, ctx: CParser.Assignment_operatorContext):
        return ctx.getText()

    # Visit a parse tree produced by CParser#logical_or_expr.
    def visitLogical_or_expr(self, ctx: CParser.Logical_or_exprContext):
        # logical AND expression
        if ctx.getChildCount() == 1:
            return self.manuallyVisitChild(ctx.getChild(0))

        # get left: child #0
        left = self.manuallyVisitChild(ctx.getChild(0))
        # child #1: "||" or "or"
        # get right: child #2
        right = self.manuallyVisitChild(ctx.getChild(2))

        return LogicOrExpr(left, right)

    # Visit a parse tree produced by CParser#logical_and_expr.
    def visitLogical_and_expr(self, ctx: CParser.Logical_and_exprContext):
        # equality expression
        if ctx.getChildCount() == 1:
            return self.manuallyVisitChild(ctx.getChild(0))

        # get left: child #0
        left = self.manuallyVisitChild(ctx.getChild(0))
        # child #1: "&&" or "and"
        # get right: child #2
        right = self.manuallyVisitChild(ctx.getChild(2))

        return LogicAndExpr(left, right)

    # Visit a parse tree produced by CParser#equality_expr.
    def visitEquality_expr(self, ctx: CParser.Equality_exprContext):
        # relational expression
        if ctx.getChildCount() == 1:
            return self.manuallyVisitChild(ctx.getChild(0))

        left = self.manuallyVisitChild(ctx.getChild(0))
        operator = ctx.getChild(1).getText()
        right = self.manuallyVisitChild(ctx.getChild(2))

        return EqualityExpr(left, right, operator)

    # Visit a parse tree produced by CParser#relational_expr.
    def visitRelational_expr(self, ctx: CParser.Relational_exprContext):
        # additive expression
        if ctx.getChildCount() == 1:
            return self.manuallyVisitChild(ctx.getChild(0))

        left = self.manuallyVisitChild(ctx.getChild(0))
        operator = ctx.getChild(1).getText()
        right = self.manuallyVisitChild(ctx.getChild(2))

        return ComparisonExpr(left, right, operator)

    # Visit a parse tree produced by CParser#additive_expr.
    def visitAdditive_expr(self, ctx: CParser.Additive_exprContext):
        # multiplicative expression
        if ctx.getChildCount() == 1:
            return self.manuallyVisitChild(ctx.getChild(0))

        left = self.manuallyVisitChild(ctx.getChild(0))
        operator = ctx.getChild(1).getText()
        right = self.manuallyVisitChild(ctx.getChild(2))

        return AdditiveExpr(left, right, operator)

    # Visit a parse tree produced by CParser#multiplicative_expr.
    def visitMultiplicative_expr(self, ctx: CParser.Multiplicative_exprContext):
        # cast expression
        if ctx.getChildCount() == 1:
            return self.manuallyVisitChild(ctx.getChild(0))

        left = self.manuallyVisitChild(ctx.getChild(0))
        operator = ctx.getChild(1).getText()
        right = self.manuallyVisitChild(ctx.getChild(2))

        return MultiplicativeExpr(left, right, operator)

    # Visit a parse tree produced by CParser#cast_expr.
    def visitCast_expr(self, ctx: CParser.Cast_exprContext):
        if ctx.getChildCount() == 1:
            return self.manuallyVisitChild(ctx.getChild(0))

        # the last child contains the expression
        expr = self.manuallyVisitChild(ctx.getChild(ctx.getChildCount() - 1))

        # all the child nodes that contain a type
        type_ctx_list = [ctx for ctx in list(ctx.getChildren())[0:-1] if not ctx.getText() in ['(', ')']]

        # visit each type-child and retrieve type name
        type_list = [self.manuallyVisitChild(ctx) for ctx in type_ctx_list]

        return CastExpr(type_list, expr)

    # Visit a parse tree produced by CParser#unaryAsPostfix.
    def visitUnaryAsPostfix(self, ctx: CParser.UnaryAsPostfixContext):
        return self.manuallyVisitChild(ctx.getChild(0))

    # Visit a parse tree produced by CParser#unaryOp.
    def visitUnaryOp(self, ctx: CParser.UnaryOpContext):
        operator = self.manuallyVisitChild(ctx.getChild(0))
        expr = self.manuallyVisitChild(ctx.getChild(1))

        if operator == "+":
            return PlusPrefixExpr(expr)

        elif operator == "-":
            return MinPrefixExpr(expr)

        elif operator == "not" or operator == '!':
            return LogicNotExpr(expr)

        elif operator == "*":
            return PointerDerefExpr(expr)

        elif operator == "&":
            return AddressExpr(expr)

        elif operator == "++":
            return PrefixIncExpr(expr)

        elif operator == "--":
            return PrefixDecExpr(expr)

        else:
            raise Exception("Invalid operator '{}'".format(operator))

    # Visit a parse tree produced by CParser#unary_operator.
    def visitUnary_operator(self, ctx: CParser.Unary_operatorContext):
        # return the operator to be checked in visitUnaryOp
        return ctx.getText()

    # Visit a parse tree produced by CParser#arrayAccesExpr.
    def visitArrayAccesExpr(self, ctx: CParser.ArrayAccesExprContext):
        target_array = self.manuallyVisitChild(ctx.getChild(0))
        # child #1 is '['
        index_expr = self.manuallyVisitChild(ctx.getChild(2))
        # child # 3 is ']'

        return ArrayAccessExpr(target_array, index_expr)

    # Visit a parse tree produced by CParser#postfixDec.
    def visitPostfixDec(self, ctx: CParser.PostfixDecContext):
        expression = self.manuallyVisitChild(ctx.getChild(0))
        return PostfixDecExpr(expression)

    # Visit a parse tree produced by CParser#primitiveExpr.
    def visitPrimitiveExpr(self, ctx: CParser.PrimitiveExprContext):
        return self.manuallyVisitChild(ctx.getChild(0))

    # Visit a parse tree produced by CParser#funcCall.
    def visitFuncCall(self, ctx: CParser.FuncCallContext):
        # function id is a string that contains the name of the function.
        function_id = self.manuallyVisitChild(ctx.getChild(0))

        arg_ctx_list = [node for node in list(ctx.getChildren())[1:] if not node.getText() in [',', '(', ')']]

        argument_nodes = [self.manuallyVisitChild(arg_ctx) for arg_ctx in arg_ctx_list]

        return FuncCallExpr(function_id, argument_nodes)

    # Visit a parse tree produced by CParser#postfixInc.
    def visitPostfixInc(self, ctx: CParser.PostfixIncContext):
        expression = self.manuallyVisitChild(ctx.getChild(0))
        return PostfixIncExpr(expression)

    # Visit a parse tree produced by CParser#parenExpr.
    def visitParenExpr(self, ctx: CParser.ParenExprContext):
        # here we ignore the "(" and ")" and simply return the contained expression.
        # this is because the goal of using parenthesis is altering
        # precedence. Precedence is handled by the parser, not by the AST tree.
        return self.manuallyVisitChild(ctx.getChild(1))

    # Visit a parse tree produced by CParser#idExpr.
    def visitIdExpr(self, ctx: CParser.IdExprContext):
        # return an identifier expression

        id_str = self.manuallyVisitChild(ctx.getChild(0))

        return IdentifierExpr(id_str)

    # Visit a parse tree produced by CParser#constantExpr.
    def visitConstantExpr(self, ctx: CParser.ConstantExprContext):
        return self.manuallyVisitChild(ctx.getChild(0))

    # Visit a parse tree produced by CParser#prim_type.
    def visitPrim_type(self, ctx: CParser.Prim_typeContext):
        # skip this node and just return the child.
        return self.manuallyVisitChild(ctx.getChild(0))

    # Visit a parse tree produced by CParser#type_int.
    def visitType_int(self, ctx: CParser.Type_intContext):
        return "int"

    # Visit a parse tree produced by CParser#type_float.
    def visitType_float(self, ctx: CParser.Type_floatContext):
        return "float"

    # Visit a parse tree produced by CParser#type_char.
    def visitType_char(self, ctx: CParser.Type_charContext):
        return "char"

    # Visit a parse tree produced by CParser#type_void.
    def visitType_void(self, ctx: CParser.Type_voidContext):
        return "void"

    # Visit a parse tree produced by CParser#type_bool.
    def visitType_bool(self, ctx: CParser.Type_boolContext):
        return "bool"

    # Visit a parse tree produced by CParser#id_with_ptr.
    def visitId_with_ptr(self, ctx: CParser.Id_with_ptrContext):
        pointer_amount = ctx.getChildCount() - 1  # -1 because of identifier

        # take child that contains the identifier = last child
        identifier_child = ctx.getChild(pointer_amount)

        # process child. This will return a string
        identifier = self.manuallyVisitChild(identifier_child)

        # return a tuple that contains the information
        # an AST node is not needed
        return identifier, pointer_amount

    # Visit a parse tree produced by CParser#identifier.
    def visitIdentifier(self, ctx: CParser.IdentifierContext):
        # simply return the string representation of the identifier
        return ctx.getText()

    # Visit a parse tree produced by CParser#pointer.
    def visitPointer(self, ctx: CParser.PointerContext):
        raise Exception("'pointer' rule must node be visited during conversion to AST!")

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
