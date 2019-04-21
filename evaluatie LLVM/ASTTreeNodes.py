from SymbolTable import SymbolTable


class ASTNode:
    """
        Base class for all nodes in AST Trees.
    """

    def __init__(self, node_name):
        self.node_name = node_name
        self.symbol_table = None

    def getNodeName(self):
        if self.symbol_table is None:
            return self.node_name
        else: # if the symbol table is present, annotate with star
            return "*"+self.node_name

    def getSymbolTable(self):
        """
            Retrieve the symbol table that node is part of. This can be used
            to check whether or not the node is valid w.r.t. the symbol table.
        """
        return self.symbol_table

    def setSymbolTable(self, symbol_table):
        self.symbol_table = symbol_table

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        """
            Gives a dot presententation for this node/branch/tree.
            
            The opening and closing statements "digraph graphName{", "splines=ortho;", and "}" will only
            be included of 'add_open_close' is set to true.

            Example with add_open_close=False:
                1 [label="20"];
                2 [label="30"];
                1 -> 2;

            Example with add_open_close=True:
                digraph ast_tree {
                splines=ortho;
                1 [label="20"];
                2 [label="30"];
                1 -> 2;
                }

            Params:
                'parent_nr': An integer that specifies the number of the parent node.
                'begin_nr': An integer that specifies what number the beginning dot-node should have.
                'add_open_close': Whether or not the open and closing statements must be added.

            The exact return value is a tuple. The first member is the number of the node that was last added
            to the dot file, the second member is a string that contains the dot contents of this branch.
        """
        raise NotImplementedError()

    def M_defaultToDotImpl(self, children, parent_nr, begin_nr, add_open_close):
        """
            Default implementation for the toDot() method. This method can be called
            from a toDot() method. The children on which the recursion will be performed
            are passed to the parameter 'children'.
        """
        # nr [label="ProgramNode"]
        # nr -> parent_nr

        dotdata = ""

        current_node_nr = begin_nr

        # add self
        dotdata += "{} [label=\"{}\", shape=box]\n".format(current_node_nr, self.getNodeName())

        if parent_nr is not None:
            dotdata += "{}:s -> {}:n\n".format(parent_nr, current_node_nr)

        current_node_nr += 1
        # new_children = list()
        # this is disabled since 'list' as a child can be an indication of a ParserVisitor error
        # for child in children:
        #     if isinstance(child, list):
        #         new_children.extend(child)
        #     else:
        #         new_children.append(child)

        for child in children:
            # the child should have node number 'current_node_nr+1'
            # update the current node number

            current_node_nr, child_dotdata = child.toDot(parent_nr=begin_nr, begin_nr=current_node_nr + 1)

            # add the dotfile data to the current data
            dotdata += child_dotdata

        if add_open_close:
            dotdata = "digraph ast_tree {\nsplines=ortho;\n" + dotdata + "}\n"

        return current_node_nr, dotdata


class ASTTestTermNode(ASTNode):
    """
        A terminal node for testing purposes. Will always display as "TestNode" with no children.
    """

    def __init__(self):
        super().__init__(node_name="TestNode")

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class EmptyNode(ASTNode):
    """
        Node that represents missing statement. Useful for displaying optional components in the AST tree.
    """

    def __init__(self):
        super().__init__(node_name="Ø")

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class ProgramNode(ASTNode):
    """
        Node that represents the entire program. This
        also functions as the root node of the AST tree.
    """

    def __init__(self):
        super().__init__(node_name="Program")
        self.children = []

    def addChild(self, child):
        self.children.append(child)

    def getChildren(self):
        return self.children

    def genSymbolTable(self):
        """
            Recursively traverse the AST tree and create a symbol table for each scope.
        """

        symbol_table = SymbolTable()

        self.setSymbolTable(symbol_table)

        for tln in self.children:
            if isinstance(tln, SymbolDecl):
                tln.addToSymbolTable(symbol_table)
            elif isinstance(tln, IncludeNode):
                tln.addToSymbolTable(symbol_table)
            elif isinstance(tln, FuncDef):
                tln.addToSymbolTable(symbol_table) # does nothing wrt the function symbol table
                tln.addFunctionScopeToSymbolTable(symbol_table) # sets function body's table
        # ENDFOR

        return symbol_table

    def toDot(self, parent_nr=None, begin_nr=1, add_open_close=False):
        return self.M_defaultToDotImpl(children=self.children,
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class TopLevelNode(ASTNode):
    """
        Base class for nodes that appear directly underneath the program node.
    """

    def __init__(self, node_name):
        super().__init__(node_name=node_name)


class IncludeNode(TopLevelNode):
    """
        Node that represents "#include <stdio.h>"
    """

    def __init__(self):
        super().__init__(node_name="Include <stdio.h>")

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)

    def addToSymbolTable(self, symbol_table):
        self.setSymbolTable(symbol_table)
        symbol_table.insert("printf", 'void()')
        symbol_table.insert("scanf", 'void()')


