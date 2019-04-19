from ASTTreeNodes import *


class LLVMGeneratorExpressions:
    def __init__(self):
        self.cur_reg = 0

    def additiveExpr(self, expr):
        # add (int) or fadd (float)
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


def isConstant(node):
    return isinstance(node, ConstantExpr)

