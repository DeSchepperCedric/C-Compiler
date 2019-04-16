
class ASTNode:
    """
        Base class for all nodes in AST Trees.
    """
    def __init(self, node_name):
        self.node_name = node_name

    def getNodeName(self):
        return self.node_name
# ENDCLASS


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
# ENDCLASS


class IncludeNode(ASTNode):
    """
        Node that represents "#include <stdio.h>"
    """

    def __init__(self):
        super().__init__(node_name="Include")
# ENDCLASS


class FuncDecl(ASTNode):
    """
        Node that represents a function declaration: "type func(type param);"
    """
    def __init__(self, return_type, func_id, param_list):
        super().__init__(node_name="FuncDecl")
        self.return_type = return_type
        self.func_id = func_id
        self.param_list = param_list

    def getReturnType(self):
        return self.return_type

    def getFuncID(self):
        return self.func_id

    def getParamList(self):
        return self.param_list
# ENDCLASS


class SymbolDecl(ASTNode):
    """
        Base class for variable declaration nodes.
    """
    def __init__(self, symbol_name, var_type, var_id):
        super().__init__(node_name="SymbolDecl:" + symbol_name)
        self.type = var_type
        self.id = identifier_with_ptr

    def getType(self):
        return self.type

    def getID(self):
        return self.id
# ENDCLASS
        

class ArrayDecl(SymbolDecl):
    """
        Node that represents an array declaration: "type id[size_expr];"
    """

    def __init__(self, array_type, array_id, size_expr):
        super().__init__(symbol_name="Array",
                         var_type = array_type,
                         var_id = array_id)
        self.size_expr = size_exp

    def getSizeExp(self):
        return self.size_expr
# ENDCLASS


class VarDelcDefault(SymbolDecl):
    """
        Node that represents a variable declaration without initializer: "type id;"
    """
    def __init__(self, var_type, var_id):
        super().__init__(symbol_name="Var",
                         var_type=var_type,
                         var_id=var_id)
# ENDCLASS


class VarDeclWithInit(SymbolDecl):
    """
        Node that represents a variabele declaration with initializer: "type id = init_expr;"
    """

    def __init__(self, var_type, var_id, init_expr):
        super().__init__(symbol_name="VarWithInit",
                         var_type=var_type,
                         var_id=var_id)
        self.init_expr = init_expr

    def getInitExpr(self):
        return self.init_expr
# ENDCLASS


class FuncDef(ASTNode):
    """
		Node that represents a function definition: "type func(param) { <statements> }"
    """
    def __init__(self, return_type, func_id, param_list, body)
        super().__init__(node_name="FuncDef")
        self.return_type = return_type
        self.func_id     = func_id
        self.param_list  = param_list
        self.body        = body

    def getReturnType(self):
        return self.return_type

    def getFuncID(self):
        return self.func_id

    def getParamList(self):
        return self.param_list

    def getBody(self):
    	return self.body
# ENDCLASS


class IdWithPtr(ASTNode):
    """
		Node that represents an identifier that can possibly be a pointer: "**id"; "id", "*id", etc.
    """
    def __init__(self, id_name, pointer_count):
    	super().__init__(node_name="IdWithPtr")
    	self.identifier = self.identifier
    	self.pointer_count = pointer_count

    def getID(self):
    	return self.identifier

    def getPointerCount(self):
    	return self.pointer_count
# ENDCLASS


class Body(ASTNode):
	def __init__(self, child_list):
		super().__init__(node_name="Body")
		self.child_list = child_list

	def getChildren(self):
		return self.child_list
# ENDCLASS


class FuncParam(ASTNode):
    """
		Node that represents a function param: "type id_with_ptr".
    """
    def __init__(self, param_type, param_id):
    	super().__init__(node_name="FuncParam")
    	self.param_type = param_type
    	self.param_id   = param_id

    def getParamType(self):
    	return self.param_type

    def getParamID(self):
    	return self.param_id
# ENDCLASS