class SymbolDecl(TopLevelNode):
    """
        Base class for variable declaration nodes.
    """

    def __init__(self, symbol_class: str, symbol_type: str, symbol_id: str, symbol_ptr_cnt: int):
        """
        Params:
            'symbol_class': Whether the symbol is an array, variable, function, etc.
            'symbol_type': A string that contains the name of the type of the symbol.
            'symbol_id': String that represents the name of the symbol.
            'symbol_ptr_count': Integer that denotes the amount of pointer levels. Can be set to zero if the symbol is not a pointer.
        """
        # string that represents the node in dot-format.
        full_node_name = "Decl:{}\\nId:{}\\nPtrCount:{}\\nType:{}".format(symbol_class, symbol_id, symbol_ptr_cnt,
                                                                          symbol_type)
        super().__init__(node_name=full_node_name)
        self.symbol_type = symbol_type
        self.symbol_id = symbol_id
        self.symbol_ptr_cnt = symbol_ptr_cnt

    def getType(self):
        """
           Retrieve a string that contains the name of the type of the symbol. 
        """
        return self.symbol_type

    def getID(self):
        """
            Retrieve a string that contains the name of the identifier.
        """
        return self.symbol_id

    def getPointerCount(self):
        """
            Retrieve the number of pointer levels the identifier of the symbol has.
        """
        return self.symbol_ptr_cnt

    def addToSymbolTable(self, symbol_table):
        """
            Add the declared symbol to the specified symbol table.
        """

        raise NotImplementedError()


class ArrayDecl(SymbolDecl):
    """
        Node that represents an array declaration: "type id[size_expr];"
    """

    def __init__(self, array_type: str, array_id: str, ptr_count: int, size_expr):
        super().__init__(symbol_class="Array",
                         symbol_type=array_type,
                         symbol_id=array_id,
                         symbol_ptr_cnt=ptr_count)
        self.size_expr = size_expr

    def getSizeExp(self):
        return self.size_expr

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.size_expr],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)

    def addToSymbolTable(self, symbol_table):
        self.setSymbolTable(symbol_table)
        self.size_expr.setExprTreeSymbolTable(symbol_table)
        symbol_table.insert(self.symbol_id, "{}{}[]".format(self.symbol_type, "*" * self.symbol_ptr_cnt))


class VarDeclDefault(SymbolDecl):
    """
        Node that represents a variable declaration without initializer: "type id;"
    """

    def __init__(self, var_type: str, var_id: str, ptr_count: int):
        super().__init__(symbol_class="VarDefault",
                         symbol_type=var_type,
                         symbol_id=var_id,
                         symbol_ptr_cnt=ptr_count)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)

    def addToSymbolTable(self, symbol_table):
        self.setSymbolTable(symbol_table)
        symbol_table.insert(self.symbol_id, "{}{}".format(self.symbol_type, "*" * self.symbol_ptr_cnt))


class VarDeclWithInit(SymbolDecl):
    """
        Node that represents a variabele declaration with initializer: "type id = init_expr;"
    """

    def __init__(self, var_type: str, var_id: str, ptr_count: int, init_expr):
        super().__init__(symbol_class="VarWithInit",
                         symbol_type=var_type,
                         symbol_id=var_id,
                         symbol_ptr_cnt=ptr_count)
        self.init_expr = init_expr

    def getInitExpr(self):
        return self.init_expr

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.init_expr],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)

    def addToSymbolTable(self, symbol_table):
        self.setSymbolTable(symbol_table)
        self.init_expr.setExprTreeSymbolTable(symbol_table)
        symbol_table.insert(self.symbol_id, "{}{}".format(self.symbol_type, "*" * self.symbol_ptr_cnt))


