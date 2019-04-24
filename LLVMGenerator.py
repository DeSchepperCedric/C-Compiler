from ASTTreeNodes import *
import struct as struct

class LLVMGenerator:
    def __init__(self):
        self.cur_reg = 0
        self.variable_reg = dict()
        self.reg_stack = list()

    def astNodeToLLVM(self, node):
        """
        Returns LLVM code string + register number
        Only function to call outside the class
        """

        if isinstance(node, IncludeNode):
            return self.include()

        elif isinstance(node, BoolConstantExpr):
            return self.boolConstantExpr(node)
        elif isinstance(node, FloatConstantExpr):
            return self.floatConstantExpr(node)
        elif isinstance(node, IntegerConstantExpr):
            return self.integerConstantExpr(node)

        elif isinstance(node, VarDeclDefault):
            return self.varDeclDefault(node)
        elif isinstance(node, VarDeclWithInit):
            return self.varDeclWithInit(node)
        elif isinstance(node, AssignmentExpr):
            return self.assignmentExpr(node)

        elif isinstance(node, AddressExpr):
            return self.addressExpr(node)

        elif isinstance(node, IdentifierExpr):
            return self.identifierExpr(node)

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

        elif isinstance(node, BranchStmt):
            return self.branchStatement(node)

        elif isinstance(node, ExpressionStatement):
            return self.expressionStatement(node)
        elif isinstance(node, Body):
            return self.body(node)
        elif isinstance(node, ProgramNode):
            return self.programNode(node)
        return "", self.cur_reg

    def boolConstantExpr(self, expr):
        """
        Return a constant bool with its type and the register it's stored in
        """
        code = ""
        register = self.cur_reg
        self.cur_reg += 1
        llvm_type = "i32"

        code += "%{} = alloca {}\n".format(register, llvm_type)
        code += "store {} {}, {}* %{}\n".format(llvm_type, expr.getBoolValue(), llvm_type, register)

        return code, register

    def floatConstantExpr(self, expr):
        """
        Return a constant float with its type and the register it's stored in
        """
        code = ""
        register = self.cur_reg
        self.cur_reg += 1
        llvm_type = "float"

        code += "%{} = alloca {}\n".format(register, llvm_type)
        code += "store {} {}, {}* %{}\n".format(llvm_type, self.floatToHex(expr.getFloatValue()), llvm_type, register)

        return code, register

    def integerConstantExpr(self, expr):
        """
        Return a constant integer with its type and the register it's stored in
        """
        code = ""
        register = self.cur_reg
        self.cur_reg += 1

        llvm_type = "i32"

        code += "%{} = alloca {}\n".format(register, llvm_type)
        code += "store {} {}, {}* %{}\n".format(llvm_type, expr.getIntValue(), llvm_type, register)

        return code, register

    def loadVariable(self, register, var_type, is_global):
        """

        :param register: register the variable is saved in
        :param var_type: variable type
        :param is_global: is the variable global
        :return: code, register where it's loaded to
        """
        new_reg = self.cur_reg
        self.cur_reg += 1

        glob = "@" if is_global else "%"

        return "%{} = load {}, {}* {}{} \n".format(new_reg, var_type, var_type, glob, register), new_reg

    def loadGlobalVariable(self, var_id, var_type):
        """
        Load a global variable into a scoped register
        """
        register = self.cur_reg
        self.cur_reg += 1
        return "%{} = load {}, {}* @{} \n".format(register, var_type, var_type, var_id), register

    def loadLocalVariable(self, var_id, var_type):
        """
        Load a local variable into a scoped register
        """
        register = self.cur_reg
        self.cur_reg += 1
        return "%{} = load {}, {}* %{} \n".format(register, var_type, var_type, var_id), register

    def storeVariable(self, store_to, store_from, var_type, is_global):
        glob = "@" if is_global else "%"
        return "store {} %{}, {}* {}{} \n".format(var_type, store_from, var_type, glob, store_to)

    def storeGlobalVariableFromRegister(self, var_id, var_type, register):

        return "store {} %{}, {}* @{} \n".format(var_type, register, var_type, var_id)

    def storeLocalVariableFromRegister(self, var_id, var_type, register):
        return "store {} %{}, {}* %{} \n".format(var_type, register, var_type, var_id)

    def allocate(self, register, llvm_type, is_global):
        glob = "@" if is_global else "%"
        return "{}{} = alloca {}\n".format(glob, register, llvm_type)

    def varDeclDefault(self, node):
        """
        # default initialization to 0. Might be improved later
        var_type = node.getType() + str(node.getPointerCount())
        var_id = node.getID()
        code = ""
        if node.getSymbolTable().isGlobal(var_id):
            code += "@{} = global {} 0".format(var_id, var_type)
            # code += "store {} 0, {}* @{}".format(var_type, var_type, var_id)
        else:
            t, table = node.getSymbolTable().lookup(var_id)
            reg_name = table + "." + var_id
            self.variable_reg[reg_name] = self.cur_reg
            code += "%{} = {} 0".format(self.cur_reg, var_type)
            self.cur_reg += 1

        code += "\n"
        return code
        """
        # default initialization to 0. Might be improved later
        var_type = self.getLLVMType(node.getExpressionType())
        var_id = node.getID()
        code = ""
        if node.getSymbolTable().isGlobal(var_id):
            # code += "@{} = global {} 0".format(var_id, var_type)
            code += "@{} = alloca {}\n".format(var_id, var_type)
            code += "store {} 0, {}* {}\n".format(var_type, var_id, var_type)
        else:

            t, table = node.getSymbolTable().lookup(var_id)
            reg_name = table + "." + var_id
            code += "%{} = alloca {}\n".format(var_id, var_type)
            code += "store {} 0, {}* {}\n".format(var_type, reg_name, var_type)

        code += "\n"
        return code

    def varDeclWithInit(self, node):
        expr_type = self.getLLVMType(node.getInitExpr().getExpressionType())
        var_id = node.getID()
        var_type, table = node.getSymbolTable().lookup(var_id)
        var_type = self.getLLVMType(var_type)
        code = ""

        is_global = node.getSymbolTable().isGlobal(var_id)

        if is_global and isinstance(node.getInitExpr(), ConstantExpr):
            # node.getInitExpr() should return a ConstantExpr
            code += "@{} = global {} {}".format(var_id, var_type, node.getInitExpr().getValue())

        elif is_global and isinstance(node.getInitExpr(), AddressExpr):
            target_reg = "@" + node.getInitExpr().getTargetExpr().getIdentifierName()
            code += "@{} = global {} {}".format(var_id, var_type, target_reg)

        else:
            new_code, register = self.astNodeToLLVM(node.getInitExpr())
            code += new_code

            if var_type != expr_type:
                new_code, register = self.convertToType(register, expr_type, var_type)
                code += new_code

            var_id = table + "." + var_id

            code += self.allocate(var_id, var_type, is_global)

            # otherwise type isn't correct
            if not isinstance(node.getInitExpr(), IdentifierExpr):
                load, register = self.loadVariable(register, var_type, False)

                code += load
            code += self.storeVariable(var_id, register, var_type, is_global)

        code += "\n"
        return code, -1

    def branchStatement(self, node):
        # no else statement will still generate a label
        # might be removed later
        code, register = self.astNodeToLLVM(node.getCondExpr())
        branch_if = self.cur_reg

        # we need to generate conditional code last since we need the correct register numbers
        # cond
        # code += "br i1 %{}, label %{}, label %{}\n\n".format(register, self.cur_reg, self.cur_reg + 1)
        # self.cur_reg += 2

        # if
        reg_if_label = self.cur_reg
        self.cur_reg += 1
        # code_if = "; <label>:{}:\n".format(reg_if_label)  # comment for clarity
        code_new_if, reg = self.astNodeToLLVM(node.getIfBody())
        code_if = code_new_if

        # else
        reg_else_label = self.cur_reg
        self.cur_reg += 1
        # code_else = "; <label>:{}:\n".format(reg_else_label)  # comment for clarity
        code_new_else, reg = self.astNodeToLLVM(node.getElseBody())
        code_else = code_new_else
        # cond
        cond_code = "br i1 %{}, label %{}, label %{}\n\n".format(register, reg_if_label, reg_else_label)

        code += cond_code

        code += code_if
        code += "br label %{}\n\n".format(self.cur_reg)

        code += code_else
        code += "br label %{}\n\n".format(self.cur_reg)

        code += "; <label>:{}:\n".format(self.cur_reg)
        self.cur_reg += 1


        return code, -1

    def programNode(self, node):
        code = ""
        for child in node.getChildren():
            new_code, reg = self.astNodeToLLVM(child)
            code += new_code
        return code

    def body(self, node):
        code = ""
        for child in node.getChildren():
            new_code, reg = self.astNodeToLLVM(child)
            code += new_code
        return code, -1

    def funcParam(self, node):
        # param_type = self.getLLVMType(node.getExpressionType())
        param_name = " %" + node.getParamID() if node.getParamID() is not None else ""
        param_type, table = node.getSymbolTable().lookup(node.getParamID())
        param_type = self.getLLVMType(param_type)
        #return param_type + " " + param_name
        return param_type

    def funcDecl(self, node):
        code = ""

        return_type = self.getLLVMType(node.getExpressionType())
        function_name = "@" + node.getID()

        code += "declare " + return_type + function_name + "("
        first_param = True
        for param in node.getParams():
            if not first_param:
                code += ","
            else:
                first_param = False

            code += self.funcParam(param)

        code += ")\n"
        return code, -1

    def funcDef(self, node):
        # enter new scope
        self.reg_stack.append(self.cur_reg)
        # %0 is start label
        # %1 ... are args
        self.cur_reg = 0
        code = ""
        return_type, scope = node.getSymbolTable().lookup(node.getFuncID())
        return_type = self.getLLVMType(return_type.getReturnType()) + " "
        function_name = "@" + node.getFuncID()

        code += "define " + return_type + function_name + "("
        first_param = True
        for param in node.getParamList():
            if not first_param:
                code += ","
            else:
                first_param = False

            code += self.funcParam(param)

        code += "){\n"

        # allocate and store parameters
        for param in node.getParamList():
            param_type, table = node.getSymbolTable().lookup(param.getParamID())
            param_type = self.getLLVMType(param_type)
            param_name = table + "." + param.getParamID()
            code += "%{} = alloca {}\n".format(param_name, param_type)
            code += self.storeLocalVariableFromRegister(param_name, param_type, self.cur_reg)
            self.cur_reg += 1

        # +1 since otherwise register points to code block
        self.cur_reg += 1
        new_code, reg = self.astNodeToLLVM(node.getBody())
        code += new_code

        # replace by if return_type == "void" at some point when == issue is fixed
        return_found = False
        for child in node.getBody().getChildren():
            if isinstance(child, ReturnStatement) or isinstance(child, ReturnWithExprStatement):
                return_found = True
                break

        # TODO find out why this doesn't work
        if not return_found:
            code += "ret void\n"

        code += "}\n"

        # exit scope
        self.cur_reg = self.reg_stack.pop()
        return code, -1

    def funcCallExpr(self, node):
        # "%retval = call i32 @test(i32 %argc)"
        # first load the correct variables to use as arguments

        code = ""
        first_arg = True
        arg_list = "("
        for arg in node.getArguments():
            if not first_arg:
                arg_list += ","
            else:
                first_arg = False

            arg_code, arg_reg = self.astNodeToLLVM(arg)

            code += arg_code

            arg_type = self.getLLVMType(arg.getExpressionType())
            arg_list += "{} %{}".format(arg_type, arg_reg)
        arg_list += ")"


        return_type = self.getLLVMType(node.getExpressionType())

        func_reg = self.cur_reg
        # void function result can't be assigned
        if return_type == "void":
            code += "call "
        else:
            code += "%{} = call ".format(func_reg)
            self.cur_reg += 1

        code += "{} @{}".format(return_type, node.getFunctionID().getIdentifierName())
        code += arg_list
        code += "\n"
        # store variable after call (when not void as return type)
        if not return_type == "void":
            code += self.allocate(self.cur_reg, return_type, False)
            code += self.storeVariable(self.cur_reg, func_reg, return_type, False)
            func_reg = self.cur_reg
            self.cur_reg += 1

        return code, func_reg

    def isConstant(self, node):
        return isinstance(node, ConstantExpr)

    def getLLVMType(self, type_node):
        if type_node.isVar():
            type_string = type_node.toString()

            type_string = type_string.replace("int", "i32")
            type_string = type_string.replace("bool", "i1")
            return type_string

        return ""

    def identifierExpr(self, node):
        """
        Returns register number the identifier is located in
        """
        identifier = node.getIdentifierName()

        var_type = self.getLLVMType(node.getExpressionType())

        if node.getSymbolTable().isGlobal(identifier):
            return self.loadVariable(identifier, var_type, True)
        else:
            t, table = node.getSymbolTable().lookup(identifier)
            var_name = table + "." + identifier
            return self.loadVariable(var_name, var_type, False)

    def arithmeticExpr(self, node, operation):
        code = ""

        type_left = self.getLLVMType(node.getLeft().getExpressionType())
        type_right = self.getLLVMType(node.getRight().getExpressionType())

        code_left, reg_left = self.astNodeToLLVM(node.getLeft())

        # extra load not necessary when dealing with Identifiers
        if not isinstance(node.getLeft(), IdentifierExpr):
            load, reg_left = self.loadVariable(reg_left, type_left, False)

            code_left += load

        code_right, reg_right = self.astNodeToLLVM(node.getRight())

        if not isinstance(node.getRight(), IdentifierExpr):
            load, reg_right = self.loadVariable(reg_right, type_right, False)

            code_right += load

        code += code_left
        code += code_right

        strongest_type = self.getStrongestType(type_left, type_right)
        llvm_type = ""
        if strongest_type == "float":
            code_left, reg_left = self.convertToFloat(reg_left, type_left)
            code_right, reg_right = self.convertToFloat(reg_right, type_right)

            code += code_left
            code += code_right
            code += "%{} = f{} float %{}, %{}\n".format(self.cur_reg, operation, reg_left, reg_right)
            llvm_type = "float"

        else:
            code_left, reg_left = self.convertToInt(reg_left, type_left)
            code_right, reg_right = self.convertToInt(reg_right, type_right)

            code += code_left
            code += code_right
            code += "%{} = {} i32 %{}, %{}\n".format(self.cur_reg, operation, reg_left, reg_right)
            llvm_type = "i32"

        self.cur_reg += 1
        code += self.allocate(self.cur_reg, llvm_type, False)
        code += self.storeVariable(self.cur_reg, self.cur_reg - 1, llvm_type, False)

        self.cur_reg += 1

        return code, self.cur_reg - 1

    def getStrongestType(self, a, b):
        if a == "float" or b == "float":
            return "float"
        elif a == "int" or b == "int":
            return "int"
        else:
            return "char"

    def convertToFloat(self, reg, type):
        code = ""
        if "float" in type:
            return code, reg

        elif "char" in type:
            code += "%{} = sext i8 %{} to i32\n".format(self.cur_reg, reg)
            code += "%{} = sitofp i32 %{} to float\n".format(self.cur_reg + 1, self.cur_reg)
            self.cur_reg += 2
            return code, self.cur_reg - 1
        elif "int" in type or "i32" in type:
            code += "%{} = sitofp i32 %{} to float\n".format(self.cur_reg, reg)
            self.cur_reg += 1
            return code, self.cur_reg - 1
        else:
            # what with other types?
            return code, reg

    def convertToInt(self, reg, type):
        code = ""
        if "int" in type or "i32" in type:
            return code, reg

        elif "char" in type:
            code += "%{} = sext i8 %{} to i32\n".format(self.cur_reg, reg)
            self.cur_reg += 1
            return code, self.cur_reg - 1

        elif "float" in type:
            code += " %{} = fptosi float %{} to i32\n".format(self.cur_reg, reg)
            self.cur_reg += 1
            return code, self.cur_reg - 1

        else:
            # what with other types?
            return code, reg

    def convertToType(self, reg, old_type, new_type):
        if "int" in new_type or "i32" in new_type:
            return self.convertToInt(reg, old_type)

        elif "float" in new_type:
            return self.convertToFloat(reg, old_type)

    def returnStatement(self):
        return "ret void\n", -1

    def returnWithExprStatement(self, node):

        return_type = self.getLLVMType(node.getExpression().getExpressionType())
        code, register = self.astNodeToLLVM(node.getExpression())

        if not isinstance(node.getExpression(), IdentifierExpr):
            new_code, register = self.loadVariable(register, return_type, False)
            code += new_code
        code += "ret {} %{}\n".format(return_type, register)
        return code, -1

    def comparisonExpr(self, node, int_op, float_op):
        code = ""

        type_left = self.getLLVMType(node.getLeft().getExpressionType())

        type_right = self.getLLVMType(node.getRight().getExpressionType())

        code_left, reg_left = self.astNodeToLLVM(node.getLeft())

        if not isinstance(node.getLeft(), IdentifierExpr):
            load, reg_left = self.loadVariable(reg_left, type_left, False)

            code_left += load

        code_right, reg_right = self.astNodeToLLVM(node.getRight())

        if not isinstance(node.getRight(), IdentifierExpr):
            load, reg_right = self.loadVariable(reg_right, type_right, False)

            code_right += load

        code += code_left
        code += code_right

        strongest_type = self.getStrongestType(type_left, type_right)

        if strongest_type == "float":
            code_left, reg_left = self.convertToFloat(reg_left, type_left)
            code_right, reg_right = self.convertToFloat(reg_right, type_right)

            code += code_left
            code += code_right
            code += "%{} = icmp {} float %{}, %{}\n".format(self.cur_reg, float_op, reg_left, reg_right)
        else:
            code_left, reg_left = self.convertToInt(reg_left, type_left)
            code_right, reg_right = self.convertToInt(reg_right, type_right)

            code += code_left
            code += code_right
            code += "%{} = icmp {} i32 %{}, %{}\n".format(self.cur_reg, int_op, reg_left, reg_right)

        self.cur_reg += 1

        return code, self.cur_reg - 1

    def include(self):
        code = "declare i32 @printf(i8*, ...) nounwind \n"
        code += "declare i32 @scanf(i8*, ...) nounwind \n"
        return code, -1

    def assignmentExpr(self, node):
        code, register = self.astNodeToLLVM(node.getRight())
        right_type = self.getLLVMType(node.getRight().getExpressionType())
        left_type = self.getLLVMType(node.getLeft().getExpressionType())
        identifier = node.getLeft().getIdentifierName()

        if not isinstance(node.getRight(), IdentifierExpr):
            load, register = self.loadVariable(register, right_type, False)

            code += load

        if right_type == left_type:
            pass
        elif left_type == "int":
            convert, register = self.convertToInt(register, right_type)
            code += convert
        elif left_type == "float":
            convert, register = self.convertToFloat(register, right_type)
            code += convert

        if node.getSymbolTable().isGlobal(identifier):
            code += self.storeGlobalVariableFromRegister(identifier, left_type, register)
        else:
            t, table = node.getSymbolTable().lookup(identifier)
            identifier = table + "." + identifier
            code += self.storeLocalVariableFromRegister(identifier, left_type, register)

        return code, -1

    def expressionStatement(self, node):
        return self.astNodeToLLVM(node.getExpression())

    def floatToHex(self, f):
        """convert float to hex (needed in llvm)"""
        single_precision_rep = struct.pack('>f', f)
        single_precision_val = struct.unpack(">f", single_precision_rep)[0]
        double_val = struct.pack('>d', single_precision_val)
        double_hex = "0x" + double_val.hex()
        return double_hex

    def addressExpr(self, node):

        # %1 = alloca i32*, align 8
        code, target_reg = self.astNodeToLLVM(node.getTargetExpr())
        expr_type = self.getLLVMType(node.getTargetExpr().getExpressionType())

        register = self.cur_reg
        self.cur_reg += 1
        code += self.allocate(register, expr_type, False)
        code += self.storeVariable(register, target_reg, expr_type, False)

        expr_type += "*"

        code += self.allocate(self.cur_reg, expr_type, False)
        code += self.storeVariable(self.cur_reg, register, expr_type, False)

        self.cur_reg += 1
        return code, self.cur_reg - 1





