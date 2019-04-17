
class ASTNode:
    """
        Base class for all nodes in AST Trees.
    """
    def __init(self, node_name):
        self.node_name = node_name

    def getNodeName(self):
        return self.node_name

    def toDot(self):
        return ""
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

    def toDot(self):
        # nr [label="ProgramNode"]
        # nr -> parent_nr
# ENDCLASS


class TopLevelNode(ASTNode):
    """
        Base class for nodes that appear directly underneath the program node.
    """
    def __init__(self, node_name):
        super().__init__(node_name=node_name)
# ENDCLASS


class IncludeNode(TopLevelNode):
    """
        Node that represents "#include <stdio.h>"
    """

    def __init__(self):
        super().__init__(node_name="Include")
# ENDCLASS


class SymbolDecl(TopLevelNode):
    """
        Base class for variable declaration nodes.
    """
    def __init__(self, symbol_class, symbol_type, symbol_id):
        super().__init__(node_name="SymbolDecl:" + symbol_class)
        self.symbol_type = symbol_type
        self.symbol_id = symbol_id

    def getType(self):
        return self.symbol_type

    def getID(self):
        return self.symbol_id
# ENDCLASS
        

class ArrayDecl(SymbolDecl):
    """
        Node that represents an array declaration: "type id[size_expr];"
    """

    def __init__(self, array_type, array_id, size_expr):
        super().__init__(symbol_class="Array",
                         symbol_type = array_type,
                         symbol_id = array_id)
        self.size_expr = size_exp

    def getSizeExp(self):
        return self.size_expr
# ENDCLASS


class VarDelcDefault(SymbolDecl):
    """
        Node that represents a variable declaration without initializer: "type id;"
    """
    def __init__(self, var_type, var_id):
        super().__init__(symbol_class="Var",
                         symbol_type=var_type,
                         symbol_id=var_id)
# ENDCLASS


class VarDeclWithInit(SymbolDecl):
    """
        Node that represents a variabele declaration with initializer: "type id = init_expr;"
    """

    def __init__(self, var_type, var_id, init_expr):
        super().__init__(symbol_class="VarWithInit",
                         symbol_type=var_type,
                         symbol_id=var_id)
        self.init_expr = init_expr

    def getInitExpr(self):
        return self.init_expr
# ENDCLASS

class FuncDecl(SymbolDecl):
    """
        Node that represents a function declaration: "type func(type param);"
    """
    def __init__(self, return_type, func_id, param_list):
        super().__init__(symbol_class="FuncDecl",
                         symbol_type=return_type,
                         symbol_id=func_id)
        self.param_list = param_list

    def getParams(self):
        return self.param_list
# ENDCLASS


class FuncDef(TopLevelNode):
    """
	Node that represents a function definition: "type func(param) { <statements> }"
    """
    def __init__(self, return_type, func_id, param_list, body):
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
    """
        Node that represents the body of statement (e.g. forloop, whileloop, etc). This is simply a list of statements.
    """
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
# ENDCLASS


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


class JumpStatement(Statement):
    """
        Base class for jump statements.
    """
    def __init__(self, jump_type):
        super().__init__(statement_type="JumpStmt:"+jump_type)
# ENDCLASS


class ReturnStatement(JumpStatement):
    """
        Node that represents a return statement.
    """
    def __init__(self):
        super().__init__(jump_type="return")
# ENDCLASS


class BreakStatement(JumpStatement):
    """
        Node that represents a return statement.
    """
    def __init__(self):
        super().__init__(jump_type="break")
# ENDCLASS


class ContinueStatement(JumpStatement):
    """
        Node that represents a return statement.
    """
    def __init__(self):
        super().__init__(jump_type="continue")
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


class ParenExpression(Expression):
	"""
		Node that represents a parentheses expression: "(expr)".
	"""
	def __init__(self, expression):
		super().__init__(expression_type="ParenExpression")
		self.expression = expression

	def getExpr(self):
		return self.expression
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
    """
    	Node that represents equality or inequality expression.
    """
    def __init__(self, left, right, operator):
    	super().__init__(expression_type="EqualityExpr")
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


class ComparisonExpr(Expression):
    """
        Node that represents a comparison.
    """
    def __init__(self, left, right, operator):
    	super().__init__(expression_type="ComparisonExpr")
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


class AdditiveExpr(Expression):
    """
        Node that represents an addition or subtraction.
    """
    def __init__(self, left, right, operator):
    	super().__init__(expression_type="AdditiveExpr")
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


class MultiplicativeExpr(Expression):
    """
        Node that represents a multiplication, division or modulo operation.
    """
    def __init__(self, left, right, operator):
    	super().__init__(expression_type="MultiplicativeExpr")
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


class CastExpr(Expression):
    """
        Node that represents a cast expression.
    """
    def __init__(self, type_list, expression):
    	super().__init__(expression_type="CastExpr")
    	self.type_list = type_list
    	self.expression = expression

    def getTypeList(self):
    	return self.type_list

    def getExpr(self):
    	return self.expression
# ENDCLASS


class LogicNotExpr(Expression):
    """
        Node that represents a logical NOT expression.
    """
    def __init__(self, expression):
    	super().__init__(expression_type="LogicNotExpr")
    	self.expression = expression

    def getExpr(self):
    	return self.expression
# ENDCLASS


class PrefixIncExpr(Expression):
    """
        Node that represents "++x".
    """
    def __init__(self, expression,):
    	super().__init__(expression_type="PrefixIncExpr")
    	self.expression = expression

    def getExpr(self):
    	return self.expression
# ENDCLASS