class FuncDecl(SymbolDecl):
    """
        Node that represents a function declaration: "type func(type param);"
    """

    def __init__(self, return_type: str, func_id: str, ptr_count: int, param_list):
        super().__init__(symbol_class="FuncDecl",
                         symbol_type=return_type,
                         symbol_id=func_id,
                         symbol_ptr_cnt=ptr_count)
        self.param_list = param_list

    def getParams(self):
        return self.param_list

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[*self.param_list],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)

    def addToSymbolTable(self, symbol_table):
        self.setSymbolTable(symbol_table)
        symbol_table.insert(self.symbol_id, "{}({})".format(self.symbol_type, [param.getParamType() for param in self.param_list]))


class FuncDef(TopLevelNode):
    """
    Node that represents a function definition: "type func(param) { <statements> }"
    """

    def __init__(self, return_type: str, func_id: str, ptr_count: int, param_list: list, body):
        super().__init__(node_name="FuncDef\\n'" + func_id + "'\\nType:'" + return_type + "'")
        self.return_type = return_type
        self.func_id = func_id
        self.ptr_count = ptr_count
        self.param_list = param_list
        self.body = body

    def getReturnType(self):
        return self.return_type

    def getFuncID(self):
        return self.func_id

    def getPointerCount(self):
        return self.ptr_count

    def getParamList(self):
        return self.param_list

    def getBody(self):
        return self.body

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[*self.param_list, self.body],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)

    def addToSymbolTable(self, symbol_table):
        """
            Add the signature of the function to the specified symbol table.
        """
        symbol_table.insert(self.func_id, "{}({})".format(self.return_type, [param.getParamType() for param in self.param_list]))

    def addFunctionScopeToSymbolTable(self, parent_table):
        """
            Create a new symbol table from the function scope, and add it as a child to the specified symbol table.
        """

        # instantiate child table
        symbol_table = parent_table.allocate()

        self.setSymbolTable(symbol_table)

        for param in self.param_list:
            param.addToSymbolTable(symbol_table)

        # add the body to the existing symbol table
        self.body.addScopeToSymbolTable(parent_table=symbol_table, as_child=False)

        return symbol_table


class StatementContainer:
    """
        Base class for nodes that contains statements or declarations.
    """

    def __init__(self, child_list):
        self.child_list = child_list

    def getChildren(self):
        return self.child_list

    def isEmpty(self):
        return len(self.child_list) == 0

    def addScopeToSymbolTable(self, parent_table, as_child):
        """
            Add the symbols declared in this statement container to the specified symbol table.

            Param:
                'parent_table': The table that is the parent of this scope, or the statements in this scope.
                'as_child': Whether or not the symbols should be added as a child table.
        """

        if as_child:
            symbol_table = parent_table.allocate()
        else:
            symbol_table = parent_table

        # TODO check if this is possible
        self.setSymbolTable(symbol_table)

        for child in self.child_list:
            # each child is declaration or statement
            # important statements;
            #   if: own scope
            #   for: own scope
            #   while: own scope
            #   compound statements
            # each declaration introduces a symbol.

            if isinstance(child, SymbolDecl):  # a symbol can simply be added
                # note: this also sets the symbol table for the declaration
                child.addToSymbolTable(symbol_table)

            elif isinstance(child, BranchStmt):  # if statement: has its own scope
                # retrieve if, else body

                child.addToSymbolTable(symbol_table)

                if_body = child.getIfBody()
                else_body = child.getElseBody()

                # add if body
                # note: this also sets the symbol table for the body
                if_body.addScopeToSymbolTable(parent_table=symbol_table, as_child=True)

                # add else body if it is not empty.
                # note: this also sets the symbol table for the body
                if not else_body.isEmpty():
                    else_body.addScopeToSymbolTable(parent_table=symbol_table, as_child=True)

            elif isinstance(child, ForStmt):  # for statement: has its own scope
                # retrieve condition init_expr
                # retrieve body
                # merge these and add as child

                # filter out expression
                init_decl_list = [decl for decl in child.getInitList() if isinstance(decl, SymbolDecl)]
                body = child.getBody()

                # allocate new scope
                for_scope = symbol_table.allocate()

                # merge body and declarators
                for decl in init_decl_list:
                    # only declarations
                    decl.addToSymbolTable(for_scope)
                # note: this also sets the symbol table for the body
                body.addScopeToSymbolTable(parent_table=for_scope, as_child=False)

                # if we retrieve the symbol table
                # it will be the one with the children of the for body, and de declarations
                child.setSymbolTable(for_scope)

            elif isinstance(child, WhileStmt):  # while statement: has its own scope
                # retrieve body and add as child.
                body = child.getBody()
                # note: this also sets the symbol table for the body
                tbl = body.addScopeToSymbolTable(parent_table=symbol_table, as_child=True)

                # if we retrieve the symbol table
                # it will be the one with the children of the while body.
                child.setSymbolTable(tbl)

            elif isinstance(child, CompoundStmt):  # compound statement: has its own scope
                # add contents as child
                # note: this also sets the symbol table for the body
                child.addScopeToSymbolTable(parent_table=symbol_table, as_child=True)

            elif isinstance(child, ExpressionStatement): # expression statement: annotate the expression tree with the symbol table
                child.getExpression().setExprTreeSymbolTable(symbol_table)


        return symbol_table


