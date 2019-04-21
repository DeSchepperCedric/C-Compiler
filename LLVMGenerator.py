from ASTTreeNodes import *


class LLVMGenerator:
    def __init__(self, symbol_table):
        self.cur_reg = 0
        self.symbol_table = symbol_table
        self.code = ""

    def getCode(self):
        return self.code

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

        elif isinstance(node, AddExpr):
            return self.arithmeticExpr(node, "add")
        elif isinstance(node, SubExpr):
            return self.arithmeticExpr(node, "sub")
        elif isinstance(node, MulExpr):
            return self.arithmeticExpr(node, "mul")
        elif isinstance(node, DivExpr):
            return self.arithmeticExpr(node, "div")
        elif isinstance(node, ModExpr):
            return self.arithmeticExpr(node, "srem")

        elif isinstance(node, EqualityExpr):
            return self.comparisonExpr(node, "eq", "eq")
        elif isinstance(node, InequalityExpr):
            return self.comparisonExpr(node, "ne", "ne")
        elif isinstance(node, CompGreater):
            return self.comparisonExpr(node, "sgt", "ogt")
        elif isinstance(node, CompLess):
            return self.comparisonExpr(node, "slt", "olt")
        elif isinstance(node, CompGreaterEqual):
            return self.comparisonExpr(node, "sge", "oge")
        elif isinstance(node, CompLessEqual):
            return self.comparisonExpr(node, "sle", "ole")

        elif isinstance(node, ReturnStatement):
            return self.returnStatement()
        elif isinstance(node, ReturnWithExprStatement):
            return self.returnWithExprStatement(node)

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
        register = self.astNodeToLLVM(node.getInitExpr())
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

    def body(self, node):
        for child in node.getChildren():
            self.code += self.astNodeToLLVM(child)

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

        return func_reg

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

    def identifierExpr(self, node):
        """
        Returns register number the indentifier is located in
        """
        identifier = node.getIdentifier()
        t, table = self.symbol_table.lookup(identifier)
        return "%" + table + "." + identifier

    def arithmeticExpr(self, node, operation):
        type_left = node.getLeft().getType()
        type_right = node.getRight().getType()

        reg_left = self.astNodeToLLVM(node.getLeft())
        reg_right = self.astNodeToLLVM(node.getRight())

        strongest_type = self.getStrongestType(type_left, type_right)

        if strongest_type == "float":
            reg_left = self.convertToFloat(reg_left, type_left)
            reg_right = self.convertToFloat(reg_right, type_right)

            self.code += "%{} = f{} float %{}, %{}\n".format(self.cur_reg, operation, reg_left, reg_right)
        else:
            reg_left = self.convertToInt(reg_left, type_left)
            reg_right = self.convertToInt(reg_right, type_right)

            self.code += "%{} = {} i32 %{}, %{}\n".format(self.cur_reg, operation, reg_left, reg_right)

        self.cur_reg += 1
        return self.cur_reg - 1

    def getStrongestType(self, a, b):
        if a == "float" or b == "float":
            return "float"
        elif a == "int" or b == "int":
            return "int"
        else:
            return "char"

    def convertToFloat(self, reg, type):
        if type == "float":
            return reg

        elif type == "char":
            self.code += "%{} = sext i8 %{} to i32\n".format(self.cur_reg, reg)
            self.code += "%{} = sitofp i32 %{} to float\n".format(self.cur_reg + 1, self.cur_reg)
            self.cur_reg += 2
            return self.cur_reg - 1
        elif type == "int":
            self.code += "%{} = sitofp i32 %{} to float\n".format(self.cur_reg, reg)
            self.cur_reg += 1
            return self.cur_reg - 1
        else:
            # what with other types?
            return reg

    def convertToInt(self, reg, type):
        if type == "int":
            return reg

        elif type == "char":
            self.code += "%{} = sext i8 %{} to i32\n".format(self.cur_reg, reg)
            self.cur_reg += 1
            return self.cur_reg - 1

        elif type == "float":
            self.code += " %{} = fptosi float %{} to i32\n".format(self.cur_reg, reg)
            self.cur_reg += 1
            return self.cur_reg - 1

        else:
            # what with other types?
            return reg

    def returnStatement(self):
        self.code += "ret void"

    def returnWithExprStatement(self, node):
        return_type = node.getType()
        register = self.astNodeToLLVM(node.getExpression())
        self.code += "ret {} %{}".format(return_type, register)

    def comparisonExpr(self, node, int_op, float_op):
        type_left = node.getLeft().getType()
        type_right = node.getRight().getType()

        reg_left = self.astNodeToLLVM(node.getLeft())
        reg_right = self.astNodeToLLVM(node.getRight())

        strongest_type = self.getStrongestType(type_left, type_right)

        if strongest_type == "float":
            reg_left = self.convertToFloat(reg_left, type_left)
            reg_right = self.convertToFloat(reg_right, type_right)

            self.code += "%{} = {} float %{}, %{}\n".format(self.cur_reg, float_op, reg_left, reg_right)
        else:
            reg_left = self.convertToInt(reg_left, type_left)
            reg_right = self.convertToInt(reg_right, type_right)

            self.code += "%{} = {} i32 %{}, %{}\n".format(self.cur_reg, int_op, reg_left, reg_right)

        self.cur_reg += 1


        #   %10 = icmp sgt i32 %8, %9
        return self.cur_reg - 1