class Statement(ASTNode):
	"""
		Base class for statements nodes.
	"""
    def __init__(self, statement_type):
    	super().__init__(node_name="Stmt:"+statement_type)


class CompoundStmt(Statement):
    """
		Node that represents a compound statement: "{ <statements> }".
    """
    def __init__(self, child_list):
    	super().__init__(statement_type="CompoundStmt")
    	self.child_list = child_list

    def getChildList(self):
    	return self.child_list
# ENDCLASS


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
# ENDCLASS


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
# ENDCLASS


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
# ENDCLASS


class ExpressionStatement(Statement):
	"""
		Node that represents an expression statement.
		An expression statement can contain multiple expressions.
	"""
    def __init__(self, expressions):
    	super().__init__(statement_type="ExpressionStatement")
    	self.expressions = expressions

    def getExpressions(self):
    	return self.expressions
# ENDCLASS


class Expression(ASTNode):
    """
		Base class for all expression nodes.
    """
    
    def __init__(self, expression_type):
    	super().__init__(node_name=expression_type)
# ENDCLASS


class AssignmentExpr(Expression):
    """
		Node that represents assignment expression.
    """
    
    def __init__(self, left, right, operator):
    	super().__init__(expression_type="AssignmentExpr")
    	self.left = left
    	self.right = right

    	self.operator = operator

    def getLeft(self):
    	return self.left

    def getRight(self):
    	return self.right

    def getOperator(self):
    	return self.operator
# ENDCLASS


class LogicBinExpr(Expression):
	"""
		Node that represents AND, OR expression.
	"""

    def __init__(self, left, right, operator):
    	super().__init__(expression_type="AssignmentExpr")
    	self.left = left
    	self.right = right

    	self.operator = operator

    def getLeft(self):
    	return self.left

    def getRight(self):
    	return self.right

    def getOperator(self):
    	return self.operator
# ENDCLASS


class EqualityExpr(Expression):
    # left
    # right
    # operator: {'==', '!='}
    pass
# ENDCLASS


class ComparisonExpr(Expression):
    # left
    # right
    # operator: {'<', '>', '<=', '>='}
    pass
# ENDCLASS


class AdditiveExpr(Expression):
    # left
    # right
    # operator: {'+', '-'}
    pass
# ENDCLASS


class MultiplicativeExpr(Expression):
    # left
    # right
    # operator: {'*', '/', '%'}
    pass
# ENDCLASS


class CastExpr(Expression):
    # list of types
    # expr
    pass
# ENDCLASS


class LogicNotExpr(Expression):
    # expr
    pass
# ENDCLASS


class PrefixIncDecExpr(Expression):
    # ++x, --x
    # op: {'++', '--'}
    # expr
    pass
# ENDCLASS


class PostfixIncDecExpr(Expression):
    # x++, x--
    # expr
    # op: {'++', '--'}
    pass
# ENDCLASS


class PlusMinPrefixExpr(Expression):
    # +x, -x
    # op: {'+', '-'}
    # expr
    pass
# ENDCLASS


class ArrayAccessExpr(Expression):
    # target: expression
    # index: expression
    pass
# ENDCLASS


class PointerDerefExpr(Expression):
    # *x
    # expr
    pass
# ENDCLASS


class FuncCallExpr(Expression):
    # functionname
    # List of Expression: parameters
    pass
# ENDCLASS


class IdentifierExpr(Expression):
    # identifier
    pass
# ENDCLASS


class ConstantExpr(Expression):
    # base class for constants
    pass
# ENDCLASS


class IntegerConstantExpr(ConstantExpr):
    pass
# ENDCLASS


class FloatConstantExpr(ConstantExpr):
    pass
# ENDCLASS


class StringConstantExpr(ConstantExpr):
    pass
# ENDCLASS


class CharConstantExpr(ConstantExpr):
    pass
# ENDCLASS


class BoolConstantExpr(ConstantExpr):
    pass
# ENDCLASS