class Body(ASTNode, StatementContainer):
    """
        Node that represents the body of statement (e.g. forloop, whileloop, etc). This is simply a list of statements.
    """

    def __init__(self, child_list):
        ASTNode.__init__(self, node_name="Body")
        StatementContainer.__init__(self, child_list=child_list)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=self.child_list,
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class FuncParam(ASTNode):
    """
        Node that represents a function param: "type id_with_ptr".
    """

    def __init__(self, param_type: str, param_id: str, ptr_count: int):
        super().__init__(node_name="FuncParam\\nId: '" + param_id + "'\\nPtrCount:" + str(
            ptr_count) + "\\nType:'" + param_type + "'")
        self.param_type = param_type
        self.param_id = param_id
        self.ptr_count = ptr_count

    def getParamType(self):
        return self.param_type

    def getParamID(self):
        return self.param_id

    def getPointerCount(self):
        return self.ptr_count

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)

    def addToSymbolTable(self, symbol_table):
        """
            A function param introduces an identifier into the function's own scope.
        """
        self.setSymbolTable(symbol_table)
        symbol_table.insert(self.param_id, "{}{}".format(self.param_type, "*" * self.ptr_count))


class Statement(ASTNode):
    """
        Base class for statements nodes.
    """

    def __init__(self, statement_type):
        super().__init__(node_name="Stmt:" + statement_type)


class CompoundStmt(Statement, StatementContainer):
    """
    Node that represents a compound statement: "{ <statements> }".
    """

    def __init__(self, child_list):
        Statement.__init__(self, statement_type="CompoundStmt")
        StatementContainer.__init__(self, child_list=child_list)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=self.child_list,
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class WhileStmt(Statement):
    """
        Node that represents a while loop.
    """

    def __init__(self, condition_expr, body):
        super().__init__(statement_type="WhileStmt")
        self.cond_expr = condition_expr
        self.body = body

    def getCondExpr(self):
        return self.cond_expr

    def getBody(self):
        return self.body

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.cond_expr, self.body],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class ForStmt(Statement):
    """
        Node that represents a for loop.
    """

    def __init__(self, init_list, condition_expr, iter_list, body):
        """
            'init_list': a list of declarations, or expressions.
            'condition_expr': an expression that will be evaluated to determine whether or not to 
            continue iterating, or None.
            'iter_list': a list of expressions that will be performed at the end of each iteration.
        """
        super().__init__(statement_type="ForStmt")
        self.init_list = init_list
        self.cond_expr = condition_expr
        self.iter_list = iter_list
        self.body = body

    def getInitList(self):
        return self.init_list

    def getCondExpr(self):
        return self.cond_expr

    def getIterList(self):
        return self.iter_list

    def getBody(self):
        return self.body

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[*self.init_list, self.cond_expr, *self.iter_list, self.body],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class BranchStmt(Statement):
    """
        Node that represents an if statement.
    """

    def __init__(self, condition_expr, if_body, else_body):
        super().__init__(statement_type="BranchStmt")
        self.cond_expr = condition_expr
        self.if_body = if_body
        self.else_body = else_body

    def getCondExpr(self):
        return self.cond_expr

    def getIfBody(self):
        return self.if_body

    def getElseBody(self):
        return self.else_body

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.cond_expr, self.if_body, self.else_body],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class JumpStatement(Statement):
    """
        Base class for jump statements.
    """

    def __init__(self, jump_type):
        super().__init__(statement_type="JumpStmt:" + jump_type)


