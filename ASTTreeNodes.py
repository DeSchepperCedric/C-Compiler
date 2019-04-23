from SymbolTable import SymbolTable
from SymbolTable import SymbolType
from SymbolTable import FunctionType
from SymbolTable import ArrayType
from SymbolTable import VariableType
from Logger import Logger

from CompilerException import *

class ASTNode:
    """
        Base class for all nodes in AST Trees.
    """

    def __init__(self, node_name):
        self.node_name    = node_name
        self.symbol_table = None
        self.line_nr      = None
        self.col_nr       = None

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

    def getLineNr(self):
        """ 
            Retrieve the line number of the AST node w.r.t. the original C source file.
        """
        return self.line_nr

    def setLineNr(self, line_nr):
        self.line_nr = line_nr
        return self # return self so we can chain these operations

    def getColNr(self):
        """ 
            Retrieve the column number of the AST node w.r.t. the original C source file.
        """
        return self.col_nr

    def setColNr(self, col_nr):
        self.col_nr = col_nr
        return self # return self so we can chain these operations

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
            Type checking will also be performed at this stage.
            Each expression node will be annotated with a type. Can be retrieved with getExpressionType()
            Each statement will have a symbol table if relevant. Can be retrieved with getSymbolTable()
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
        symbol_table.insert("printf", FunctionType('void', []))
        symbol_table.insert("scanf",  FunctionType('void', []))


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
        full_node_name = "Decl:{}\\nId:{}\\nPtrCount:{}\\nType:{}".format(symbol_class, symbol_id, symbol_ptr_cnt, symbol_type)
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



        symbol_table.insert(self.symbol_id, ArrayType(type_to_string(self.symbol_type, self.symbol_ptr_cnt)))


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
        symbol_table.insert(self.symbol_id, VariableType(type_to_string(self.symbol_type, self.symbol_ptr_cnt)))


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
        symbol_table.insert(self.symbol_id, VariableType(type_to_string(self.symbol_type, self.symbol_ptr_cnt)))


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

        symbol_table.insert(self.symbol_id, FunctionType(self.symbol_type, [type_to_string(param.getParamType(), param.getPointerCount()) for param in self.param_list]))


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
        symbol_table.insert(self.func_id, FunctionType(self.return_type, [type_to_string(param.getParamType(), param.getPointerCount()) for param in self.param_list]))

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

                if_body = child.getIfBody()
                else_body = child.getElseBody()

                # add if body
                # note: this also sets the symbol table for the body
                if_body.addScopeToSymbolTable(parent_table=symbol_table, as_child=True)

                # add else body if it is not empty.
                # note: this also sets the symbol table for the body
                if not else_body.isEmpty():
                    else_body.addScopeToSymbolTable(parent_table=symbol_table, as_child=True)

            elif isinstance(child, ForStmt):  
                # for statement: has its own scope

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

            elif isinstance(child, WhileStmt):  
                # while statement: has its own scope
                # retrieve body and add as child.
                body = child.getBody()
                # note: this also sets the symbol table for the body
                tbl = body.addScopeToSymbolTable(parent_table=symbol_table, as_child=True)

                # if we retrieve the symbol table
                # it will be the one with the children of the while body.
                child.setSymbolTable(tbl)

            elif isinstance(child, CompoundStmt):  
                # compound statement: has its own scope
                # add contents as child
                # note: this also sets the symbol table for the body
                child.addScopeToSymbolTable(parent_table=symbol_table, as_child=True)

            elif isinstance(child, ExpressionStatement): 
                # expression statement: annotate the expression tree with the symbol table and type information
                child.getExpression().setExprTreeSymbolTable(symbol_table)
                child.getExpression().resolveExpressionType(symbol_table)

            elif isinstance(child, VarDeclWithInit):
                child.getInitExpr().setExprTreeSymbolTable(symbol_table) # annotate with symbol table
                child.getInitExpr().resolveExpressionType(symbol_table)  # resolve expr type

                # check if compatible is_conversion_possible
                # check for narrowing will_conversion_narrow
                # TODO
            elif isinstance(child, ReturnWithExprStatement):
                child.getExpression().setExprTreeSymbolTable(symbol_table) # annotate with symbol table
                child.getExpression().resolveExpressionType(symbol_table)  # resolve expr type

                # check return type for compatibility and narrowing
                # TODO





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

        symbol_table.insert(self.param_id, VariableType(type_to_string(self.param_type, self.ptr_count)))


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
        self.expression_type = None

    def setExprTreeSymbolTable(self, symbol_table):
        """
            Sets the symbol table for all in the expression tree with this expression as root.
        """
        pass

    def resolveExpressionType(self, symbol_table):
        """
            This will assign types to the expression nodes in the expression tree.
            If an identifier is encountered, it's type will be extracted from the specified
            symbol table.

            Return value: None

            !! Use getExpressionType() to retrieve the resolved type. !!
        """
        pass

    def getExpressionType(self):
        """
            Retrieve the type of the expression.

            Returns a string with the name of the type

            !! First use resolveExpressionType() to calculate the type. !!
        """
        return self.expression_type

