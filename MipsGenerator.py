from ASTTreeNodes import *
import struct as struct
from itertools import zip_longest


class MipsGenerator:
    def __init__(self):
        self.cur_reg = 0
        self.variable_reg = dict()
        self.reg_stack = list()
        self.global_scope_string = ""
        self.string_counter = 0
        self.reg_to_string = dict()
        self.array_sizes = dict()

    def astNodeToLLVM(self, node):
        """
        Returns LLVM code string + register number
        Only function to call outside the class
        """
        if isinstance(node, IncludeNode):
            pass

        elif isinstance(node, BoolConstantExpr):
            return self.boolConstantExpr(node)
        elif isinstance(node, FloatConstantExpr):
            return self.floatConstantExpr(node)
        elif isinstance(node, IntegerConstantExpr):
            return self.integerConstantExpr(node)
        elif isinstance(node, CharConstantExpr):
            return self.charConstantExpr(node)
        elif isinstance(node, BoolConstantExpr):
            return self.boolConstantExpr(node)
        elif isinstance(node, StringConstantExpr):
            return self.stringConstantExpr(node)

        elif isinstance(node, VarDeclDefault):
            return self.varDeclDefault(node)
        elif isinstance(node, VarDeclWithInit):
            return self.varDeclWithInit(node)
        elif isinstance(node, ArrayDecl):
            return self.arrayDecl(node)
        elif isinstance(node, AssignmentExpr):
            return self.assignmentExpr(node)

        elif isinstance(node, AddressExpr):
            return self.addressExpr(node)
        elif isinstance(node, PointerDerefExpr):
            return self.pointerDerefExpr(node)

        elif isinstance(node, IdentifierExpr):
            return self.identifierExpr(node)
        elif isinstance(node, ArrayAccessExpr):
            return self.arrayElementAccess(node)
        elif isinstance(node, CastExpr):
            return self.castExpr(node)

        elif isinstance(node, FuncParam):
            return self.funcParam(node)
        elif isinstance(node, FuncDecl):
            return self.funcDecl(node)
        elif isinstance(node, FuncDef):
            return self.funcDef(node)
        elif isinstance(node, FuncCallExpr):
            return self.funcCallExpr(node)

        elif isinstance(node, AddExpr):
            return self.arithmeticExpr(node, "add")
        elif isinstance(node, SubExpr):
            return self.arithmeticExpr(node, "sub")
        elif isinstance(node, MulExpr):
            return self.arithmeticExpr(node, "mul")
        elif isinstance(node, DivExpr):
            return self.arithmeticExpr(node, "div")
        elif isinstance(node, ModExpr):
            #  no mod operation
            # see https://stackoverflow.com/questions/21695333/how-do-i-correctly-use-the-mod-operator-in-mips
            # return self.arithmeticExpr(node, "srem")
            pass

        elif isinstance(node, PrefixIncExpr):
            return self.prefixArithmetics(node, "add")
        elif isinstance(node, PrefixDecExpr):
            return self.prefixArithmetics(node, "sub")
        elif isinstance(node, PostfixIncExpr):
            return self.postfixArithmetics(node, "add")
        elif isinstance(node, PostfixDecExpr):
            return self.postfixArithmetics(node, "sub")

        # format here is (node, int-op, float-op)
        elif isinstance(node, EqualityExpr):
            return self.comparisonExpr(node, "eq")
        elif isinstance(node, InequalityExpr):
            return self.comparisonExpr(node, "ne")
        elif isinstance(node, CompGreater):
            return self.comparisonExpr(node, "gt")
        elif isinstance(node, CompLess):
            return self.comparisonExpr(node, "lt")
        elif isinstance(node, CompGreaterEqual):
            return self.comparisonExpr(node, "ge")
        elif isinstance(node, CompLessEqual):
            return self.comparisonExpr(node, "le")

        elif isinstance(node, ReturnStatement):
            return self.returnStatement()
        elif isinstance(node, ReturnWithExprStatement):
            return self.returnWithExprStatement(node)

        elif isinstance(node, BranchStmt):
            return self.branchStatement(node)
        elif isinstance(node, WhileStmt):
            return self.whileStatement(node)

        elif isinstance(node, ExpressionStatement):
            return self.expressionStatement(node)
        elif isinstance(node, StatementContainer):  # Body & CompoundStmt
            return self.statementContainer(node)
        elif isinstance(node, ProgramNode):
            return self.programNode(node)

        raise Exception("Encountered unknown AST node of type '{}'.\n This node has no support yet.".format(type(node)))

    def boolConstantExpr(self, expr):
        """
        Return a constant bool with its type and the register it's stored in
        """
        pass

    def floatConstantExpr(self, expr):
        """
        Return a constant float with its type and the register it's stored in
        """
        pass

    def integerConstantExpr(self, expr):
        """
        Return a constant integer with its type and the register it's stored in
        """
        pass

    def charConstantExpr(self, expr):
        """
        Return a constant integer with its type and the register it's stored in
        """
        pass

    def stringConstantExpr(self, expr):
        pass

    def loadVariable(self, register, var_type, is_global):
        """

        :param register: register the variable is saved in
        :param var_type: variable type
        :param is_global: is the variable global
        :return: code, register where it's loaded to
        """
        pass

    def loadGlobalVariable(self, var_id, var_type):
        """
        Load a global variable into a scoped register
        """
        pass

    def loadLocalVariable(self, var_id, var_type):
        """
        Load a local variable into a scoped register
        """
        pass

    def storeVariable(self, store_to, store_from, var_type, is_global):
        pass

    def allocate(self, register, llvm_type, is_global):
        pass

    def varDeclDefault(self, node):
        pass

    def varDeclWithInit(self, node):
        pass

    def branchStatement(self, node):
        pass

    def whileStatement(self, node):
        pass

    def programNode(self, node):
        pass

    def statementContainer(self, node):
        pass

    def funcParam(self, node):
        pass

    def funcDecl(self, node):
        pass

    def funcDef(self, node):
        pass

    def funcCallExpr(self, node):
        pass

    def identifierExpr(self, node):
        pass

    def arithmeticExpr(self, node, operation):
        # dest = src1 op src2
        # op dest, src, src2
        # int -> op
        # float ->  op + ".s"
        pass

    def getStrongestType(self, a, b):
        INTREP = ["int", "i32"]
        CHARREP = ["char", "i8"]
        BOOLREP = ["bool", "i1"]

        if a == "float" or b == "float":
            return "float"
        elif a in INTREP or b in INTREP:
            return "int"
        elif a in CHARREP or b in CHARREP:
            return "char"
        elif a in BOOLREP or b in BOOLREP:
            return "bool"
        else:
            raise Exception("Invalid call to getStrongestType for '{}' and '{}'".format(a, b))

    def convertToFloat(self, reg, type):
        pass

    def convertToInt(self, reg, type):
        pass

    def convertToDouble(self, reg, from_type):
        pass

    def convertToChar(self, reg, from_type):
        pass

    def convertToBool(self, reg, from_type):
        pass

    def convertToType(self, reg, old_type, new_type):
        pass

    def convertConstant(self, new_type, old_type, value):
        pass

    def returnStatement(self):
        pass

    def returnWithExprStatement(self, node):
        pass

    def comparisonExpr(self, node, int_op):
        # cond = (src1 op src2)
        # op src, src2
        # int -> op
        # float ->  "c." + op + ".s"
        pass

    def assignmentExpr(self, node):
        pass

    def expressionStatement(self, node):
        pass

    def addressExpr(self, node):
        pass

    def pointerDerefExpr(self, node):
        pass

    def addStringToGlobal(self, string):
        pass

    def storeString(self, string_reg, reg_to):
        pass

    def arrayDecl(self, node):
        pass

    def arrayAccessHelperString(self, reg_to, reg_from, element_type, index, is_global):
        pass

    def arrayElementAssignment(self, node):
        pass

    def arrayElementAccess(self, node):
        pass

    def castExpr(self, node):
        pass

    def prefixArithmetics(self, node, operation):
        pass

    def postfixArithmetics(self, node, operation):
        pass