class ReturnStatement(JumpStatement):
    """
        Node that represents a return statement without return value.
    """

    def __init__(self):
        super().__init__(jump_type="return")

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class ReturnWithExprStatement(JumpStatement):
    """
        Node that represents a return statement with return value.
    """

    def __init__(self, expression):
        super().__init__(jump_type="returnWithExpr")
        self.expression = expression

    def getExpression(self):
        return self.expression

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.expression],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class BreakStatement(JumpStatement):
    """
        Node that represents a break statement.
    """

    def __init__(self):
        super().__init__(jump_type="break")

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class ContinueStatement(JumpStatement):
    """
        Node that represents a continue statement.
    """

    def __init__(self):
        super().__init__(jump_type="continue")

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class ExpressionStatement(Statement):
    """
        Node that represents an expression statement.
        An expression statement contains exactly one expression.
    """

    def __init__(self, expression):
        super().__init__(statement_type="ExpressionStatement")
        self.expression = expression

    def getExpression(self):
        return self.expression

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.expression],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class Expression(ASTNode):
    """
        Base class for all expression nodes.
    """

    def __init__(self, expression_type):
        super().__init__(node_name=expression_type)

    def setExprTreeSymbolTable(self, symbol_table):
    	"""
			Sets the symbol table for all in the expression tree with this expression as root.
    	"""
    	pass

    def checkIdentifierExistance(self, symbol_table):
        """
            Determine whether or not all identifier used in the expression are present in
            the specified symbol table.
        """

        # TODO implement
        pass


