from ASTTreeNodes import *


class LLVMGenerator:
    def __init__(self, symbol_table):
        self.cur_reg = 0
        self.symbol_table = symbol_table

    def boolConstantExpr(self, expr):
        """
        Return a constant bool with its type and the register it's stored in
        """
        register = self.cur_reg
        self.cur_reg += 1
        code = "%{} = i1 {} \n".format(register, expr.getBoolValue())

        return code, register

    def floatConstantExpr(self, expr):
        """
        Return a constant float with its type and the register it's stored in
        """
        register = self.cur_reg
        self.cur_reg += 1
        code = "%{} = float {} \n".format(register, expr.getFloatValue())

        return code, register

    def integerConstantExpr(self, expr):
        """
        Return a constant integer with its type and the register it's stored in
        """
        register = self.cur_reg
        self.cur_reg += 1
        code = "%{} = i32 {} \n".format(register, expr.getIntValue())

        return code, register

    def loadGlobalVariableInto(self, var_id, var_type):
        """
        Load a global variable into a scoped register
        """
        register = self.cur_reg
        self.cur_reg += 1
        return "%{} = load {}, {}* @{} \n".format(register, var_type, var_type, var_id), register

    def storeGlobalVariableFromRegister(self, var_id, var_type):
        register = self.cur_reg
        self.cur_reg += 1
        return "store {} %{}, {}* @{} \n".format(var_type, register, var_type, var_id)

    def varDeclDefault(self, decl):
        # default initialization to 0. Might be improved later
        var_type = decl.getType() + str(decl.getPointerCount())
        var_id = decl.getID()
        code = ""

        if self.symbol_table.isGlobal(var_id):

            code += "store {} 0, {}* @{}".format(var_type, var_type, var_id)
        else:
            code += "%{} = {} 0".format(var_id, var_type)

        code += "\n"
        return code

    def varDeclWithInit(self, decl):
        var_type = decl.getType() + str(decl.getPointerCount())
        var_id = decl.getID()
        register = self.cur_reg
        self.cur_reg += 1
        code, register = self.astNodeToLLVM(decl.getInitExpr(), register)
        if self.symbol_table.isGlobal(var_id):
            code += self.storeGlobalVariableFromRegister(var_id, var_type)
        else:
            code += "%{} = {} %{}".format(var_id, var_type, register)

        code += "\n"
        return code

    def branchStatement(self, stat):
        # WIP
        code, register = self.astNodeToLLVM(stat.getCondExpr())
        code = "br i1 %{}, label %{}, label %{}".format(register, register + 1, register + 2)
        # add code blocks

    def programNode(self, node):
        code = ""
        for child in node.getChildren():
            code += self.astNodeToLLVM(child)

        return code

    def body(self, node):
        code = ""
        for child in node.getChildren():
            code += self.astNodeToLLVM(child)

        return code

    def funcParam(self, node):
        param_type = self.getLLVMType(node.getParamType()) + node.getPointerCount() * "*"
        param_name = " %" + node.getParamID() if node.getParamID() is not None else ""
        return param_type + param_name

    def funcDecl(self, node):
        return_type = node.getType() + node.getPointerCount() * "*"
        function_name = "@" + node.getID()

        code = "declare " + return_type + function_name + "("
        first_param = True
        for param in node.getParams():
            if not first_param:
                code += ","
            else:
                first_param = False

            code += self.funcParam(param)

        code += ")\n"
        return code

    def funcDef(self, node):
        return_type = node.getReturnType() + node.getPointerCount() * "*"
        function_name = "@" + node.getFuncID()

        code = "define " + return_type + function_name + "("
        first_param = True
        for param in node.getParamList():
            if not first_param:
                code += ","
            else:
                first_param = False

            code += self.funcParam(param)

        code += "){\n"
        code += self.astNodeToLLVM(node.getBody())
        code += "}\n"
        return code

    def astNodeToLLVM(self, node):
        """
        Returns LLVM code string + register number
        """
        # TODO large if/elif statement containing all the different options
        if isinstance(node, BoolConstantExpr):
            return self.boolConstantExpr(node)
        elif isinstance(node, FloatConstantExpr):
            return self.floatConstantExpr(node)
        elif isinstance(node, IntegerConstantExpr):
            return self.integerConstantExpr(node)

        elif isinstance(node, VarDeclDefault):
            return self.varDeclDefault(node)
        elif isinstance(node, VarDeclWithInit):
            return self.varDeclWithInit(node)

        elif isinstance(node, FuncParam):
            return self.funcParam(node)

        elif isinstance(node, Body):
            return self.body(node)
        elif isinstance(node, ProgramNode):
            return self.programNode(node)
        return "", self.cur_reg

    def isConstant(self, node):
        return isinstance(node, ConstantExpr)

    def getLLVMType(self, type):
        # TODO add char/string
        if type == "float":
            return "float"
        elif type == "int":
            return "i32"
        elif type == "bool":
            return "i1"
        return ""
