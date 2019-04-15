
class ASTNode:
    """
        Base class for all nodes in AST Trees.
    """
    def __init(self, parent, node_name):
        self.parent = parent
        self.node_name = node_name

    def getParent(self):
        return parent

    def getName(self):
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


class VarDecl(ASTNode):
    """
        Base class for variable declaration nodes.
    """
    def __init__(self, node_name, var_type, var_id):
        super().__init__(node_name=node_name)
        self.type = var_type
        self.id = identifier_with_ptr

    def getType(self):
        return self.type

    def getID(self):
        return self.id
# ENDCLASS
        

class ArrayDecl(VarDecl):
    """
        Node that represents an array declaration: "type id[size_expr];"
    """

    def __init__(self, array_type, array_id, size_expr):
        super().__init__(node_name="ArrayDecl",
                         var_type = array_type,
                         var_id = array_id)
        self.size_expr = size_exp

    def getSizeExp(self):
        return self.size_expr
# ENDCLASS


class VarDelcDefault(VarDecl):
    """
        Node that represents a variable declaration without initializer: "type id;"
    """
    def __init__(self, var_type, var_id):
        super().__init__(node_name="VarDeclDefault",
                         var_type=var_type,
                         var_id=var_id)
# ENDCLASS


class VarDeclWithInit(VarDecl):
    """
        Node that represents a variabele declaration with initializer: "type id = init_expr;"
    """

    def __init__(self, var_type, var_id, init_expr):
        super().__init__(node_name="VarDeclInit",
                         var_type=var_type,
                         var_id=var_id)
        self.init_expr = init_expr

    def getInitExpr(self):
        return self.init_expr
# ENDCLASS


class FuncDef(ASTNode):
    # type
    # IdWithPtr
    # LIST of Param
    # body: LIST of Statement
    # NOTE: alles na "return" statement moet weg!
    pass

class IdWithPtr(ASTNode):
    # id: IdentifierExpr
    # pointer-count: string
    pass

class FuncParam(ASTNode):
    # type
    # IdWithPtr
    pass

class Statement(ASTNode):
    # base class for statements
    pass

class CompoundStmt(Statement):
    # LIST of Statement
    pass

class WhileStmt(Statement):
    # condition: expr
    # body: LIST of Statement
    # NOTE: alles na "continue" of "break" weg.
    pass

class ForStmt(Statement):
    # init
    # condition
    # iter
    # body: LIST of Statement
    # NOTE: alles na "continue" of "break" weg.
    pass

class BranchStmt(Statement):
    # conditon
    # if-branch
    # else-branch
    pass

class ExpressionStatement(Statement):
    # expression: can be empty
    pass

class Expression:
    # base class for all expression
    pass

class AssignmentExpr(Expression):
    # left
    # right
    # operator: {'=', '+=', '-=', '*=', '/='
    pass

class LogicBinExpr(Expression):
    # left
    # right
    # operator: {'&&', '||'}
    pass

class EqualityExpr(Expression):
    # left
    # right
    # operator: {'==', '!='}
    pass

class ComparisonExpr(Expression):
    # left
    # right
    # operator: {'<', '>', '<=', '>='}
    pass

class AdditiveExpr(Expression):
    # left
    # right
    # operator: {'+', '-'}
    pass

class MultiplicativeExpr(Expression):
    # left
    # right
    # operator: {'*', '/', '%'}
    pass

class CastExpr(Expression):
    # list of types
    # expr
    pass

class LogicNotExpr(Expression):
    # expr
    pass

class PrefixIncDecExpr(Expression):
    # ++x, --x
    # op: {'++', '--'}
    # expr
    pass

class PostfixIncDecExpr(Expression):
    # x++, x--
    # expr
    # op: {'++', '--'}
    pass

class PlusMinPrefixExpr(Expression):
    # +x, -x
    # op: {'+', '-'}
    # expr
    pass

class ArrayAccessExpr(Expression):
    # target: expression
    # index: expression
    pass

class PointerDerefExpr(Expression):
    # *x
    # expr
    pass

class FuncCallExpr(Expression):
    # functionname
    # List of Expression: parameters
    pass

class IdentifierExpr(Expression):
    # identifier
    pass

class ConstantExpr(Expression):
    # base class for constants
    pass

class IntegerConstant(ConstantExpr):
    pass

class FloatConstant(ConstantExpr):
    pass

class StringConstant(ConstantExpr):
    pass

class CharConstant(ConstantExpr):
    pass

class BoolConstant(ConstantExpr):
    pass