class PrefixDecExpr(Expression):
    """
        Node that represents "--x".
    """
    def __init__(self, expression):
    	super().__init__(expression_type="PrefixDecExpr")
    	self.expression = expression

    def getExpr(self):
    	return self.expression
# ENDCLASS


class PostfixIncExpr(Expression):
    """
        Node that represents "x++".
    """
    def __init__(self, expression, operator):
    	super().__init__(expression_type="PostfixIncExpr")
    	self.expression = expression

    def getExpr(self):
    	return self.expression

# ENDCLASS

class PostfixDecExpr(Expression):
    """
        Node that represents "x--".
    """
    def __init__(self, expression, operator):
    	super().__init__(expression_type="PostfixDecExpr")
    	self.expression = expression

    def getExpr(self):
    	return self.expression
# ENDCLASS


class PlusPrefixExpr(Expression):
    """
        Node that represents a plus prefix expression: "+x".
    """
    def __init__(self, expression):
    	super().__init__(expression_type="PlusPrefixExpr")
    	self.expression = expression

    def getExpr(self):
    	return self.expression
# ENDCLASS

class MinPrefixExpr(Expression):
    """
        Node that represents a minus prefix expression: "-x".
    """
    def __init__(self, expression):
    	super().__init__(expression_type="MinPrefixExpr")
    	self.expression = expression

    def getExpr(self):
    	return self.expression
# ENDCLASS


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
# ENDCLASS


class PointerDerefExpr(Expression):
    """
    	Node that represents a pointer dereference expression: "*target_ptr".
    """
    def __init__(self, target_ptr):
    	super().__init__(expression_type="PointerDerefExpr")
    	self.target_ptr = target_ptr

    def getTargetPtr(self):
    	return self.target_ptr
# ENDCLASS


class FuncCallExpr(Expression):
    """
    	Node that represents a function call: "identifier(params)".
    """
    def __init__(self, function_identifier, argument_list):
    	super().__init__(expression_type="FuncCallExpr")
    	self.identifier = function_identifier
    	self.argument_list = argument_list

    def getFunctionID(self):
        return self.function_identifier

    def getArguments(self):
        return self.argument_list
# ENDCLASS


class IdentifierExpr(Expression):
    """
        Node that represents an identifier.
    """
    def __init__(self, identifier):
    	super().__init__(expression_type="IdentifierExpr")
    	self.identifier = identifier

    def getIdentifier(self):
    	return self.identifier
# ENDCLASS


class ConstantExpr(Expression):
    """
        Base class for constant expressions.
    """
    def __init__(self, constant_expr_type, value):
    	super().__init__(expression_type="constant_expr_type")

    def getValue(self):
    	return self.value
# ENDCLASS


class IntegerConstantExpr(ConstantExpr):
    """
        Node that represents integer constants: "0123456789".
    """
    def __init__(self, integer_value):
    	super().__init__(constant_expr_type="IntConstant", value = integer_value)
    
    def getIntValue(self):
    	return int(self.getValue())
# ENDCLASS


class FloatConstantExpr(ConstantExpr):
    """
        Node that represents float constants: "012345.6789".
    """
    def __init__(self, float_value):
    	super().__init__(constant_expr_type="IntConstant", value = float_value)
    
    def getFloatValue(self):
    	return float(self.getValue())
# ENDCLASS


class StringConstantExpr(ConstantExpr):
    """
        Node that represents string constants: "abcdef".
    """
    def __init__(self, str_value):
    	super().__init__(constant_expr_type="IntConstant", value = str_value)
    
    def getStrValue(self):
    	return str(self.getValue())
# ENDCLASS


class CharConstantExpr(ConstantExpr):
    """
        Node that represents character constants: 'a', 'b', 'abc'.
    """
    def __init__(self, char_value):
    	super().__init__(constant_expr_type="IntConstant", value = char_value)
    
    def getCharValue(self):
    	return str(self.getValue())
# ENDCLASS


class BoolConstantExpr(ConstantExpr):
    """
        Node that represents boolean constants: 'true', 'false'.
    """
    def __init__(self, bool_value):
    	super().__init__(constant_expr_type="IntConstant", value = bool_value)
    
    def getBoolValue(self):
    	return str(self.getValue()).lower() == "true"
# ENDCLASS


class TypeNode(ASTNode):
    """
        Node that represents a type.
    """
    def __init__(self, type_name):
        super().__init__(node_name="Type:"+type_name)
        self.type_name = type_name

    def getTypeName(self):
        return self.type_name
# ENDCLASS


class TypeVoid(TypeNode):
    """
        Node that represents the 'void' type.
    """
    def __init__(self):
        super().__init__(type_name="void")
# ENDCLASS


class TypeInt(TypeNode):
    """
        Node that represents the 'int' type.
    """
    def __init__(self):
        super().__init__(type_name="int")
# ENDCLASS

class TypeFloat(TypeNode):
    """
        Node that represents the 'float' type.
    """
    def __init__(self):
        super().__init__(type_name="float")
# ENDCLASS


class TypeBool(TypeNode):
    """
        Node that represents the 'bool' type.
    """
    def __init__(self):
        super().__init__(type_name="bool")
# ENDCLASS


class TypeChar(TypeNode):
    """
        Node that represents the 'char' type.
    """
    def __init__(self):
        super().__init__(type_name="char")
# ENDCLASS


class IdentifierNode(ASTNode):
    """
        Node that represents an identifier (without pointer stars, and not an expression).
    """
    def __init__(self, identifier):
        super().__init__(node_name="Identifier")
        self.identifier = identifier

    def getID(self):
        return self.identifier