# TODO check left expression: must be deref, array access, non-function variable, 
# TODO check if left and right expression types are compatible
# TODO narrowing warnings
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

    def resolveExpressionType(self, symbol_table):
        # left type does not matter, since assignments are possible on all types
        # right value conforms to the same constraints as division operators

        left_type = self.left.resolveExpressionType(symbol_table)
        right_type = self.right.resolveExpressionType(symbol_table)

        # and assignment is not possible
        if not is_conversion_possible(left_type, right_type):
            Logger.error("Assignment of expression of type '{}' to target of incompatible type '{}' is not possible on line {}."
                                .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            raise AstTypingException()

        # check for narrowing
        if will_conversion_narrow(left_type, right_type):
            Logger.warning("Assignment of expression of type '{}' to target of type '{}' will result in narrowing on line {}."
                                .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            # no exception here, compilation may continue.

        # lhs = rhs, lhs is returned, so we take the type of lhs
        return left_type

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

    def resolveExpressionType(self, symbol_table):
        # left type does not matter, since assignments are possible on all types
        # right value conforms to the same constraints as division operators

        left_type = self.left.resolveExpressionType(symbol_table)
        right_type = self.right.resolveExpressionType(symbol_table)

        if not is_non_ptr_variable_type(left_type) or not is_non_ptr_variable_type(right_type):
            Logger.error("Pointers, arrays and functions cannot be used as operators for addition. Tried to use types '{}' and '{}' on line {}."
                            .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            raise AstTypingException()

        # assignment is possible since left and right type are both non-pointer variable types. The only possible
        # complication is 'float' and integer type, but those too can be converted.

        # check for narrowing
        if will_conversion_narrow(left_type, right_type):
            Logger.warning("Assignment of expression of type '{}' to target of type '{}' will result in narrowing on line {}."
                                .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            # no exception here, compilation may continue.

        # lhs = rhs, lhs is returned, so we take the type of lhs
        return left_type

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

    def resolveExpressionType(self, symbol_table):
        # left type does not matter, since assignments are possible on all types
        # right value conforms to the same constraints as division operators

        left_type = self.left.resolveExpressionType(symbol_table)
        right_type = self.right.resolveExpressionType(symbol_table)

        if not is_non_ptr_variable_type(left_type) or not is_non_ptr_variable_type(right_type):
            Logger.error("Pointers, arrays and functions cannot be used as operators for subtraction. Tried to use types '{}' and '{}' on line {}."
                            .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            raise AstTypingException()

        # assignment is possible since left and right type are both non-pointer variable types. The only possible
        # complication is 'float' and integer type, but those too can be converted.

        # check for narrowing
        if will_conversion_narrow(left_type, right_type):
            Logger.warning("Assignment of expression of type '{}' to target of type '{}' will result in narrowing on line {}."
                                .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            # no exception here, compilation may continue.

        # lhs = rhs, lhs is returned, so we take the type of lhs
        return left_type

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

    def resolveExpressionType(self, symbol_table):
        # left type does not matter, since assignments are possible on all types
        # right value conforms to the same constraints as division operators

        left_type = self.left.resolveExpressionType(symbol_table)
        right_type = self.right.resolveExpressionType(symbol_table)

        if not is_non_ptr_variable_type(left_type) or not is_non_ptr_variable_type(right_type):
            Logger.error("Only pointers, arrays and functions cannot be used as operators for multiplication. Tried to use types '{}' and '{}' on line {}."
                            .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            raise AstTypingException()

        # assignment is possible since left and right type are both non-pointer variable types. The only possible
        # complication is 'float' and integer type, but those too can be converted.

        # check for narrowing
        if will_conversion_narrow(left_type, right_type):
            Logger.warning("Assignment of expression of type '{}' to target of type '{}' will result in narrowing on line {}."
                                .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            # no exception here, compilation may continue.

        # lhs = rhs, lhs is returned, so we take the type of lhs
        return left_type

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)

# left = array access, 
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

    def resolveExpressionType(self, symbol_table):
        # left type does not matter, since assignments are possible on all types
        # right value conforms to the same constraints as division operators

        left_type = self.left.resolveExpressionType(symbol_table)
        right_type = self.right.resolveExpressionType(symbol_table)

        if not is_non_ptr_variable_type(left_type) or not is_non_ptr_variable_type(right_type):
            Logger.error("Pointers, arrays and functions cannot be used as operators for division. Tried to use types '{}' and '{}' on line {}."
                            .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            raise AstTypingException()

        # assignment is possible since left and right type are both non-pointer variable types. The only possible
        # complication is 'float' and integer type, but those too can be converted.

        # check for narrowing
        if will_conversion_narrow(left_type, right_type):
            Logger.warning("Assignment of expression of type '{}' to target of type '{}' will result in narrowing on line {}."
                                .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            # no exception here, compilation may continue.

        # lhs = rhs, lhs is returned, so we take the type of lhs
        return left_type

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

    def resolveExpressionType(self, symbol_table):
        # pointer types, arrays, value types are all allowed so that 0 is false, anything else is true.

        left_type = self.left.resolveExpressionType(symbol_table)
        right_type = self.right.resolveExpressionType(symbol_table)

        if left_type.isFunction() or right_type.isFunction():

            Logger.error("Functions cannot be used in logical expressions. Tried to use types '{}' and '{}' on line {}."
                            .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            raise AstTypingException()

        # return bool
        self.expression_type = VariableType('bool')

        return self.expression_type

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

    def resolveExpressionType(self, symbol_table):
        # pointer types, arrays, value types are all allowed so that 0 is false, anything else is true.

        left_type = self.left.resolveExpressionType(symbol_table)
        right_type = self.right.resolveExpressionType(symbol_table)

        if left_type.isFunction() or right_type.isFunction():

            Logger.error("Functions cannot be used in logical expressions. Tried to use types '{}' and '{}' on line {}."
                            .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            raise AstTypingException()

        # return bool
        self.expression_type = VariableType('bool')

        return self.expression_type

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

    def resolveExpressionType(self, symbol_table):

        left_type = self.left.resolveExpressionType(symbol_table)
        right_type = self.right.resolveExpressionType(symbol_table)

        # variables, arrays and pointers are allowed
        if left_type.isFunction() or right_type.isFunction():
            Logger.error("Functions cannot be used as operators for comparisons. Tried to use types '{}' and '{}' on line {}."
                            .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            raise AstTypingException()

        # return bool
        self.expression_type = VariableType('bool')

        return self.expression_type

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

    def resolveExpressionType(self, symbol_table):

        left_type = self.left.resolveExpressionType(symbol_table)
        right_type = self.right.resolveExpressionType(symbol_table)

        # variables, arrays and pointers are allowed
        if left_type.isFunction() or right_type.isFunction():
            Logger.error("Functions cannot be used as operators for comparisons. Tried to use types '{}' and '{}' on line {}."
                            .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            raise AstTypingException()

        # return bool
        self.expression_type = VariableType('bool')

        return self.expression_type

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

    def resolveExpressionType(self, symbol_table):

        left_type = self.left.resolveExpressionType(symbol_table)
        right_type = self.right.resolveExpressionType(symbol_table)

        # variables, arrays and pointers are allowed
        if left_type.isFunction() or right_type.isFunction():
            Logger.error("Functions cannot be used as operators for comparisons. Tried to use types '{}' and '{}' on line {}."
                            .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            raise AstTypingException()

        # return bool
        self.expression_type = VariableType('bool')

        return self.expression_type

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

    def resolveExpressionType(self, symbol_table):

        left_type = self.left.resolveExpressionType(symbol_table)
        right_type = self.right.resolveExpressionType(symbol_table)

        # variables, arrays and pointers are allowed
        if left_type.isFunction() or right_type.isFunction():
            Logger.error("Functions cannot be used as operators for comparisons. Tried to use types '{}' and '{}' on line {}."
                            .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            raise AstTypingException()

        # return bool
        self.expression_type = VariableType('bool')

        return self.expression_type

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

    def resolveExpressionType(self, symbol_table):

        left_type = self.left.resolveExpressionType(symbol_table)
        right_type = self.right.resolveExpressionType(symbol_table)

        # variables, arrays and pointers are allowed
        if left_type.isFunction() or right_type.isFunction():
            Logger.error("Functions cannot be used as operators for comparisons. Tried to use types '{}' and '{}' on line {}."
                            .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            raise AstTypingException()

        # return bool
        self.expression_type = VariableType('bool')

        return self.expression_type

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

    def resolveExpressionType(self, symbol_table):

        left_type = self.left.resolveExpressionType(symbol_table)
        right_type = self.right.resolveExpressionType(symbol_table)

        # variables, arrays and pointers are allowed
        if left_type.isFunction() or right_type.isFunction():
            Logger.error("Functions cannot be used as operators for comparisons. Tried to use types '{}' and '{}' on line {}."
                            .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            raise AstTypingException()

        # return bool
        self.expression_type = VariableType('bool')

        return self.expression_type

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

    def resolveExpressionType(self, symbol_table):
        # only "values" are allowed

        left_type = self.left.resolveExpressionType(symbol_table)
        right_type = self.right.resolveExpressionType(symbol_table)

        if not is_non_ptr_variable_type(left_type) or not is_non_ptr_variable_type(right_type):
            Logger.error("Pointers, arrays and functions cannot be used as operators for addition. Tried to use types '{}' and '{}' on line {}."
                            .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            raise AstTypingException()

        self.expression_type = get_maximal_type(left_type, right_type)

        return self.expression_type

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

    def resolveExpressionType(self, symbol_table):
        # only "values" are allowed

        left_type = self.left.resolveExpressionType(symbol_table)
        right_type = self.right.resolveExpressionType(symbol_table)

        if not is_non_ptr_variable_type(left_type) or not is_non_ptr_variable_type(right_type):
            Logger.error("Pointers, arrays and functions cannot be used as operators for subtraction. Tried to use types '{}' and '{}' on line {}."
                            .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            raise AstTypingException()

        self.expression_type = get_maximal_type(left_type, right_type)

        return self.expression_type

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

    def resolveExpressionType(self, symbol_table):
        # only "values" are allowed

        left_type = self.left.resolveExpressionType(symbol_table)
        right_type = self.right.resolveExpressionType(symbol_table)

        if not is_non_ptr_variable_type(left_type) or not is_non_ptr_variable_type(right_type):
            Logger.error("Only pointers, arrays and functions cannot be used as operators for multiplication. Tried to use types '{}' and '{}' on line {}."
                            .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            raise AstTypingException()

        self.expression_type = get_maximal_type(left_type, right_type)

        return self.expression_type

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

    def resolveExpressionType(self, symbol_table):
        # only "values" are allowed

        left_type = self.left.resolveExpressionType(symbol_table)
        right_type = self.right.resolveExpressionType(symbol_table)

        if not is_non_ptr_variable_type(left_type) or not is_non_ptr_variable_type(right_type):
            Logger.error("Pointers, arrays and functions cannot be used as operators for division. Tried to use types '{}' and '{}' on line {}."
                            .format(left_type.toString(), right_type.toString(), self.getLineNr()))
            raise AstTypingException()

        self.expression_type = get_maximal_type(left_type, right_type)

        return self.expression_type

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

    def resolveExpressionType(self, symbol_table):
        # only on integers, char, bool

        left_type = self.left.resolveExpressionType(symbol_table)
        right_type = self.right.resolveExpressionType(symbol_table)

        left_type_name = None
        right_type_name = None

        if left_type.isVar() and not left_type.toString().endswith("*") and not left_type.toString() == 'float':
            left_type_name = left_type.toString()
        else:
            Logger.error("Operands of modulo operator need to be of type 'bool', 'char', or 'int'. LHS argument of type '{}' was given on line {}."
                            .format(left_type.toString(), self.getLineNr()))
            raise AstTypingException()

        if right_type.isVar() and not right_type.toString().endswith("*") and not right_type.toString() == 'float':
            right_type_name = right_type.toString()
        else:
            Logger.error("Operands of modulo operator need to be of type 'bool', 'char', or 'int'. RHS side argument of type '{}' was given on line {}."
                            .format(right_type.toString(), self.getLineNr()))
            raise AstTypingException()

        # always convert to int
        self.expression_type = VariableType("int")

        return self.expression_type


    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)

# TODO: find out how!
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

    def resolveExpressionType(self, symbol_table):
        # returns the same type as the target expression

        target_type = self.expression.resolveExpressionType(symbol_table)

        if target_type.isFunction():
            Logger.error("Logical not operator cannot be applied to functions. Tried to apply to function of type '{}' on line {}.".format(target_type.toString(), self.getLineNr()))
            raise AstTypingException()

        self.expression_type = target_type

        return self.expression_type

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

    def resolveExpressionType(self, symbol_table):
        # returns the same type as the target expression

        # get type of target expression
        target_type = self.expression.resolveExpressionType(symbol_table)

        # ptr, array and function is not allowed
        if not target_type.isVar():
            Logger.error("Prefix increment cannot be performed on arrays or functions. Tried to apply on type '{}' on line {}."
                            .format(target_type.toString(), self.getLineNr()))
            raise AstTypingException()

        self.expression_type = target_type

        return self.expression_type

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

    def resolveExpressionType(self, symbol_table):
        # returns the same type as the target expression

        # get type of target expression
        target_type = self.expression.resolveExpressionType(symbol_table)

        # ptr, array and function is not allowed
        if not target_type.isVar():
            Logger.error("Prefix decrement cannot be performed on arrays or functions. Tried to apply on type '{}' on line {}."
                            .format(target_type.toString(), self.getLineNr()))
            raise AstTypingException()

        self.expression_type = target_type

        return self.expression_type

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

    def resolveExpressionType(self, symbol_table):
        # returns the same type as the target expression

        # get type of target expression
        target_type = self.expression.resolveExpressionType(symbol_table)

        # ptr, array and function is not allowed
        if not target_type.isVar():
            Logger.error("Postfix increment cannot be performed on arrays or functions. Tried to apply on type '{}' on line {}."
                            .format(target_type.toString(), self.getLineNr()))
            raise AstTypingException()

        self.expression_type = target_type

        return self.expression_type

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

    def resolveExpressionType(self, symbol_table):
        # returns the same type as the target expression

        # get type of target expression
        target_type = self.expression.resolveExpressionType(symbol_table)

        # ptr, array and function is not allowed
        if not target_type.isVar():
            Logger.error("Postfix decrement cannot be performed on arrays or functions. Tried to apply on type '{}' on line {}."
                            .format(target_type.toString(), self.getLineNr()))
            raise AstTypingException()

        self.expression_type = target_type

        return self.expression_type

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

    def resolveExpressionType(self, symbol_table):
        # returns the same type as the target expression

        # get type of target expression
        target_type = self.expression.resolveExpressionType(symbol_table)

        # ptr, array and function is not allowed
        if not is_non_ptr_variable_type(target_type):
            Logger.error("Unary plus cannot be performed on pointers, arrays or functions. Tried to apply on type '{}' on line {}."
                            .format(target_type.toString(), self.getLineNr()))
            raise AstTypingException()

        self.expression_type = target_type

        return self.expression_type

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

    def resolveExpressionType(self, symbol_table):
        # returns the same type as the target expression

        # get type of target expression
        target_type = self.expression.resolveExpressionType(symbol_table)

        # ptr, array and function is not allowed
        if not is_non_ptr_variable_type(target_type):
            Logger.error("Unary minus cannot be performed on pointers, arrays or functions. Tried to apply on type '{}' on line {}."
                            .format(target_type.toString(), self.getLineNr()))
            raise AstTypingException()

        self.expression_type = target_type

        return self.expression_type

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
        """
            Constructor.

            Params:
                'target_array': IdentifierExpr that represents the array.
                'index_expr': Expression that evaluates to a type compatible with 'int'
        """
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

    def resolveExpressionType(self, symbol_table):
        target_type = self.target_array.resolveExpressionType(symbol_table)

        target_name = self.target_array.getIdentifierName()

        if target_type.isArray():
            # access on an array returns an entry
            self.expression_type = VariableType(target_type.getEntryType())
        elif target_type.isVar() and target_type.toString().endswith("*"):
            # access on a ptr, dereferences the ptr
            self.expression_type = VariableType(target_type.toString()[:-1]) # remove star
        else:
            # invalid target
            Logger.error("Array access can only be performed on arrays and pointers. Tried to apply array access on '{}' with type '{}' on line '{}'."
                            .format(target_name, target_type.toString(), self.getLineNr()))
            raise AstTypingException()

        # check that index expression can evaluated to int
        index_type = self.index_expr.resolveExpressionType(symbol_table)

        # index type needs to be compatible with 
        if not is_conversion_possible('int', index_type.toString()):
            Logger.error("Invalid index expression passed to array '{}' on line {}: Type '{}' is requested, incompatible type '{}' was given."
                            .format(target_name, self.getLineNr(), 'int', index_type.toString()))
            raise AstTypingException()

        return self.expression_type

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

    def resolveExpressionType(self, symbol_table):
        target_type = self.target_ptr.resolveExpressionType(symbol_table)

        # only pointer variables can be dereferenced.
        if target_type.isVar() and target_type.toString().endswith("*"):
            new_type = VariableType(target_type.toString()[:-1]) # strip the pointer star
        elif target_type.isArray():
            new_type = VariableType(target_type.getEntryType()) # deref of array simply points to first element.
        else:
            Logger.error("Only pointer types and array types can be dereferened. Tried to derefence type '{}' on line {}.".format(target_type.toString(), self.getLineNr()))
            raise AstTypingException()

        self.expression_type = new_type

        return self.expression_type

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

    def resolveExpressionType(self, symbol_table):
        target_type = self.target_expr.resolveExpressionType(symbol_table)

        if target_type.isArray():
            entry_type = target_type.getEntryType()
            new_type = VariableType(entry_type + "*")
            # array is pointer to first element
            # pointer to array is pointer to pointer to first element
        elif target_type.isFunction():
            Logger.error("Error at line {}. Cannot take address of function.".format(self.getLineNr()))
            raise AstTypingException()
        elif target_type.isVar():
            target_type_name = target_type.toString()
            # add ptr level
            new_type = VariableType(target_type_name + "*")

        # a pointer to the target is returned.
        self.expression_type = new_type

        return self.expression_type


    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.target_expr],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)

# TODO narrowing
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

    def resolveExpressionType(self, symbol_table):
        # f(param, param)

        # identifier will be of type "ret_type(param_type, param_type, ...)"
        # if the function is not yet delcared, it will be detected here
        # NOTE: arguments still need to be checked!
        function_type = self.identifier.resolveExpressionType(symbol_table)

        # retrieve a string that contains the name of the function
        function_name = self.identifier.getIdentifierName()

        if not function_type.isFunction():
            Logger.error("Symbol '{}' cannot be called as a function on line {}".format(function_name, self.getLineNr()))
            raise AstTypingException()

        # check argument count
        if len(self.argument_list) != len(function_type.getParamTypes()):
            Logger.error("Function {} called with invalid amount of arguments on line {}. {} parameters needed, {} parameters specified."
                            .format(function_name, len(function_type.getParamTypes()), len(self.argument_list)))
            raise AstTypingException()

        # check arguments
        for i in range(0, len(self.argument_list)):
            arg_expr_type = self.argument_list[i].resolveExpressionType(symbol_table) # supplied param type
            param_type = function_type.getParamTypes()[i] # expected param type

            if arg_expr_type.isFunction():
                Logger.error("Invalid argument #{} passed to function '{}' on line {}: Functions cannot be passed as argument."
                                .format(i+1, function_name, self.getLineNr()))
                raise AstTypingException()

            # check if parameters are compatible
            if not is_conversion_possible(VariableType(param_type), arg_expr_type):
                Logger.error("Invalid argument #{} passed to function '{}' on line {}: Type '{}' is requested, incompatible type '{}' was given."
                                .format(i+1, function_name, self.getLineNr(), param_type, arg_expr_type.toString()))
                raise AstTypingException()

            # parameters are compatible, check for narrowing
            if will_conversion_narrow(VariableType(param_type), arg_expr_type):
                Logger.warning("Passing expression of type '{}' as argument #{} for function '{}' narrowing on line {}. Expected type is '{}'."
                                    .format(arg_expr_type.toString(), i+1, function_name, self.getLineNr(), param_type))
                # no exception needed here

        self.expression_type = VariableType(function_type.getReturnType())

        return self.expression_type

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
        """
            Constructor.

            Param:
                'identifier': A string that contains the name of the identifier.
        """
        super().__init__(expression_type="IdentifierExpr\\n'" + identifier + "'")
        self.identifier = identifier

    def getIdentifierName(self):
        return self.identifier

    def setExprTreeSymbolTable(self, symbol_table):
        self.setSymbolTable(symbol_table)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)

    def resolveExpressionType(self, symbol_table):
        # extract from table
        symbol_type, scope_name = symbol_table.lookup(self.identifier)

        # determine if symbol exists in table
        if symbol_type == 0:
            # symbol not found
            Logger.error("Referenced undeclared symbol {} at line {}.".format(self.identifier, self.getLineNr()))
            raise AstTypingException()
        else:
            # set symbol type
            self.expression_type = symbol_type

            # returned type can be of function, array or variable
            return self.expression_type


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

    def resolveExpressionType(self, symbol_table):
        self.expression_type = VariableType('int')

        return self.expression_type


class FloatConstantExpr(ConstantExpr):
    """
        Node that represents float constants: "012345.6789".
    """

    def __init__(self, float_value):
        super().__init__(constant_expr_type="FloatConstant", value=float_value)

    def getFloatValue(self):
        return float(self.getValue())

    def resolveExpressionType(self, symbol_table):
        self.expression_type = VariableType('float')

        return self.expression_type


class StringConstantExpr(ConstantExpr):
    """
        Node that represents string constants: "abcdef".
    """

    def __init__(self, str_value):
        super().__init__(constant_expr_type="StrConstant", value=str_value)

    def getStrValue(self):
        return str(self.getValue())

    def resolveExpressionType(self, symbol_table):
        # string is a char pointer
        self.expression_type = VariableType('char*')

        return self.expression_type


class CharConstantExpr(ConstantExpr):
    """
        Node that represents character constants: 'a', 'b', 'abc'.
    """

    def __init__(self, char_value):
        super().__init__(constant_expr_type="CharConstant", value=char_value)

    def getCharValue(self):
        return str(self.getValue())

    def resolveExpressionType(self, symbol_table):
        self.expression_type = VariableType('char')

        return self.expression_type


class BoolConstantExpr(ConstantExpr):
    """
        Node that represents boolean constants: 'true', 'false'.
    """

    def __init__(self, bool_value):
        super().__init__(constant_expr_type="BoolConstant", value=bool_value)

    def getBoolValue(self):
        return str(self.getValue()).lower() == "true"

    def resolveExpressionType(self, symbol_table):
        self.expression_type = VariableType('bool')

        return self.expression_type

############### TYPE FUNCTIONS ###############

def type_to_string(typename, pointer_count):
    return typename + ("*"*pointer_count)


def get_maximal_type(type_a, type_b):
    """
        Returns the widest type of the two specified types. The following order is used: float > int > char > bool.
        Only non-pointer variable types are allowed!
    """
    
    type_list = ['bool', 'char', 'int', 'float']

    type_a_idx = type_list.index(type_a.toString())
    type_b_idx = type_list.index(type_b.toString())

    max_id = max(type_a_idx, type_a_idx)

    return type_list[max_id]

def is_non_ptr_variable_type(type):
    """
        Determines whether or not the specified type is a non-pointer variable type.
    """
    return type.isVar() and not type.toString().endswith("*")

def is_integral_variable_type(type):
    """
        Determines whether or not the specified type is an integral type.
    """
    return type.isVar() and type.toString() in ['bool', 'char', 'int']

def is_conversion_possible(target_type, original_type):
    """
        Determine whether or not a conversion from the original type to the target type is possible.
    """

    # two different pointer types: not possible
    # two different value types: maybe
    # array assigned to array_entry_type* ok
    # functions are not assignable
    # assignment to array is not possible, and array-type parameters are not possible.

    # -> if target, origin is var, non-ptr and value types:
    #   -> further determine value types
    #   -> !! void not allowed!!
    # -> if taret is ptr:
    #       -> if original is identical ptr: ok
    #       -> if original is compatible array: ok
    # return false.

    pass

def will_conversion_narrow(target_type, original_type):
    """
        Determine whether or not a conversion from the original type to the target type will result in narrowing.
    """

    # if target < original_type:
    #   return True
    # return False

    pass