class ASTNode:
    """
        Base class for all nodes in AST Trees.
    """

    def __init__(self, node_name):
        self.node_name = node_name

    def getNodeName(self):
        return self.node_name

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
        new_children = list()
        for child in children:
            if child is None:
                continue

            if isinstance(child, list):
                new_children.append(*child)
            else:
                new_children.append(child)

        for child in new_children:
            # the child should have node number 'current_node_nr+1'
            # update the current node number

            current_node_nr, child_dotdata = child.toDot(parent_nr=begin_nr, begin_nr=current_node_nr + 1)

            # add the dotfile data to the current data
            dotdata += child_dotdata

        if add_open_close:
            dotdata = "digraph ast_tree {\nsplines=ortho;\n" + dotdata + "}\n"

        return (current_node_nr, dotdata)


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


class ProgramNode(ASTNode):
    """
        Node that represents the entire program.
    """

    def __init__(self):
        super().__init__(node_name="Program")
        self.children = []

    def addChild(self, child):
        self.children.append(child)

    def getChildren(self):
        return self.children

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


class SymbolDecl(TopLevelNode):
    """
        Base class for variable declaration nodes.
    """

    def __init__(self, symbol_class : str, symbol_type : str, symbol_id : str, symbol_ptr_cnt : int):
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


class ArrayDecl(SymbolDecl):
    """
        Node that represents an array declaration: "type id[size_expr];"
    """

    def __init__(self, array_type : str, array_id : str, ptr_count : int, size_expr):
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


class VarDeclDefault(SymbolDecl):
    """
        Node that represents a variable declaration without initializer: "type id;"
    """

    def __init__(self, var_type : str, var_id : str, ptr_count : int):
        super().__init__(symbol_class="VarDefault",
                         symbol_type=var_type,
                         symbol_id=var_id,
                         symbol_ptr_cnt=ptr_count)

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class VarDeclWithInit(SymbolDecl):
    """
        Node that represents a variabele declaration with initializer: "type id = init_expr;"
    """

    def __init__(self, var_type : str, var_id : str, ptr_count : int, init_expr):
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


class FuncDecl(SymbolDecl):
    """
        Node that represents a function declaration: "type func(type param);"
    """

    def __init__(self, return_type : str, func_id : str, ptr_count : int, param_list):
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


class FuncDef(TopLevelNode):
    """
    Node that represents a function definition: "type func(param) { <statements> }"
    """

    def __init__(self, return_type : str, func_id : str, ptr_count : int, param_list : list, body):
        super().__init__(node_name="FuncDef\\nType:'" + return_type + "'")
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


class Body(ASTNode):
    """
        Node that represents the body of statement (e.g. forloop, whileloop, etc). This is simply a list of statements.
    """

    def __init__(self, child_list):
        super().__init__(node_name="Body")
        self.child_list = child_list

    def getChildren(self):
        return self.child_list

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=self.child_list,
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class FuncParam(ASTNode):
    """
        Node that represents a function param: "type id_with_ptr".
    """

    def __init__(self, param_type : str, param_id : str, ptr_count : int):
        super().__init__(node_name="FuncParam\\nType:'" + param_type + "'")
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


class Statement(ASTNode):
    """
        Base class for statements nodes.
    """

    def __init__(self, statement_type):
        super().__init__(node_name="Stmt:" + statement_type)


class CompoundStmt(Statement):
    """
    Node that represents a compound statement: "{ <statements> }".
    """

    def __init__(self, child_list):
        super().__init__(statement_type="CompoundStmt")
        self.child_list = child_list

    def getChildList(self):
        return self.child_list

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

    def __init__(self, init, condition_expr, iter_expr, body):
        super().__init__(statement_type="ForStmt")
        self.init = init
        self.cond_expr = condition_expr
        self.iter_expr = iter_expr
        self.body = body

    def getInit(self):
        return self.init

    def getCondExpr(self):
        return self.cond_expr

    def getIterExpr(self):
        return self.iter_expr

    def getBody(self):
        return self.body

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.init, self.cond_expr, self.iter_expr, self.body],
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


# ENDCLASS


class ReturnStatement(JumpStatement):
    """
        Node that represents a return statement.
    """

    def __init__(self):
        super().__init__(jump_type="return")

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[],
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


class AssignmentExpr(Expression):
    """
        Node that represents assignment expression.
    """

    def __init__(self, left, right, operator):
        super().__init__(expression_type="AssignmentExpr:" + str(operator))
        self.left = left
        self.right = right

        self.operator = operator

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def getOperator(self):
        return self.operator

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class LogicOrExpr(Expression):
    """
        Node that represents OR expression.
    """

    def __init__(self, left, right):
        super().__init__(expression_type="LogicOrExpr")
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class LogicAndExpr(Expression):
    """
        Node that represents AND expression.
    """
    def __init__(self, left, right):
        super().__init__(expression_type="LogicAndExpr")
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right


class EqualityExpr(Expression):
    """
        Node that represents equality or inequality expression.
    """

    def __init__(self, left, right, operator):
        super().__init__(expression_type="EqualityExpr:" + str(operator))
        self.left = left
        self.right = right

        self.operator = operator

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def getOperator(self):
        return self.operator

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class ComparisonExpr(Expression):
    """
        Node that represents a comparison.
    """

    def __init__(self, left, right, operator):
        super().__init__(expression_type="ComparisonExpr:" + str(operator))
        self.left = left
        self.right = right

        self.operator = operator

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def getOperator(self):
        return self.operator

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class AdditiveExpr(Expression):
    """
        Node that represents an addition or subtraction.
    """

    def __init__(self, left, right, operator):
        super().__init__(expression_type="AdditiveExpr:" + str(operator))
        self.left = left
        self.right = right

        self.operator = operator

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def getOperator(self):
        return self.operator

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.left, self.right],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class MultiplicativeExpr(Expression):
    """
        Node that represents a multiplication, division or modulo operation.
    """

    def __init__(self, left, right, operator):
        super().__init__(expression_type="MultiplicativeExpr:" + str(operator))
        self.left = left
        self.right = right

        self.operator = operator

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def getOperator(self):
        return self.operator

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

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[self.target_expr],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class FuncCallExpr(Expression):
    """
        Node that represents a function call: "identifier(params)".
    """

    def __init__(self, function_identifier : str, argument_list):
        """
        Params:
            'function_identifier': IdentifierNode object that represents the identifier of the function.
            'argument_list': list of Expression
        """
        super().__init__(expression_type="FuncCallExpr")
        self.identifier = function_identifier
        self.argument_list = argument_list

    def getFunctionID(self):
        return self.identifier

    def getArguments(self):
        return self.argument_list

    def toDot(self, parent_nr, begin_nr, add_open_close=False):
        return self.M_defaultToDotImpl(children=[*self.argument_list],
                                       parent_nr=parent_nr,
                                       begin_nr=begin_nr,
                                       add_open_close=add_open_close)


class IdentifierExpr(Expression):
    """
        Node that represents an identifier expression (different from the idenfier itself!)
    """

    def __init__(self, identifier : str):
        super().__init__(expression_type="IdentifierExpr\\n"+identifier)
        self.identifier = identifier

    def getIdentifier(self):
        return self.identifier

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
        super().__init__(expression_type=constant_expr_type + ":'" + str(value) + "'")
        self.value = value

    def getValue(self):
        return self.value

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

