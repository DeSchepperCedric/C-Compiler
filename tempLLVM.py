from ASTTreeNodes import *


class LLVMGeneratorExpressions:
    def __init__(self):
        self.cur_reg = 0

    def additiveExpr(self, expr):
        code = ""
        left = ""
        right = ""
        add = ""

        if isConstant(expr.getLeft()):
            left = str(expr.getLeft().getValue)

        else:
            pass

        if isConstant(expr.getRight()):
            right = str(expr.getRight().getValue)

        else:
            pass

        code += "%{} = {} {} {}".format(self.cur_reg, add, left, right)

def astNodeToLLVM(node):
    # TODO large if/elif statement containing all the different options
    pass


def include():
    return ""


def identifier(id_):
    """
    transform IdentifierNode to llvm code string
    :param id_: identifier
    :return: LLVM string
    """
    return "%{}".format(id_.getID())


def getType(type_):
    """
    transform TypeNode to llvm code string
    :param type_: type node
    :return: LLVM string
    """

    if isinstance(type_, TypeBool):
        return "i1"
    elif isinstance(type_, TypeChar):
        # TODO how to represent chars?
        return
    elif isinstance(type_, TypeFloat):
        return "float"
    elif isinstance(type_, TypeInt):
        return "i32"
    elif isinstance(type_, TypeVoid):
        return "void"


def isConstant(node):
    return isinstance(node, ConstantExpr)

