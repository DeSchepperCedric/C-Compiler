
class ASTNode:
    """
        Class that represents a node in an AST tree.
    """

    def __init__(self):
        self.parent = None
        self.children = []
    # ENDCTOR

    def getParent(self):
        return self.parent
    # ENDMETHOD

    def getChildren(self):
        return self.children
    # ENDMETHOD
# ENDCLASS

class ASTProgramNode:
    # LIST of includeNode, funcdecl, vardecl
    pass

class IncludeNode:
    # no members, will always be "#include <stdio.h>"
    pass

class FuncDecl:
    # type
    # IdWithPtr
    # LIST of Param
    pass

class VarDecl:
    # type
    # IdWithPtr
    pass

class ArrayVarDecl(VarDecl):
    # size expr
    pass

class VarDeclWithInit(VarDecl):
    # init_expr
    pass

class FuncDef:
    # type
    # IdWithPtr
    # LIST of Param
    # body: LIST of Statement
    # NOTE: alles na "return" statement moet weg!
    pass

class IdWithPtr:
    # id: IdentifierExpr
    # pointer-count: string
    pass

class FuncParam:
    # type
    # IdWithPtr
    pass

class Statement:
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







