from ASTTreeNodes import *


class LLVMGenerator:
    def __init__(self, symbol_table):
        self.cur_reg = 0
        self.symbol_table = symbol_table
        self.code = ""

    def astNodeToLLVM(self, node):
        """
        Returns LLVM code string + register number
        Only function to call outside the class
        """
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
        elif isinstance(node, FuncDecl):
            return self.funcDecl(node)
        elif isinstance(node, FuncDef):
            return self.funcDef(node)

        elif isinstance(node, Body):
            return self.body(node)
        elif isinstance(node, ProgramNode):
            return self.programNode(node)
        return self.cur_reg

    def boolConstantExpr(self, expr):
        """
        Return a constant bool with its type and the register it's stored in
        """
        register = self.cur_reg
        self.cur_reg += 1
        self.code += "%{} = i1 {} \n".format(register, expr.getBoolValue())

        return register

    def floatConstantExpr(self, expr):
        """
        Return a constant float with its type and the register it's stored in
        """
        register = self.cur_reg
        self.cur_reg += 1
        self.code += "%{} = float {} \n".format(register, expr.getFloatValue())

        return register

    def integerConstantExpr(self, expr):
        """
        Return a constant integer with its type and the register it's stored in
        """
        register = self.cur_reg
        self.cur_reg += 1
        self.code += "%{} = i32 {} \n".format(register, expr.getIntValue())

        return register

    def loadGlobalVariable(self, var_id, var_type):
        """
        Load a global variable into a scoped register
        """
        register = self.cur_reg
        self.cur_reg += 1
        return "%{} = load {}, {}* @{} \n".format(register, var_type, var_type, var_id), register

    def storeGlobalVariableFromRegister(self, var_id, var_type, register):
        self.code += "store {} %{}, {}* @{} \n".format(var_type, register, var_type, var_id)

    def varDeclDefault(self, node):
        # default initialization to 0. Might be improved later
        var_type = node.getType() + str(node.getPointerCount())
        var_id = node.getID()

        if self.symbol_table.isGlobal(var_id):
            self.code += "@{} = global {} 0".format(var_id, var_type)
            # self.code += "store {} 0, {}* @{}".format(var_type, var_type, var_id)
        else:
            t, table = self.symbol_table.lookup(var_id)
            reg_name = table + "." + var_id
            self.code += "%{} = {} 0".format(reg_name, var_type)

        self.code += "\n"
        return

    def varDeclWithInit(self, node):
        var_type = node.getType() + str(node.getPointerCount())
        var_id = node.getID()
        self.code, register = self.astNodeToLLVM(node.getInitExpr())
        if self.symbol_table.isGlobal(var_id):
            self.code += self.storeGlobalVariableFromRegister(var_id, var_type, register)
        else:
            t, table = self.symbol_table.lookup(var_id)
            reg_name = table + "." + var_id
            self.code += "%{} = {} %{}".format(reg_name, var_type, register)

        self.code += "\n"
        return

    def branchStatement(self, node):
        # WIP
        register = self.astNodeToLLVM(node.getCondExpr())
        self.code += "br i1 %{}, label %{}, label %{}".format(register, register + 1, register + 2)
        # add self.code blocks

    def programNode(self, node):
        for child in node.getChildren():
            self.code += self.astNodeToLLVM(child)

        return self.code

    def body(self, node):
        for child in node.getChildren():
            self.code += self.astNodeToLLVM(child)

        return self.code

    def funcParam(self, node):
        param_type = self.getLLVMType(node.getParamType()) + node.getPointerCount() * "*"
        param_name = " %" + node.getParamID() if node.getParamID() is not None else ""
        return param_type + param_name

    def funcDecl(self, node):
        return_type = node.getType() + node.getPointerCount() * "*"
        function_name = "@" + node.getID()

        self.code += "declare " + return_type + function_name + "("
        first_param = True
        for param in node.getParams():
            if not first_param:
                self.code += ","
            else:
                first_param = False

            self.code += self.funcParam(param)

        self.code += ")\n"
        return self.code

    def funcDef(self, node):
        return_type = node.getReturnType() + node.getPointerCount() * "*"
        function_name = "@" + node.getFuncID()

        self.code += "define " + return_type + function_name + "("
        first_param = True
        for param in node.getParamList():
            if not first_param:
                self.code += ","
            else:
                first_param = False

            self.code += self.funcParam(param)

        self.code += "){\n"
        self.code += self.astNodeToLLVM(node.getBody())
        self.code += "}\n"
        return

    def funcCallExpr(self, node):
        # "%retval = call i32 @test(i32 %argc)"
        # first load the correct variables to use as arguments
        first_arg = True
        arg_list = "("
        for arg in node.getArguments():
            if not first_arg:
                arg_list += ","
            else:
                first_arg = False
            arg_code, arg_reg = self.astNodeToLLVM(arg)
            self.code += arg_code

            arg_type = self.getLLVMType(arg.getType())
            arg_list += "{} %{}".format(arg_type, arg_reg)
        arg_list += ")"

        func_reg = self.cur_reg
        self.cur_reg += 1
        self.code += "%{} = call ".format(func_reg)

        return_type = node.getType()
        self.code += "{} @{}".format(return_type, node.getFunctionID())
        self.code += arg_list
        self.code += "\n"

        return self.code, func_reg

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

    def identifierExpr(self, expr):
        """
        Returns register number the indentifier is located in
        """
        identifier = expr.getIdentifier()
        t, table = self.symbol_table.lookup(identifier)
        return "%" + table + "." + identifier
