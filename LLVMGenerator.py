from ASTTreeNodes import *
import struct as struct
from itertools import zip_longest


class LLVMGenerator:
    def __init__(self):
        self.cur_reg = 0
        self.variable_reg = dict()
        self.reg_stack = list()
        self.global_scope_string = ""
        self.string_to_regs = dict()
        self.reg_to_string = dict()

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
            return self.arithmeticExpr(node, "sdiv")
        elif isinstance(node, ModExpr):
            return self.arithmeticExpr(node, "srem")

        # format here is (node, int-op, float-op)
        elif isinstance(node, EqualityExpr):
            return self.comparisonExpr(node, "eq", "oeq")
        elif isinstance(node, InequalityExpr):
            return self.comparisonExpr(node, "ne", "one")
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
        elif isinstance(node, WhileStmt):
            return self.whileStatement(node)

        elif isinstance(node, ExpressionStatement):
            return self.expressionStatement(node)
        elif isinstance(node, Body):
            return self.body(node)
        elif isinstance(node, ProgramNode):
            return self.programNode(node)

        raise Exception("Encountered unknown AST node of type '{}'".format(type(node)))

        return "", -1

    def boolConstantExpr(self, expr):
        """
        Return a constant bool with its type and the register it's stored in
        """
        code = ""
        register = self.cur_reg
        self.cur_reg += 1
        llvm_type = "i1"
        value = 1 if expr.getBoolValue() == True else 0
        code += "%{} = alloca {}\n".format(register, llvm_type)
        code += "store {} {}, {}* %{}\n".format(llvm_type, value, llvm_type, register)

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

    def charConstantExpr(self, expr):
        """
        Return a constant integer with its type and the register it's stored in
        """
        register = self.cur_reg
        self.cur_reg += 1

        llvm_type = "i8"

        code = "%{} = alloca {}\n".format(register, llvm_type)
        code += "store {} {}, {}* %{}\n".format(llvm_type, ord(expr.getCharValue()[1]), llvm_type, register)

        return code, register

    def stringConstantExpr(self, expr):
        register = self.cur_reg
        self.cur_reg += 1

        string_reg = self.addStringToGlobal(expr.getStrValue())
        llvm_type = "i8*"

        code = "%{} = alloca {}\n".format(register, llvm_type)
        code += self.storeString(string_reg, register)
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

        return "%{} = load {}, {}* {}{}\n".format(new_reg, var_type, var_type, glob, register), new_reg

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
        return "store {} %{}, {}* {}{}\n".format(var_type, store_from, var_type, glob, store_to)

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
        var_id = node.getID()
        var_type, t = node.getSymbolTable().lookup(var_id)
        var_type = self.getLLVMType(var_type)
        value = 0 if "float" not in var_type else self.floatToHex(0.0)

        is_pointer = True if "*" in var_type else False

        value = value if not is_pointer else "null"
        code = ""
        if node.getSymbolTable().isGlobal(var_id):

            code += "@{} = global {} {}".format(var_id, var_type, value)

            # code += "@{} = alloca {}\n".format(var_id, var_type)
            # code += "store {} {}, {}* {}\n".format(var_type, value, var_id, var_type)
        else:

            t, table = node.getSymbolTable().lookup(var_id)
            reg_name = table + "." + var_id
            code += "%{} = alloca {}\n".format(reg_name, var_type)
            code += "store {} {}, {}* %{}\n".format(var_type, value, var_type, reg_name)

        code += "\n"
        return code, -1

    def varDeclWithInit(self, node):
        expr_type = self.getLLVMType(node.getInitExpr().getExpressionType())
        var_id = node.getID()
        var_type, table = node.getSymbolTable().lookup(var_id)
        var_type = self.getLLVMType(var_type)
        code = ""
        is_global = node.getSymbolTable().isGlobal(var_id)

        if is_global and isinstance(node.getInitExpr(), ConstantExpr):
            # node.getInitExpr() should return a ConstantExpr
            value = self.convertConstant(var_type, expr_type, node.getInitExpr().getValue())
            code += "@{} = global {} {}".format(var_id, var_type, value)

        elif is_global and isinstance(node.getInitExpr(), AddressExpr):
            target_reg = "@" + node.getInitExpr().getTargetExpr().getIdentifierName()
            code += "@{} = global {} {}".format(var_id, var_type, target_reg)

        else:

            new_code, register = self.astNodeToLLVM(node.getInitExpr())
            code += new_code

            if var_type != expr_type and isinstance(node.getInitExpr(), IdentifierExpr):
                convert, register = self.convertToType(register, expr_type, var_type)
                code += convert
            # more loads/stores to fix type
            elif var_type != expr_type:
                load, register = self.loadVariable(register, expr_type, is_global)
                code += load
                convert, register = self.convertToType(register, expr_type, var_type)
                code += convert
                code += self.allocate(self.cur_reg, var_type, is_global)
                store = self.storeVariable(self.cur_reg, register, var_type, is_global)
                register = self.cur_reg
                self.cur_reg += 1
                code += store

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
        """
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
        """

        # no else statement will still generate a label
        # might be removed later
        code, register = self.astNodeToLLVM(node.getCondExpr())
        load, register = self.loadVariable(register, "i1", False)
        code += load
        code += "br i1 %{}, label %if.{}, label %else.{}\n".format(register, register, register)

        # if
        code_if, reg = self.astNodeToLLVM(node.getIfBody())

        code += "\nif.{}:\n".format(register)
        code += code_if
        code += "br label %end.{}\n".format(register)
        if "\nret" in code_if:
            self.cur_reg += 1

        code_else, reg = self.astNodeToLLVM(node.getElseBody())
        code += "\nelse.{}:\n".format(register)
        code += code_else
        code += "br label %end.{}\n".format(register)
        if "\nret" in code_else:
            self.cur_reg += 1

        code += "\nend.{}:\n".format(register)
        # self.cur_reg += 1

        return code, -1

    def whileStatement(self, node):
        code_cond, register = self.astNodeToLLVM(node.getCondExpr())

        # while(variable)
        if not isinstance(node.getCondExpr(), IdentifierExpr):
            load, register = self.loadVariable(register, "i1", False)
            code_cond += load

        code = "br label %cond.{}\n".format(register)
        code += "\ncond.{}:\n".format(register)
        code += code_cond
        code += "br i1 %{}, label %while.{}, label %end.{}\n".format(register, register, register)

        code_while, reg = self.astNodeToLLVM(node.getBody())
        code += "\nwhile.{}:\n".format(register)
        code += code_while
        code += "br label %cond.{}\n".format(register)
        if "\nret" in code_while:
            self.cur += 1

        code += "\nend.{}:\n".format(register)

        return code, -1

    def programNode(self, node):
        code = ""
        for child in node.getChildren():
            new_code, reg = self.astNodeToLLVM(child)
            code += new_code

        code = self.global_scope_string + code
        return code

    def body(self, node):
        code = ""
        for child in node.getChildren():
            new_code, reg = self.astNodeToLLVM(child)
            code += new_code
        return code, -1

    def funcParam(self, node):
        # param_type = self.getLLVMType(node.getExpressionType())
        param_type, t = node.getSymbolTable().lookup(node.getParamID())
        param_type = self.getLLVMType(param_type)
        return param_type

    def funcDecl(self, node):
        """
        return_type, t = node.getSymbolTable().lookup(node.getID())
        return_type = self.getLLVMType(return_type)

        function_name = "@" + node.getID()

        code = "declare " + return_type + " " + function_name + "("
        first_param = True
        for param in node.getParams():
            if not first_param:
                code += ","
            else:
                first_param = False

            code += self.funcParam(param)

        code += ")\n"
        return code, -1
        """
        return "", -1

    def funcDef(self, node):
        # enter new scope
        self.reg_stack.append(self.cur_reg)
        # %0 is start label
        # %1 ... are args
        self.cur_reg = 0
        code = ""
        return_type, scope = node.getSymbolTable().lookup(node.getFuncID())
        return_type = self.getLLVMType(return_type.getReturnType())
        function_name = "@" + node.getFuncID()

        code += "define " + return_type + " " + function_name + "("
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
            code += self.storeVariable(param_name, self.cur_reg, param_type, False)
            self.cur_reg += 1

        # +1 since otherwise register points to code block
        self.cur_reg += 1
        new_code, reg = self.astNodeToLLVM(node.getBody())
        code += new_code
        # replace by if return_type == "void" at some point when == issue is fixed
        return_found = False
        for child in node.getBody().getChildren():
            if isinstance(child, ReturnStatement):
                return_found = True
                break

        if return_type == "void" and not return_found:
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
        function_id = node.getFunctionID().getIdentifierName()
        needed_param_types, t = node.getSymbolTable().lookup(function_id)
        needed_param_types = needed_param_types.getParamTypes()
        load_groups = list()
        for arg, needed_param_type in zip_longest(node.getArguments(), needed_param_types):
            if not first_arg:
                arg_list += ","
            else:
                first_arg = False

            needed_param_type = self.getLLVMType(
                VariableType(needed_param_type)) if needed_param_type is not None else None

            if isinstance(arg, ConstantExpr) and not function_id in ["scanf", "printf"]:
                constant_type = self.getLLVMType(arg.getExpressionType())
                value = self.convertConstant(needed_param_type, constant_type, arg.getValue())
                arg_list += "{} {}".format(needed_param_type, value)
                continue

            arg_code, arg_reg = self.astNodeToLLVM(arg)

            arg_type = self.getLLVMType(arg.getExpressionType())

            # handle strings separately since we split up the constant expressions
            if isinstance(arg, ConstantExpr):
                load, arg_reg = self.loadVariable(arg_reg, arg_type, False)
                arg_code += load

            # convert params when necessary (not in scanf or printf)
            if needed_param_type != arg_type and function_id not in ["scanf", "printf"]:
                convert, arg_reg = self.convertToType(arg_reg, arg_type, needed_param_type)
                arg_type = needed_param_type
                arg_code += convert

            # vararg functions do not take floats, all floats are converted to double
            if function_id == "printf" and arg_type == "float":
                convert, arg_reg = self.convertToType(arg_reg, arg_type, "double")
                arg_type = "double"
                arg_code += convert

            if isinstance(arg, AddressExpr) and function_id == "scanf":
                load, arg_reg = self.loadVariable(arg_reg, arg_type, False)
                arg_code += load
                arg_id = arg.getTargetExpr().getIdentifierName()
                is_global = node.getSymbolTable().isGlobal(arg_id)
                var_type, t = node.getSymbolTable().lookup(arg_id)

                reg = (t + "." + arg_id) if not is_global else arg_id

                load_groups.append((reg, arg_reg, arg_type[:-1], is_global))

            # extra load necessary because we did a redundant store
            if isinstance(arg, PointerDerefExpr) and function_id == "printf":
                load, arg_reg = self.loadVariable(arg_reg, arg_type, False)
                arg_code += load

            code += arg_code

            arg_list += "{} %{}".format(arg_type, arg_reg)

        arg_list += ")"

        function_id = node.getFunctionID().getIdentifierName()
        reg_type = self.getLLVMType(node.getExpressionType())
        return_type = reg_type if function_id not in ["printf", "scanf"] else "i32 (i8*, ...)"
        func_reg = self.cur_reg
        # void function result can't be assigned
        if reg_type == "void":
            code += "call "
        else:
            code += "%{} = call ".format(func_reg)
            self.cur_reg += 1

        code += "{} @{}".format(return_type, function_id)

        code += arg_list
        code += "\n"
        # store variable after call (when not void as return type)
        if not reg_type == "void":
            code += self.allocate(self.cur_reg, reg_type, False)
            code += self.storeVariable(self.cur_reg, func_reg, reg_type, False)
            func_reg = self.cur_reg
            self.cur_reg += 1

        for reg, arg_reg, arg_type, is_global in load_groups:
            load, load_reg = self.loadVariable(arg_reg, arg_type, is_global)
            code += load
            code += self.storeVariable(reg, load_reg, arg_type, is_global)

        return code, func_reg

    def getLLVMType(self, type_node):
        """ Converts a symbolType to an LLVM type"""
        if type_node.isFunction():
            type_string = type_node.getReturnTypeAsString()

        elif type_node.isVar():
            type_string = type_node.toString()

        elif type_node.isArray():
            type_string = type_node.getEntryTypeAsString()

        else:
            raise Exception("Incorrect type node")
        type_string = type_string.replace("int", "i32")
        type_string = type_string.replace("bool", "i1")
        type_string = type_string.replace("char", "i8")
        return type_string

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

            # if we do division, the passed argument will be "sdiv", but we need "div" to make the trickwork
            if operation == "sdiv":
                operation = "div"

            code += code_left
            code += code_right
            code += "%{} = f{} float %{}, %{}\n".format(self.cur_reg, operation, reg_left, reg_right)
            llvm_type = "float"

        elif strongest_type == "int":
            code_left, reg_left = self.convertToInt(reg_left, type_left)
            code_right, reg_right = self.convertToInt(reg_right, type_right)

            code += code_left
            code += code_right
            code += "%{} = {} i32 %{}, %{}\n".format(self.cur_reg, operation, reg_left, reg_right)
            llvm_type = "i32"

        elif strongest_type == "char":
            code_left, reg_left = self.convertToChar(reg_left, type_left)
            code_right, reg_right = self.convertToChar(reg_right, type_right)

            code += code_left
            code += code_right
            code += "%{} = {} i8 %{}, %{}\n".format(self.cur_reg, operation, reg_left, reg_right)
            llvm_type = "i8"
        elif strongest_type == "bool":
            code_left, reg_left = self.convertToBool(reg_left, type_left)
            code_right, reg_right = self.convertToBool(reg_right, type_right)

            code += code_left
            code += code_right
            code += "%{} = {} i1 %{}, %{}\n".format(self.cur_reg, operation, reg_left, reg_right)
            llvm_type = "i1"
        else:
            raise Exception("Invalid return type from getStrongestType '{}'".format(strongest_type))

        self.cur_reg += 1
        code += self.allocate(self.cur_reg, llvm_type, False)
        code += self.storeVariable(self.cur_reg, self.cur_reg - 1, llvm_type, False)

        self.cur_reg += 1

        return code, self.cur_reg - 1

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
            raise Exception("Converting from '{}' to float for register '{}' is not defined.".format(type, reg))
            # what with other types?
            return code, reg

    def convertToInt(self, reg, type):
        code = ""
        if "int" in type or "i32" in type:
            return code, reg

        elif "i1" in type:
            code += "%{} = zext i1 %{} to i32\n".format(self.cur_reg, reg)
            self.cur_reg += 1
            return code, self.cur_reg - 1

        elif "i8" in type:

            code += "%{} = sext i8 %{} to i32\n".format(self.cur_reg, reg)
            self.cur_reg += 1
            return code, self.cur_reg - 1

        elif "float" in type:
            code += "%{} = fptosi float %{} to i32\n".format(self.cur_reg, reg)
            self.cur_reg += 1
            return code, self.cur_reg - 1


        else:
            raise Exception("Converting from '{}' to int for register '{}' is not defined.".format(type, reg))
            # what with other types?
            return code, reg

    def convertToDouble(self, reg, from_type):
        code = ""
        if "float" in from_type:
            code += "%{} = fpext float %{} to double\n".format(self.cur_reg, reg)
            self.cur_reg += 1
            return code, self.cur_reg - 1
        else:
            raise Exception("Converting from '{}' to float for register '{}' is not defined.".format(type, reg))
            return code, reg

    def convertToChar(self, reg, from_type):
        """
            Returns LLVM IR code for converting the specified register of the specfied type to the "char"/"i8" type.
        """
        code = ""
        if "char" in from_type or "i8" in from_type:
            return code, reg
        elif "i1" in from_type:
            code += "%{} = zext i1 %{} to i8\n".format(self.cur_reg, reg)
            self.cur_reg += 1
            return code, self.cur_reg - 1
        elif "i32" in from_type:
            code += "%{} = trunc i32 %{} to i8".format(self.cur_reg, reg)
            self.cur_reg += 1
            return code, self.cur_reg - 1
        elif "float" in from_type:
            code += "%{} = fptosi float %{} to i8\n".format(self.cur_reg, reg)
            self.cur_reg += 1
            return code, self.cur_reg - 1
        else:
            raise Exception("Converting from '{}' to char for register '{}' is not defined.".format(from_type, reg))
            return code, reg
        # floating point conversion?

    def convertToBool(self, reg, from_type):
        """
            Returns LLVM IR code for converting the specified register of the specified type to the "bool"/"i1" type.
        """
        code = ""
        if "bool" in from_type or "i1" in from_type:
            return code, reg
        else:
            raise Exception("Converting from '{}' to bool for register '{}' is not defined.".format(from_type, reg))
            return code, reg

    def convertToType(self, reg, old_type, new_type):
        if "int" in new_type or "i32" in new_type:
            return self.convertToInt(reg, old_type)

        elif "char" in new_type or "i8" in new_type:
            return self.convertToChar(reg, old_type)
            raise Exception("Conversion from type '{}' to type '{}' in register '{}' is not possible.".format(old_type, new_type, reg))
        elif "float" in new_type:
            return self.convertToFloat(reg, old_type)
        elif "double" in new_type:
            return self.convertToDouble(reg, old_type)
        else:
            raise Exception("Conversion from type '{}' to type '{}' in register '{}' is not possible.".format(old_type, new_type, reg))

    def convertConstant(self, new_type, old_type, value):
        if old_type == "i8" and new_type != old_type:
            value = value[1:-1]

        elif old_type == "i32" and new_type != old_type:
            value = int(value)

        elif old_type == "float" and new_type != old_type:
            value = float(value)

        if old_type == "i1" and new_type != old_type:
            value = False if value == "false" else value
            value = True if value == "true" else value

        if new_type == old_type:
            return value

        elif new_type == "i1":
            return bool(value)

        # character
        elif old_type == 'i8' and new_type == "float":
            return self.floatToHex(float(ord(value)))

        elif old_type == "i8" and new_type == "i32":
            return ord(value)

        # integer
        elif old_type == "i32" and new_type == "float":
            return self.floatToHex(float(int(value)))

        elif old_type == "i32" and new_type == "i8":
            return chr(int(value))

        # bool
        elif old_type == "i1" and new_type == "i8":
            return chr(int(value))

        elif old_type == "i1" and new_type == "i32":
            return int(bool(value))

        elif old_type == "i1" and new_type == "float":
            return float(bool(value))

        elif old_type == "float" and new_type == "i32":
            return int(round(value))

        elif old_type == "float":
            return self.convertConstant(new_type, "i32", int(round(value)))
        else:
            return value

    def returnStatement(self):
        return "ret void\n", -1

    def returnWithExprStatement(self, node):

        expr_type = self.getLLVMType(node.getExpression().getExpressionType())
        function_return_type = self.getLLVMType(node.getFunctionType())

        if isinstance(node.getExpression(), ConstantExpr):
            value = self.convertConstant(function_return_type, expr_type,
                                         node.getExpression().getValue())
            code = "ret {} {}\n".format(function_return_type, value)
            return code, -1

        code, register = self.astNodeToLLVM(node.getExpression())

        # extra load needed when not an identifier
        if not isinstance(node.getExpression(), IdentifierExpr):
            new_code, register = self.loadVariable(register, expr_type, False)
            code += new_code

        # type conversion
        if function_return_type != expr_type:
            convert, register = self.convertToType(register, expr_type, function_return_type)
            code += convert
        code += "ret {} %{}\n".format(function_return_type, register)
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
            code += "%{} = fcmp {} float %{}, %{}\n".format(self.cur_reg, float_op, reg_left, reg_right)
        else:
            code_left, reg_left = self.convertToInt(reg_left, type_left)
            code_right, reg_right = self.convertToInt(reg_right, type_right)

            code += code_left
            code += code_right
            code += "%{} = icmp {} i32 %{}, %{}\n".format(self.cur_reg, int_op, reg_left, reg_right)

        self.cur_reg += 1

        code += self.allocate(self.cur_reg, "i1", False)
        code += self.storeVariable(self.cur_reg, self.cur_reg - 1, "i1", False)
        self.cur_reg += 1
        return code, self.cur_reg - 1

    def include(self):
        self.global_scope_string += "declare i32 @printf(i8*, ...) nounwind \n"
        self.global_scope_string += "declare i32 @scanf(i8*, ...) nounwind \n"
        return "", -1

    def assignmentExpr(self, node):

        # array[element] = value has to be done differently
        if isinstance(node.getLeft(), ArrayAccessExpr):
            return self.arrayElementAssignment(node)

        code, register = self.astNodeToLLVM(node.getRight())
        right_type = self.getLLVMType(node.getRight().getExpressionType())
        left_type = self.getLLVMType(node.getLeft().getExpressionType())

        identifier = node.getLeft().getIdentifierName()
        if not isinstance(node.getRight(), IdentifierExpr):
            load, register = self.loadVariable(register, right_type, node.getSymbolTable().isGlobal(identifier))

            code += load
        if right_type == left_type:
            pass
        else:
            convert, register = self.convertToType(register, right_type, left_type)
            code += convert

        if node.getSymbolTable().isGlobal(identifier):

            code += self.storeVariable(identifier, register, left_type, True)
        else:
            t, table = node.getSymbolTable().lookup(identifier)
            identifier = table + "." + identifier
            code += self.storeVariable(identifier, register, left_type, False)

        return code, identifier

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

    def pointerDerefExpr(self, node):
        #
        if isinstance(node.getTargetPtr(), PointerDerefExpr):
            expr_type = self.getLLVMType(node.getTargetPtr().getExpressionType())
            target_reg = self.cur_reg - 1

            load, target_reg = self.loadVariable(target_reg, expr_type, False)
            code = load

        else:
            code, target_reg = self.astNodeToLLVM(node.getTargetPtr())
            expr_type = self.getLLVMType(node.getTargetPtr().getExpressionType())

        expr_type = expr_type[:-1]
        load, register = self.loadVariable(target_reg, expr_type, False)
        code += load

        code += self.allocate(self.cur_reg, expr_type, False)
        code += self.storeVariable(self.cur_reg, register, expr_type, False)

        self.cur_reg += 1

        return code, self.cur_reg - 1

    def addStringToGlobal(self, string):
        """
        Add string to global scope
        :param string: string to be added
        :return: register the string is located in
        """

        # adjust string size based on the amount of \n and \t and \\ (backslash)
        c = string.count("\\n")
        c += string.count("\\t")
        c += string.count("\\\\")
        c *= 2
        string = string.replace("\\n", "\\0A").replace("\\t", "\\09").replace("\\\\", "\\5C")
        reg = ".str"
        if len(self.string_to_regs) > 0:
            reg = reg + "." + str(len(self.string_to_regs))

        self.string_to_regs[string] = reg
        self.reg_to_string[reg] = (string, len(string) + 1 - c)

        line = "@" + reg + " = private unnamed_addr constant "
        line += "[" + str(len(string) + 1 - c) + " x i8] "
        line += "c" + "\"" + string + "\\00" + "\"" + "\n"

        self.global_scope_string += line
        return reg

    def storeString(self, string_reg, reg_to):
        # store i8* getelementptr inbounds ([14 x i8], [14 x i8]* @.str, i32 0, i32 0), i8** %2, align 8
        type_size = "[" + str(self.reg_to_string.get(string_reg)[1]) + " x i8]"
        code = "store i8* getelementptr inbounds ("
        code += type_size + ", " + type_size + "*"
        code += " @" + string_reg + ", i32 0, i32 0), "
        code += "i8** " + "%{}".format(reg_to)
        code += "\n"
        return code

    def arrayDecl(self, node):
        # array size expression must be of a IntegerConstantExpression
        array_size = node.getSizeExpr().getIntValue()

        array_id = node.getID()
        array_type, table = node.getSymbolTable().lookup(array_id)
        array_type = self.getLLVMType(array_type)
        code = ""
        is_global = node.getSymbolTable().isGlobal(array_id)

        array_code = "[{} x {}]".format(array_size, array_type)
        if is_global:
            code = "@{} = global {} zeroinitializer\n".format(array_id, array_code)

        else:
            array_id = table + "." + array_id
            code = self.allocate(array_id, array_code, False)
            # TODO do i have to add store 0 to initialize every element to 0?

        return code, -1

    def arrayElementAssignment(self, node):
        code, register = self.astNodeToLLVM(node.getRight())
        right_type = self.getLLVMType(node.getRight().getExpressionType())
        left_type = self.getLLVMType(node.getLeft().getExpressionType())

        identifier = node.getLeft().getTargetArray()

        if not isinstance(node.getRight(), IdentifierExpr):
            load, register = self.loadVariable(register, right_type, node.getSymbolTable().isGlobal(identifier))

            code += load
        if right_type == left_type:
            pass
        else:
            convert, register = self.convertToType(register, right_type, left_type)
            code += convert

        if node.getSymbolTable().isGlobal(identifier):

            code += self.storeVariable(identifier, register, left_type, True)
        else:
            t, table = node.getSymbolTable().lookup(identifier)
            identifier = table + "." + identifier
            code += self.storeVariable(identifier, register, left_type, False)

        return code, identifier


