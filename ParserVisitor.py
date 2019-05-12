from antlr_files.CVisitor import CVisitor
from antlr_files.CParser import CParser
from ASTTreeNodes import *

from Logger import Logger
from CompilerException import AstCreationException


class ParserVisitor(CVisitor):

    def manuallyVisitChild(self, child_node):
        return child_node.accept(self)

    # END

    # Visit a parse tree produced by CParser#program.
    def visitProgram(self, ctx: CParser.ProgramContext):

        program_node = ProgramNode().setLineNr(ctx.start.line).setColNr(ctx.start.column)

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
        return IncludeNode().setLineNr(ctx.start.line).setColNr(ctx.start.column)

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

        return FuncDecl(ctx.temp_typeName, func_id, ptr_count, param_list).setLineNr(ctx.start.line).setColNr(
            ctx.start.column)

    # Visit a parse tree produced by CParser#varDeclSimple.
    def visitVarDeclSimple(self, ctx: CParser.VarDeclSimpleContext):
        var_id, ptr_count = self.manuallyVisitChild(ctx.getChild(0))

        if ctx.temp_typeName == 'void':
            Logger.error("Cannot declare variable or pointer with type 'void' at line {}.".format(ctx.start.line))
            raise AstCreationException()

        # temporarily set type to None
        return VarDeclDefault(ctx.temp_typeName, var_id, ptr_count).setLineNr(ctx.start.line).setColNr(ctx.start.column)

    # ENDCLASS

    # Visit a parse tree produced by CParser#varDeclArray.
    def visitVarDeclArray(self, ctx: CParser.VarDeclArrayContext):
        # child 0 is identifier with ptr
        # child 1 is "["
        # child 2 is size_expr
        # child 3 is "]"

        var_id, ptr_count = self.manuallyVisitChild(ctx.getChild(0))
        size_expr = self.manuallyVisitChild(ctx.getChild(2))

        if ctx.temp_typeName == 'void' and ptr_count == 0:
            Logger.error("Cannot declare array with type 'void' at line {}.".format(ctx.start.line))
            raise AstCreationException()

        if not isinstance(size_expr, IntegerConstantExpr):
            Logger.error("Array size must be specified by integer constant. Error on line {}.".format(ctx.start.line))
            raise AstCreationException()

        # temporarily set type to None
        return ArrayDecl(ctx.temp_typeName, var_id, ptr_count, size_expr).setLineNr(ctx.start.line).setColNr(
            ctx.start.column)

    # Visit a parse tree produced by CParser#varDeclInit.
    def visitVarDeclInit(self, ctx: CParser.VarDeclInitContext):
        # child 0 is identifier with ptr
        # child 1 is "="
        # child 2 is init_expr

        var_id, ptr_count = self.manuallyVisitChild(ctx.getChild(0))
        init_expr = self.manuallyVisitChild(ctx.getChild(2))

        if ctx.temp_typeName == 'void':
            Logger.error("Cannot declare variable or pointer with type 'void' at line {}.".format(ctx.start.line))
            raise AstCreationException()

        # temporarily set type to None
        return VarDeclWithInit(ctx.temp_typeName, var_id, ptr_count, init_expr).setLineNr(ctx.start.line).setColNr(
            ctx.start.column)

    # Visit a parse tree produced by CParser#param.
    def visitParam(self, ctx: CParser.ParamContext):
        # child 0 is type
        # child 1 is (id, ptr_count) from id_with_ptr

        # string that contains the name of the type
        param_type = self.manuallyVisitChild(ctx.getChild(0))

        # tuple (id, ptr_count)
        param_id, ptr_count = self.manuallyVisitChild(ctx.getChild(1))

        if param_type == 'void' and ptr_count == 0:
            Logger.error("Cannot declare function parameter with type 'void' at line {}.".format(ctx.start.line))
            raise AstCreationException()

        return FuncParam(param_type, param_id, ptr_count).setLineNr(ctx.start.line).setColNr(ctx.start.column)

    # Visit a parse tree produced by CParser#func_def.
    def visitFunc_def(self, ctx: CParser.Func_defContext):
        # type id_with_ptr ( param , param ) compound_statement
        return_type = self.manuallyVisitChild(ctx.getChild(0))

        # tuple that contains the declared identifier and the pointer count
        func_id, ptr_count = self.manuallyVisitChild(ctx.getChild(1))

        # the body is the last statement
        body_child = ctx.getChild(ctx.getChildCount() - 1)
        compound_statement = self.manuallyVisitChild(body_child)[0]
        body = Body(compound_statement.child_list).setLineNr(ctx.start.line).setColNr(ctx.start.column)

        # the parameter part of the function def is the entire
        # child list without the first and last child
        param_section = list(ctx.getChildren())[2:-1]

        param_children = filter(lambda c: not c.getText() in ['(', ',', ')'], param_section)

        param_nodes = [self.manuallyVisitChild(child) for child in param_children]

        return FuncDef(return_type, func_id, ptr_count, param_nodes, body).setLineNr(ctx.start.line).setColNr(
            ctx.start.column)

    # Visit a parse tree produced by CParser#statement.
    def visitStatement(self, ctx: CParser.StatementContext):
        return self.manuallyVisitChild(ctx.getChild(0))

    # Visit a parse tree produced by CParser#if_statement.
    def visitIf_statement(self, ctx: CParser.If_statementContext):
        # if ( expr ) statement
        # if ( expr ) statement else statement

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

            if_body = Body(compound_statement.child_list).setLineNr(ctx.start.line).setColNr(ctx.start.column)
        else:
            if_body = Body(if_body_list).setLineNr(ctx.start.line).setColNr(ctx.start.column)

        if len(else_body_list) == 1 and isinstance(else_body_list[0], CompoundStmt):
            compound_statement = else_body_list[0]

            else_body = Body(compound_statement.child_list).setLineNr(ctx.start.line).setColNr(ctx.start.column)
        else:
            else_body = Body(else_body_list).setLineNr(ctx.start.line).setColNr(ctx.start.column)

        return [BranchStmt(cond_expr, if_body, else_body).setLineNr(ctx.start.line).setColNr(ctx.start.column)]

    # Visit a parse tree produced by CParser#forLoop.
    def visitForLoop(self, ctx: CParser.ForLoopContext):
        # FOR LEFT_PAREN for_condition RIGHT_PAREN statement # forLoop

        # convert to while loop:
        #
        # {
        #   init statement: for expr in init: ExpressionStatement(expr), etc etc
        #
        #   while(cond_expr)
        #   {
        #      {
        #           <statements>
        #      }
        #      iter_expr: for expr in iter: ExpressionStatement(expr), etc etc
        #   }

        statements = list()

        init_list, cond_expr, iter_list = self.manuallyVisitChild(ctx.getChild(2))

        # returns list of statements
        body_statements = self.manuallyVisitChild(ctx.getChild(4))

        # if the statement after the forloop loop, is a compound statement
        # we can use the compound.
        # Otherwise, transform statement to compound.
        if len(body_statements) == 1 and isinstance(body_statements[0], CompoundStmt):
            pass
            #body = Body(compound_statement.child_list).setLineNr(ctx.start.line).setolNr(ctx.start.column)
        else:
            # body = Body(body_statements).setLineNr(ctx.start.line).setColNr(ctx.start.column)
            body_statements = [CompoundStmt([body_statements])]

        # extend with iter expr
        body_statements.extend(iter_list)
        while_body = Body(body_statements).setLineNr(ctx.start.line).setColNr(ctx.start.column)
        while_stat = WhileStmt(cond_expr, while_body).setLineNr(ctx.start.line).setColNr(ctx.start.column)

        statements.extend(init_list)
        statements.append(while_stat)
        return [CompoundStmt(statements).setLineNr(ctx.start.line).setColNr(ctx.start.column)]

    # Visit a parse tree produced by CParser#forCondWithDecl.
    def visitFor_condition(self, ctx: CParser.For_conditionContext):
        # declaration SC expression? SC expression? # forCondWithDecl
        # expression? SC assignment_expr? SC expression? # forCondNoDecl

        targets = ["INIT", "COND", "ITER"]
        cur_target = 0  # specifies what we're looking for

        init_list = []
        cond_expr = BoolConstantExpr("true").setLineNr(ctx.start.line).setColNr(ctx.start.column) # empty condition is "true"
        iter_list = []

        for i in range(0, ctx.getChildCount()):
            if ctx.getChild(i).getText() == ";":
                # separator
                # go to next target
                cur_target += 1
            else:
                # we found something: assign it to the target
                if targets[cur_target] == "INIT":
                    init_list = self.manuallyVisitChild(ctx.getChild(i))
                elif targets[cur_target] == "COND":
                    cond_expr = self.manuallyVisitChild(ctx.getChild(i))
                elif targets[cur_target] == "ITER":
                    iter_list = self.manuallyVisitChild(ctx.getChild(i))

        return (init_list, cond_expr, iter_list)

    # Visit a parse tree produced by CParser#whileLoop.
    def visitWhileLoop(self, ctx: CParser.WhileLoopContext):
        # while ( expr ) statement
        cond_expr = self.manuallyVisitChild(ctx.getChild(2))
        body_statements = self.manuallyVisitChild(ctx.getChild(4))

        # if the statement after the while loop, is a compound statement
        # we use its contents instead of the compound itself.
        if len(body_statements) == 1 and isinstance(body_statements[0], CompoundStmt):
            compound_statement = body_statements[0]

            body = Body(compound_statement.child_list).setLineNr(ctx.start.line).setColNr(ctx.start.column)
        else:
            body = Body(body_statements).setLineNr(ctx.start.line).setColNr(ctx.start.column)

        return [WhileStmt(cond_expr, body).setLineNr(ctx.start.line).setColNr(ctx.start.column)]

    # Visit a parse tree produced by CParser#compound_statement.
    def visitCompound_statement(self, ctx: CParser.Compound_statementContext):
        # { child, child, child }
        # n children
        # each child is a list of either statement or declaration

        # remove braces
        child_part = list(ctx.getChildren())[1:-1]

        block_item_list = [self.manuallyVisitChild(child) for child in child_part]

        # each block_item is a list of statements
        statement_list = []

        for block_item in block_item_list:
            statement_list.extend(block_item)

        return [CompoundStmt(statement_list).setLineNr(ctx.start.line).setColNr(ctx.start.column)]

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
        return [ReturnStatement().setLineNr(ctx.start.line).setColNr(ctx.start.column)]

    # Visit a parse tree produced by CParser#jumpReturnWithExpr.
    def visitJumpReturnWithExpr(self, ctx: CParser.JumpReturnWithExprContext):

        # child 0: 'return'
        # child 1: return value
        return_value = self.manuallyVisitChild(ctx.getChild(1))

        # child 2: ';'

        return [ReturnWithExprStatement(return_value).setLineNr(ctx.start.line).setColNr(ctx.start.column)]

    # Visit a parse tree produced by CParser#jumpBreak.
    def visitJumpBreak(self, ctx: CParser.JumpBreakContext):
        return [BreakStatement().setLineNr(ctx.start.line).setColNr(ctx.start.column)]

    # Visit a parse tree produced by CParser#jumpContinue.
    def visitJumpContinue(self, ctx: CParser.JumpContinueContext):
        return [ContinueStatement().setLineNr(ctx.start.line).setColNr(ctx.start.column)]

    # Visit a parse tree produced by CParser#expression_statement.
    def visitExpression_statement(self, ctx: CParser.Expression_statementContext):
        # only ';' provided -> empty statement
        if ctx.getChildCount() == 1:
            return []

        # retrieve all expressions that are part of the statement
        expr_list = self.manuallyVisitChild(ctx.getChild(0))

        # one statement per expression
        statement_list = [ExpressionStatement(expr).setLineNr(ctx.start.line).setColNr(ctx.start.column) for expr in
                          expr_list]

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

        left = self.manuallyVisitChild(ctx.getChild(0))
        operator = self.manuallyVisitChild(ctx.getChild(1))  # visits the operator node, and returns string
        right = self.manuallyVisitChild(ctx.getChild(2))

        if not is_valid_assignment_target_expr(left):
            Logger.error(
                "Invalid target '{}' for assignment on line {}.".format(get_full_context_source(ctx.getChild(0)),
                                                                        ctx.start.line))
            raise AstCreationException()

        if operator == "=":
            return AssignmentExpr(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)
        elif operator == "+=":
            add_expr = AddExpr(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)
            return AssignmentExpr(left, add_expr).setLineNr(ctx.start.line).setColNr(ctx.start.column)
            # return AddAssignmentExpr(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)
        elif operator == "-=":
            sub_expr = SubExpr(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)
            return AssignmentExpr(left, sub_expr).setLineNr(ctx.start.line).setColNr(ctx.start.column)
            # return SubAssignmentExpr(left, ri ght).setLineNr(ctx.start.line).setColNr(ctx.start.column)
        elif operator == "*=":
            mul_expr = MulExpr(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)
            return AssignmentExpr(left, mul_expr).setLineNr(ctx.start.line).setColNr(ctx.start.column)
            # return MulAssignmentExpr(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)
        elif operator == "/=":
            div_expr = DivExpr(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)
            return AssignmentExpr(left, div_expr).setLineNr(ctx.start.line).setColNr(ctx.start.column)
            # return DivAssignmentExpr(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)
        else:
            raise Exception("Invalid operator for assignment expr: {}".format(operator))

    # Visit a parse tree produced by CParser#assignment_operator.
    def visitAssignment_operator(self, ctx: CParser.Assignment_operatorContext):
        return ctx.getText()

    # Visit a parse tree produced by CParser#logical_or_expr.
    def visitLogical_or_expr(self, ctx: CParser.Logical_or_exprContext):
        # logical AND expression
        if ctx.getChildCount() == 1:
            return self.manuallyVisitChild(ctx.getChild(0))

        # TODO check constant

        # get left: child #0
        left = self.manuallyVisitChild(ctx.getChild(0))
        # child #1: "||" or "or"
        # get right: child #2
        right = self.manuallyVisitChild(ctx.getChild(2))

        return LogicOrExpr(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)

    # Visit a parse tree produced by CParser#logical_and_expr.
    def visitLogical_and_expr(self, ctx: CParser.Logical_and_exprContext):
        # equality expression
        if ctx.getChildCount() == 1:
            return self.manuallyVisitChild(ctx.getChild(0))

        # TODO check constant

        # get left: child #0
        left = self.manuallyVisitChild(ctx.getChild(0))
        # child #1: "&&" or "and"
        # get right: child #2
        right = self.manuallyVisitChild(ctx.getChild(2))

        return LogicAndExpr(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)

    # Visit a parse tree produced by CParser#equality_expr.
    def visitEquality_expr(self, ctx: CParser.Equality_exprContext):
        # relational expression
        if ctx.getChildCount() == 1:
            return self.manuallyVisitChild(ctx.getChild(0))

        left = self.manuallyVisitChild(ctx.getChild(0))
        operator = ctx.getChild(1).getText()
        right = self.manuallyVisitChild(ctx.getChild(2))

        if operator == "==":
            # TODO check constant
            return EqualityExpr(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)
        elif operator == "!=":
            # TODO check constant
            return InequalityExpr(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)
        else:
            raise Exception("Invalid operator for equality expr: {}".format(operator))

    # Visit a parse tree produced by CParser#relational_expr.
    def visitRelational_expr(self, ctx: CParser.Relational_exprContext):
        # additive expression
        if ctx.getChildCount() == 1:
            return self.manuallyVisitChild(ctx.getChild(0))

        left = self.manuallyVisitChild(ctx.getChild(0))
        operator = ctx.getChild(1).getText()
        right = self.manuallyVisitChild(ctx.getChild(2))

        if operator == ">":
            # TODO check constant
            return CompGreater(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)
        elif operator == "<":
            # TODO check constant
            return CompLess(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)
        elif operator == ">=":
            # TODO check constant
            return CompGreaterEqual(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)
        elif operator == "<=":
            # TODO check constant
            return CompLessEqual(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)
        else:
            raise Exception("Invalid operator for comparison expr: {}".format(operator))

    # Visit a parse tree produced by CParser#additive_expr.
    def visitAdditive_expr(self, ctx: CParser.Additive_exprContext):
        # multiplicative expression
        if ctx.getChildCount() == 1:
            return self.manuallyVisitChild(ctx.getChild(0))

        left = self.manuallyVisitChild(ctx.getChild(0))
        operator = ctx.getChild(1).getText()
        right = self.manuallyVisitChild(ctx.getChild(2))

        if operator == "+":
            # TODO check constant
            return AddExpr(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)
        elif operator == "-":
            # TODO check constant
            return SubExpr(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)
        else:
            raise Exception("Invalid operator for additive expr: {}".format(operator))

    # Visit a parse tree produced by CParser#multiplicative_expr.
    def visitMultiplicative_expr(self, ctx: CParser.Multiplicative_exprContext):
        # cast expression
        if ctx.getChildCount() == 1:
            return self.manuallyVisitChild(ctx.getChild(0))

        left = self.manuallyVisitChild(ctx.getChild(0))
        operator = ctx.getChild(1).getText()
        right = self.manuallyVisitChild(ctx.getChild(2))

        if operator == "*":
            # TODO check constant
            return MulExpr(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)
        elif operator == "/":
            # TODO check constant
            return DivExpr(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)
        elif operator == "%":
            # TODO check constant
            return ModExpr(left, right).setLineNr(ctx.start.line).setColNr(ctx.start.column)
        else:
            raise Exception("Invalid operator for multiplicative expr: {}".format(operator))

    # Visit a parse tree produced by CParser#cast_expr.
    def visitCast_expr(self, ctx: CParser.Cast_exprContext):
        if ctx.getChildCount() == 1:
            return self.manuallyVisitChild(ctx.getChild(0))

        # format is now "prim_type pointerstar* expr"

        # the last child contains the expression
        expr = self.manuallyVisitChild(ctx.getChild(ctx.getChildCount() - 1))

        # format: 
        type_spec = [ctx for ctx in list(ctx.getChildren())[0:-1] if not ctx.getText() in ['(', ')']]

        # visit each type-child and retrieve type name
        type_list = [self.manuallyVisitChild(ctx) for ctx in type_spec]

        typename = "".join(type_list)

        return CastExpr(VariableType(typename), expr).setLineNr(ctx.start.line).setColNr(ctx.start.column)

    # Visit a parse tree produced by CParser#unaryAsPostfix.
    def visitUnaryAsPostfix(self, ctx: CParser.UnaryAsPostfixContext):
        return self.manuallyVisitChild(ctx.getChild(0))

    # Visit a parse tree produced by CParser#unaryOp.
    def visitUnaryOp(self, ctx: CParser.UnaryOpContext):
        operator = self.manuallyVisitChild(ctx.getChild(0))
        expr = self.manuallyVisitChild(ctx.getChild(1))

        if operator == "+":
            # TODO check constant
            return PlusPrefixExpr(expr).setLineNr(ctx.start.line).setColNr(ctx.start.column)

        elif operator == "-":
            # TODO check constant
            return MinPrefixExpr(expr).setLineNr(ctx.start.line).setColNr(ctx.start.column)

        elif operator == "not" or operator == '!':
            # TODO check constant
            return LogicNotExpr(expr).setLineNr(ctx.start.line).setColNr(ctx.start.column)

        elif operator == "*":
            return PointerDerefExpr(expr).setLineNr(ctx.start.line).setColNr(ctx.start.column)

        elif operator == "&":
            return AddressExpr(expr).setLineNr(ctx.start.line).setColNr(ctx.start.column)

        # note: the postfix counterparts are handled somewhere else
        elif operator == "++":
            if not is_valid_assignment_target_expr(expr):
                Logger.error("Invalid target '{}' for prefix increment on line '{}'".format(get_full_context_source(ctx.getChild(1)), ctx.start.line))
                raise AstCreationException()

            return PrefixIncExpr(expr).setLineNr(ctx.start.line).setColNr(ctx.start.column)

        elif operator == "--":
            if not is_valid_assignment_target_expr(expr):
                Logger.error("Invalid target '{}' for prefix decrement on line '{}'".format(get_full_context_source(ctx.getChild(1)), ctx.start.line))
                raise AstCreationException()

            return PrefixDecExpr(expr).setLineNr(ctx.start.line).setColNr(ctx.start.column)

        else:
            raise Exception("Invalid operator '{}'".format(operator))

    # Visit a parse tree produced by CParser#unary_operator.
    def visitUnary_operator(self, ctx: CParser.Unary_operatorContext):
        # return the operator to be checked in visitUnaryOp
        return ctx.getText()

    # Visit a parse tree produced by CParser#arrayAccesExpr.
    def visitArrayAccesExpr(self, ctx: CParser.ArrayAccesExprContext):
        # child #0 the array identifier
        target_array_id = self.manuallyVisitChild(ctx.getChild(0))
        target_array = IdentifierExpr(target_array_id).setLineNr(ctx.start.line).setColNr(ctx.start.column)

        # child #1 is '['
        index_expr = self.manuallyVisitChild(ctx.getChild(2))
        # child # 3 is ']'

        return ArrayAccessExpr(target_array, index_expr).setLineNr(ctx.start.line).setColNr(ctx.start.column)

    # Visit a parse tree produced by CParser#postfixDec.
    def visitPostfixDec(self, ctx: CParser.PostfixDecContext):
        expression = self.manuallyVisitChild(ctx.getChild(0))

        if not is_valid_assignment_target_expr(expression):
            Logger.error("Invalid target '{}' for postfix decrement on line '{}'".format(get_full_context_source(ctx.getChild(0)), ctx.start.line))
            raise AstCreationException()

        return PostfixDecExpr(expression).setLineNr(ctx.start.line).setColNr(ctx.start.column)

    # Visit a parse tree produced by CParser#primitiveExpr.
    def visitPrimitiveExpr(self, ctx: CParser.PrimitiveExprContext):
        return self.manuallyVisitChild(ctx.getChild(0))

    # Visit a parse tree produced by CParser#funcCall.
    def visitFuncCall(self, ctx: CParser.FuncCallContext):
        # function id is a IdentifierExpression
        function_id_str = self.manuallyVisitChild(ctx.getChild(0))
        function_id = IdentifierExpr(function_id_str).setLineNr(ctx.start.line).setColNr(ctx.start.column)

        arg_ctx_list = [node for node in list(ctx.getChildren())[1:] if not node.getText() in [',', '(', ')']]

        argument_exprs = [self.manuallyVisitChild(arg_ctx) for arg_ctx in arg_ctx_list]

        # arguments come from expression visit method, which returns lists
        argument_nodes = []
        for arg_expr_list in argument_exprs:
            argument_nodes.extend(arg_expr_list)

        return FuncCallExpr(function_id, argument_nodes).setLineNr(ctx.start.line).setColNr(ctx.start.column)

    # Visit a parse tree produced by CParser#postfixInc.
    def visitPostfixInc(self, ctx: CParser.PostfixIncContext):
        expression = self.manuallyVisitChild(ctx.getChild(0))

        if not is_valid_assignment_target_expr(expression):
            Logger.error("Invalid target '{}' for postfix decrement on line '{}'".format(get_full_context_source(ctx.getChild(0)), ctx.start.line))
            raise AstCreationException()

        return PostfixIncExpr(expression).setLineNr(ctx.start.line).setColNr(ctx.start.column)

    # Visit a parse tree produced by CParser#parenExpr.
    def visitParenExpr(self, ctx: CParser.ParenExprContext):
        # here we ignore the "(" and ")" and simply return the contained expression.
        # this is because the goal of using parenthesis is altering
        # precedence. Precedence is handled by the parser, not by the AST tree.

        # note this returns a single assignment_expr, since we no longer directly use expression
        return self.manuallyVisitChild(ctx.getChild(1))

    # Visit a parse tree produced by CParser#idExpr.
    def visitIdExpr(self, ctx: CParser.IdExprContext):
        # return an identifier expression

        id_str = self.manuallyVisitChild(ctx.getChild(0))

        return IdentifierExpr(id_str).setLineNr(ctx.start.line).setColNr(ctx.start.column)

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
        return IntegerConstantExpr(ctx.getText()).setLineNr(ctx.start.line).setColNr(ctx.start.column)

    # Visit a parse tree produced by CParser#float_constant.
    def visitFloat_constant(self, ctx: CParser.Float_constantContext):
        return FloatConstantExpr(ctx.getText()).setLineNr(ctx.start.line).setColNr(ctx.start.column)

    # Visit a parse tree produced by CParser#str_constant.
    def visitStr_constant(self, ctx: CParser.Str_constantContext):
        constant = ctx.getText().rstrip("\"").lstrip("\"")  # remove "
        return StringConstantExpr(constant).setLineNr(ctx.start.line).setColNr(ctx.start.column)

    # Visit a parse tree produced by CParser#char_constant.
    def visitChar_constant(self, ctx: CParser.Char_constantContext):
        return CharConstantExpr(ctx.getText()).setLineNr(ctx.start.line).setColNr(ctx.start.column)

    # Visit a parse tree produced by CParser#bool_constant.
    def visitBool_constant(self, ctx: CParser.Bool_constantContext):
        return BoolConstantExpr(ctx.getText()).setLineNr(ctx.start.line).setColNr(ctx.start.column)


def is_valid_assignment_target_expr(target_expr):
    """
        Determines whether specified target expression node is a valid target for assignment.

        Note: it should also be determine if the type of the node still allows for 
        a valid assignment, this function will only determine fitness w.r.t. Expression type.
    """

    # note: this is obtained by analysing the grammar
    # Also retrieving an object with a getter-function and assigning to it is still possible due to the derefence expression:
    #       "*get_object_location() = new_object_value"

    if isinstance(target_expr, ArrayAccessExpr) or isinstance(target_expr, IdentifierExpr) or isinstance(target_expr,
                                                                                                         PointerDerefExpr):
        return True

    return False


def get_full_context_source(ctx):
    """
        Retrieve the full source code that is behind a parser node.
    """
    start = ctx.start
    stop = ctx.stop
    start_idx = start.start
    stop_idx = stop.stop

    stream = start.getInputStream()

    return stream.getText(start_idx, stop_idx)