class AssignmentExpr(Expression):
    """
        Node that represents a normal assignment expression.
    """

    def __init__(self, left, right):
        super().__init__(expression_type="AssignmentExpr")
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.left.setExprTreeSymbolTable(symbol_table)
    	self.right.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class AddAssignmentExpr(Expression):
    """
        Node that represents an addition assignment expression: "a += b;".
    """

    def __init__(self, left, right):
        super().__init__(expression_type="AddAssign")
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.left.setExprTreeSymbolTable(symbol_table)
    	self.right.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class SubAssignmentExpr(Expression):
    """
        Node that represents a subtraction assignment expression: "a -= b;".
    """

    def __init__(self, left, right):
        super().__init__(expression_type="SubAssign")
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.left.setExprTreeSymbolTable(symbol_table)
    	self.right.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class MulAssignmentExpr(Expression):
    """
        Node that represents a multiplication assignment expression: "a *= b;".
    """

    def __init__(self, left, right):
        super().__init__(expression_type="MulAssign")
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.left.setExprTreeSymbolTable(symbol_table)
    	self.right.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class DivAssignmentExpr(Expression):
    """
        Node that represents a division assignment expression: "a /= b;".
    """

    def __init__(self, left, right):
        super().__init__(expression_type="DivAssign")
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.left.setExprTreeSymbolTable(symbol_table)
    	self.right.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class LogicOrExpr(Expression):
    """
        Node that represents an OR expression.
    """

    def __init__(self, left, right):
        super().__init__(expression_type="LogicOrExpr")
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.left.setExprTreeSymbolTable(symbol_table)
    	self.right.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class LogicAndExpr(Expression):
    """
        Node that represents an AND expression.
    """

    def __init__(self, left, right):
        super().__init__(expression_type="LogicAndExpr")
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.left.setExprTreeSymbolTable(symbol_table)
    	self.right.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class EqualityExpr(Expression):
    """
        Node that represents an equality expression.
    """

    def __init__(self, left, right):
        super().__init__(expression_type="EqualityExpr")
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.left.setExprTreeSymbolTable(symbol_table)
    	self.right.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class InequalityExpr(Expression):
    """
        Node that represents an inequality expression.
    """

    def __init__(self, left, right):
        super().__init__(expression_type="InequalityExpr")
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.left.setExprTreeSymbolTable(symbol_table)
    	self.right.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class CompGreater(Expression):
    """
        Node that represents a greater-than comparison expression: "a > b".
    """

    def __init__(self, left, right):
        super().__init__(expression_type="CompGreater")
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.left.setExprTreeSymbolTable(symbol_table)
    	self.right.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class CompLess(Expression):
    """
        Node that represents a less-than comparison expression: "a < b".
    """

    def __init__(self, left, right):
        super().__init__(expression_type="CompLess")
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.left.setExprTreeSymbolTable(symbol_table)
    	self.right.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class CompGreaterEqual(Expression):
    """
        Node that represents a greater-than-or-equal comparison expression: "a >= b".
    """

    def __init__(self, left, right):
        super().__init__(expression_type="CompGreaterEqual")
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.left.setExprTreeSymbolTable(symbol_table)
    	self.right.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class CompLessEqual(Expression):
    """
        Node that represents a less-than-or-equal comparison expression: "a <= b".
    """

    def __init__(self, left, right):
        super().__init__(expression_type="CompLessEqual")
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.left.setExprTreeSymbolTable(symbol_table)
    	self.right.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class AddExpr(Expression):
    """
        Node that represents an addition expression.
    """

    def __init__(self, left, right):
        super().__init__(expression_type="AddExpr")
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.left.setExprTreeSymbolTable(symbol_table)
    	self.right.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class SubExpr(Expression):
    """
        Node that represents an subtraction expression.
    """

    def __init__(self, left, right):
        super().__init__(expression_type="SubExpr")
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.left.setExprTreeSymbolTable(symbol_table)
    	self.right.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class MulExpr(Expression):
    """
        Node that represents a multiplication expression: "a * b".
    """

    def __init__(self, left, right):
        super().__init__(expression_type="MulExpr")
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.left.setExprTreeSymbolTable(symbol_table)
    	self.right.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class DivExpr(Expression):
    """
        Node that represents a division expression: "a / b".
    """

    def __init__(self, left, right):
        super().__init__(expression_type="ModExpr")
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.left.setExprTreeSymbolTable(symbol_table)
    	self.right.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class ModExpr(Expression):
    """
        Node that represents a modulo expression: "a % b".
    """

    def __init__(self, left, right):
        super().__init__(expression_type="ModExpr")
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.left.setExprTreeSymbolTable(symbol_table)
    	self.right.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class CastExpr(Expression):
    """
        Node that represents a cast expression.
    """

    def __init__(self, type_list, expression):
        """
        Params:
            'type_list': list of str.
            'expression': The Expression that is cast to the specified types.
        """
        super().__init__(expression_type="CastExpr\\nTypes:{}".format(type_list))
        self.type_list = type_list
        self.expression = expression

    def getTypeList(self):
        return self.type_list

    def getExpr(self):
        return self.expression

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.expression.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.expression],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class LogicNotExpr(Expression):
    """
        Node that represents a logical NOT expression.
    """

    def __init__(self, expression):
        super().__init__(expression_type="LogicNotExpr")
        self.expression = expression

    def getExpr(self):
        return self.expression

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.expression.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.expression],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class PrefixIncExpr(Expression):
    """
        Node that represents "++x".
    """

    def __init__(self, expression):
        super().__init__(expression_type="PrefixIncExpr")
        self.expression = expression

    def getExpr(self):
        return self.expression

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.expression.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.expression],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class PrefixDecExpr(Expression):
    """
        Node that represents "--x".
    """

    def __init__(self, expression):
        super().__init__(expression_type="PrefixDecExpr")
        self.expression = expression

    def getExpr(self):
        return self.expression

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.expression.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.expression],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class PostfixIncExpr(Expression):
    """
        Node that represents "x++".
    """

    def __init__(self, expression):
        super().__init__(expression_type="PostfixIncExpr")
        self.expression = expression

    def getExpr(self):
        return self.expression

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.expression.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.expression],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class PostfixDecExpr(Expression):
    """
        Node that represents "x--".
    """

    def __init__(self, expression):
        super().__init__(expression_type="PostfixDecExpr")
        self.expression = expression

    def getExpr(self):
        return self.expression

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.expression.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.expression],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class PlusPrefixExpr(Expression):
    """
        Node that represents a plus prefix expression: "+x".
    """

    def __init__(self, expression):
        super().__init__(expression_type="PlusPrefixExpr")
        self.expression = expression

    def getExpr(self):
        return self.expression

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.expression.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.expression],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class MinPrefixExpr(Expression):
    """
        Node that represents a minus prefix expression: "-x".
    """

    def __init__(self, expression):
        super().__init__(expression_type="MinPrefixExpr")
        self.expression = expression

    def getExpr(self):
        return self.expression

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.expression.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.expression],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class ArrayAccessExpr(Expression):
    """
        Node that represent an array access expression: "target_array[index_expr]".
    """

    def __init__(self, target_array, index_expr):
        super().__init__(expression_type="ArrayAccessExpr")
        self.target_array = target_array
        self.index_expr = index_expr

    def getTargetArray(self):
        return self.target_array

    def getIndexArray(self):
        return self.index_expr

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.target_array.setExprTreeSymbolTable(symbol_table)
    	self.index_expr.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.target_array, self.index_expr],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class PointerDerefExpr(Expression):
    """
        Node that represents a pointer dereference expression: "*target_ptr".
    """

    def __init__(self, target_ptr):
        super().__init__(expression_type="PointerDerefExpr")
        self.target_ptr = target_ptr

    def getTargetPtr(self):
        return self.target_ptr

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.target_ptr.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.target_ptr],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class AddressExpr(Expression):
    """
        Node that represents an address expression: "&x".
    """

    def __init__(self, target_expr):
        super().__init__(expression_type="AddressExpr")
        self.target_expr = target_expr

    def getTargetExpr(self):
        return self.target_expr

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.target_expr.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.target_expr],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class FuncCallExpr(Expression):
    """
        Node that represents a function call: "identifier(params)".
    """

    def __init__(self, function_identifier, argument_list):
        """
        Params:
            'function_identifier': IdentifierExpr object that represents the identifier of the function.
            'argument_list': list of Expression
        """
        super().__init__(expression_type="FuncCallExpr")
        self.identifier = function_identifier
        self.argument_list = argument_list

    def getFunctionID(self):
        return self.identifier

    def getArguments(self):
        return self.argument_list

    def setExprTreeSymbolTable(self, symbol_table):
    	self.setSymbolTable(symbol_table)

    	self.identifier.setExprTreeSymbolTable(symbol_table)

    	for arg in self.argument_list:
    		arg.setExprTreeSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.identifier, *self.argument_list],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class IdentifierExpr(Expression):
    """
        Node that represents an identifier expression (different from the idenfier itself!)
    """

    def __init__(self, identifier: str):
        super().__init__(expression_type="IdentifierExpr\\n'" + identifier + "'")
        self.identifier = identifier

    def getIdentifier(self):
        return self.identifier

    def setExprTreeSymbolTable(self, symbol_table):
        self.setSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class ConstantExpr(Expression):
    """
        Base class for constant expressions.
    """

    def __init__(self, constant_expr_type, value):
        """
            Constructor.

            Params:
                value: the value of the constant. These are not Expression objects.
        """
        super().__init__(expression_type=constant_expr_type + "\\n'" + str(value) + "'")
        self.value = value

    def getValue(self):
        return self.value

    def setExprTreeSymbolTable(self, symbol_table):
        self.setSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class IntegerConstantExpr(ConstantExpr):
    """
        Node that represents integer constants: "0123456789".
    """

    def __init__(self, integer_value):
        super().__init__(constant_expr_type="IntConstant", value=integer_value)

    def getIntValue(self):
        return int(self.getValue())


class FloatConstantExpr(ConstantExpr):
    """
        Node that represents float constants: "012345.6789".
    """

    def __init__(self, float_value):
        super().__init__(constant_expr_type="FloatConstant", value=float_value)

    def getFloatValue(self):
        return float(self.getValue())


class StringConstantExpr(ConstantExpr):
    """
        Node that represents string constants: "abcdef".
    """

    def __init__(self, str_value):
        super().__init__(constant_expr_type="StrConstant", value=str_value)

    def getStrValue(self):
        return str(self.getValue())


class CharConstantExpr(ConstantExpr):
    """
        Node that represents character constants: 'a', 'b', 'abc'.
    """

    def __init__(self, char_value):
        super().__init__(constant_expr_type="CharConstant", value=char_value)

    def getCharValue(self):
        return str(self.getValue())


class BoolConstantExpr(ConstantExpr):
    """
        Node that represents boolean constants: 'true', 'false'.
    """

    def __init__(self, bool_value):
        super().__init__(constant_expr_type="BoolConstant", value=bool_value)

    def getBoolValue(self):
        return str(self.getValue()).lower() == "true"