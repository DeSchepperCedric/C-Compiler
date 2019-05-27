from ASTTreeNodes import *
import struct as struct
from itertools import zip_longest


class MipsGenerator:
    def __init__(self):
        self.data_string = ".data: \n"
        self.string_counter = 0
        self.float_counter = 0
        self.reg_to_string = dict()
        self.array_sizes = dict()

        # maps scope_name.var_name to an offset relative to the frame pointer
        self.var_offset_dict = dict()

        # dict that maps function names to FuncDef objects
        self.function_defs = dict()

        self.fp_offset = 0  # offset to current frame pointer

        self.sp_offset = 0 # offset to the final stack pointer

        self.label_counter = 0
        self.free_regs = ["$t0", "$t1", "$t2", "$t3"]
        self.free_float_regs = ["$f0", "$f1", "$f2", "$f3"]

        self.float_return_reg = "$f31"
        self.return_reg = "$v0"

    def astNodeToMIPS(self, node):
        """
            Returns a tuple (code, reg) with code being the MIPS code and reg
            being the register that contains the result.
        """
        if isinstance(node, IncludeNode):
            return "", -1

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
            return "", -1
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
            return "", -1
        elif isinstance(node, FuncDecl):
            return "", -1
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
            return "", -1
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

    def getUniqueLabelId(self):
        """
            Retrieve a unique id to create labels with. This
            function also increments the internal label counter.
        """

        self.label_counter += 1

        return self.label_counter

    def getFreeReg(self):
        """
            Retrieve the name of an available temp register.
        """
        if len(self.free_regs) == 0:
            raise Exception("Error when requesting free register: no registers available.")

        return self.free_regs.pop()

    def releaseReg(self, reg: str):
        """
            Mark the specified temp register as available.
        """

        if reg.startswith("$t"):
            if reg in self.free_regs:
                raise Exception("Error when releasing reg '{}': register is already free.".format(reg))
            else:
                self.free_regs.append(reg)
        elif reg.startswith("$f"):
            if reg in self.free_float_regs:
                raise Exception("Error when releasing reg '{}': register is already free.".format(reg))
            else:
                self.free_float_regs.append(reg)
        else:
            raise Exception("Specified register '{}' is not a temporary or float register.".format(reg))

    def getFreeFloatReg(self):
        """
            Retrieve the name an available float register.
        """

        if len(self.free_float_regs) == 0:
            raise Exception("Error when requesting free float register: no float register availble.")

        return self.free_float_regs.pop()

    def releaseFloatReg(self, reg):
        """
            Mark the specified float register as available.
        """

        if reg in self.free_float_regs:
            raise Exception("Error when releasing float reg '{}': float register is already free.".format(reg))

        if not reg.startswith("$f"):
            raise Exception("Specified register '{}' is not a float register.".format(reg))

        self.free_float_regs.append(reg)

    def getSpOffset(self):
        """
            Retrieve the current $sp offset. The offset
            is so that $sp+offset points to the bottom of the stackframe:

            -------- <- $sp + offset
            stackframe
            -------- <- $sp

            If a new value needs to be stored, use "sw $val offset($sp)" and increment
            offset by 4.

        :return: An integer that represents the offset.
        """

        return self.sp_offset

    def incrementSpOffset(self, amount=4):
        """
            Increment the $sp offset by the specified amount (in bytes). Use positive values!
            The default amount is 4.
        :param amount: The amount of bytes that the $sp should be offset by.
        :return: The new $sp offset;
        """

        self.sp_offset += amount

        return self.sp_offset

    def resetSpOffset(self):
        """
            Reset the $sp offset to its default value. This will set the
            stackframe size to 0.
        :return: The new $sp offset.
        """

        self.sp_offset = 0
        return self.sp_offset

    def getFpOffset(self):
        """
            Retrieve the current fp offset.
        """
        return self.fp_offset

    def pushFpOffset(self, change=4):
        """
            Adjust the fp offset to accomodate 4 % change variable(s) on the stack.

            :return: The new value of the fp offset.
        """

        # 4 bytes
        self.fp_offset -= change

        return self.fp_offset

    def popFpOffset(self, change=4):
        """
            Adjust the fp offset to remove 4 % change variable(s) from the stack.
            :return: The new value of the fp offset.
        """

        self.fp_offset += change

        return self.fp_offset

    def resetFpOffset(self):
        """
            Reset the fp offset to 0.
        """

        self.fp_offset = 0

    def storeRegister(self, source_reg: str, addr_reg: str, offset, is_float=False) -> str:
        """
            Store the specified register in memory at the specified address.

            Params:
                'source_reg': the register that contains the value that will be stored.
                'addr_reg': the register that contains the address where the value will be stored.
                'offset': the offset that will be added to the address stored in 'addr_reg'. Specify as integer.
        """

        # added extra check for $fp
        if is_float and (not source_reg.startswith("$f") or source_reg == "$fp"):
            raise Exception("Error when trying to store non-float register {} as float.".format(source_reg))

        if not is_float and source_reg.startswith("$f") and source_reg != "$fp":
            raise Exception("Error when trying to store float register {} as non-float.".format(source_reg))

        command = "sw" if not is_float else "swc1"

        return "{} {}, {}({})\n".format(command, source_reg, offset, addr_reg)

    def loadRegister(self, addr_reg: str, offset, is_float=False, target_reg=None):
        """
            Load the value stored in the memory at the specified address into the specified register.

            Params:
                'addr_reg': The register that contains the address at which the value is stored.
                'offset': the offset that will be added to the address stored in 'addr_reg'. Specify as integer.
                'target_reg': Specific register to place value in
        """

        command = "lw" if not is_float else "lwc1"
        if target_reg is None:
            target_reg = self.getFreeReg() if not is_float else self.getFreeFloatReg()
            return "{} {}, {}({})\n".format(command, target_reg, offset, addr_reg), target_reg

        else:
            return "{} {}, {}({})\n".format(command, target_reg, offset, addr_reg)

    def storeVariable(self, source_reg, node) -> str:
        """
            Store a variable on the stack. If the variable is not yet present on the stack the
            stackframe will be expanded to accomodate the variable. If the variable already exists,
            the existing value will be adjusted.

        :param source_reg: The register that contains the new value.
        :param node: The node that contains information about the variable. This can be IdentifierExpr or VarDeclWithInit
        :return:
        """
        # node can be IdentifierExpr or VarDeclWithInit
        var_type = node.getExpressionType().toString() if isinstance(node, IdentifierExpr) else node.getType()
        # determine if the variable is a float
        is_float = var_type == "float"

        # get varname
        varname = node.getIdentifierName() if isinstance(node, IdentifierExpr) else node.getID()

        # determine whether the variable is a global:
        is_global = node.getSymbolTable().isGlobal(varname)

        if is_global:

            # aquire register
            temp_addr_reg = self.getFreeReg()

            code = "la {}, {}\n".format(temp_addr_reg, varname)
            code += self.storeRegister(source_reg, temp_addr_reg, 0, is_float)

            # release register
            self.releaseReg(temp_addr_reg)

            # retrieve from data segment and store
            return code

        else:
            # there is a 100% guarantee that the variable exists in the table

            # get scopename
            type, scopename = node.getSymbolTable().lookup(varname, False)

            # get full var id
            full_id = scopename + "." + varname

            # determine if the variable already is stored on the stack
            if full_id in self.var_offset_dict:
                # retrieve offset and store

                reg, offset = self.var_offset_dict[full_id]

                # store in "offset(source_reg)"
                code = self.storeRegister(source_reg, reg, offset, is_float)

                return code
            else:
                # push new variable to the stack

                # make place for the value
                # this needs to happen before store since the $sp points at
                # the most recently stored entry.
                offset = self.incrementSpOffset()
                code = self.storeRegister(source_reg, "$sp", offset, is_float)

                # note here we place a value on the stack and assume that it is
                # relative to the stack pointer. The only times a store needs to
                # be relative to the $fp, is when placing function args on the stack.
                self.var_offset_dict[full_id] = ("$sp", offset)

                return code

    def loadVariable(self, id_node: IdentifierExpr) -> (str, str):
        """
            Load the specified variable into a temp register.

        :param id_node: An IdentifierExpr that contains information about the variable.
        :return: A pair of strings. The first string specifies the code, the second specifies the register.
        """
        # determine if the variable is a float
        is_float = id_node.getExpressionType().toString() == "float"

        # get varname
        varname = id_node.getIdentifierName()

        # determine whether the variable is a global:
        if id_node.getSymbolTable().isGlobal(varname):

            # aquire register
            temp_addr_reg = self.getFreeReg()

            code = "la {}, {}\n".format(temp_addr_reg, varname)
            load, target_reg = self.loadRegister(temp_addr_reg, 0, is_float)
            code += load
            # release register
            self.releaseReg(temp_addr_reg)

            # retrieve from data segment and store
            return code, target_reg

        else:
            # get scopename
            type, scopename = id_node.getSymbolTable().lookup(varname, False)

            # get full var id
            full_id = scopename + "." + varname

            # determine if the variable already is stored on the stack
            if full_id in self.var_offset_dict:
                # retrieve offset and store

                reg, offset = self.var_offset_dict[full_id]

                return self.loadRegister(reg, offset, is_float)
            else:
                raise Exception("Error when loading variable '{}': variable is not yet stored on the stack".format(varname))

    ################################### CONSTANT EXPRESSIONS ###################################

    def boolConstantExpr(self, expr):
        """
        Return a constant bool with its type and the register it's stored in
        """

        value = 1 if expr.getBoolValue() is True else 0
        reg = self.getFreeReg()
        code = "li {}, {}\n".format(reg, value)
        return code, reg

    def floatConstantExpr(self, expr):
        """
        Return a constant float with its type and the register it's stored in
        """

        # TODO handle floats
        # add to data segment
        float_id = "float." + str(self.float_counter)
        self.float_counter += 1
        self.data_string += "{}: .{} {}\n".format(float_id, "float", expr.getFloatValue())
        code = ""

        # aquire register
        temp_addr_reg = self.getFreeReg()

        code = "la {}, {}\n".format(temp_addr_reg, float_id)
        load, float_reg = self.loadRegister(temp_addr_reg, 0, True)
        code += load
        # release register
        self.releaseReg(temp_addr_reg)

        # retrieve from data segment and store
        return code, float_reg

        pass

    def integerConstantExpr(self, expr):
        """
        Return a constant integer with its type and the register it's stored in
        """
        reg = self.getFreeReg()
        code = "li {}, {}\n".format(reg, expr.getIntValue())
        return code, reg

    def charConstantExpr(self, expr):
        """
        Return a constant char with its type and the register it's stored in
        """
        reg = self.getFreeReg()

        char_val = expr.getCharValue()[1:-1] # strip '
        char_val = char_val.replace("\\\\", "\\")
        char_val = char_val.replace("\\t", "\t")
        char_val = char_val.replace("\\n","\n")
        char_val = char_val.replace("\\0", "\0")
        char_val = char_val.replace("\\'", "'")

        code = "li {}, {}\n".format(reg, ord(char_val))
        return code, reg

    def stringConstantExpr(self, expr):
        # TODO handle strings
        pass

    ################################### AST NODES ###################################

    def programNode(self, node: ProgramNode):
        """
            Process a program node. This will return the full .text segment.
        """

        code = ".text\n"

        code += "j main\n"  # jump to main function

        # discover function nodes
        for child in node.getChildren():
            if isinstance(child, FuncDef):
                # add function decl node to list of functions
                self.function_defs[child.getFuncID()] = child

        # process top level nodes
        for child in node.getChildren():
            child_code, child_reg = self.astNodeToMIPS(child)
            code += child_code
            # ignore register

        # label end program to provide exit for main()
        code += "program_end:\n"

        code = self.data_string + code
        return code

    def varDeclWithInit(self, node):
        expr_type = self.getMipsType(node.getInitExpr().getExpressionType())
        var_id = node.getID()
        var_type, table = node.getSymbolTable().lookup(var_id)
        var_type = self.getMipsType(var_type)
        code = ""
        is_global = node.getSymbolTable().isGlobal(var_id)

        if is_global and isinstance(node.getInitExpr(), ConstantExpr):
            value = self.convertConstant(var_type, expr_type, node.getInitExpr().getValue())
            self.data_string += "{}: .{} {}\n".format(var_id, var_type, value)
        elif is_global and isinstance(node.getInitExpr(), AddressExpr):
            # TODO handle AddressExpr
            pass

        else:
            new_code, register = self.astNodeToMIPS(node.getInitExpr())
            code += new_code

            if var_type != expr_type:
                convert, register = self.convertToType(register, expr_type, var_type)
                code += convert

            code += self.storeVariable(register, node)
            self.releaseReg(register)

        return code, -1

    def branchStatement(self, node: BranchStmt):
        """
            Convert an BranchStmt to MIPS code.
        """

        ## process children ##
        # retrieve condition code
        cond_code, cond_reg = self.astNodeToMIPS(node.getCondExpr())

        # check of the condition expression is float
        is_float = node.getCondExpr().getExpressionType().toString() == "float"

        if_code, reg = self.astNodeToMIPS(node.getIfBody())
        else_code, reg = self.astNodeToMIPS(node.getElseBody())

        cond_label_id = self.getUniqueLabelId()
        if_label_id = self.getUniqueLabelId()
        else_label_id = self.getUniqueLabelId()
        endif_label_id = self.getUniqueLabelId()

        code = "cond_{}:\n".format(cond_label_id)
        code += cond_code

        if is_float:
            # float must first be evaluated, then the bit must be checked

            raise Exception("If statements with float are not yet implemented.")

            code += "bc1f else_branch_{}\n".format(else_label_id)
        else:
            # non-float, simple branch statement is enough
            # if the result is false => go to else
            code += "beqz {}, else_branch_{}\n".format(cond_reg, else_label_id)

        code += "if_branch_{}:\n".format(if_label_id)
        code += if_code

        # jump to end
        code += "j endif_{}\n".format(endif_label_id)

        code += "else_branch_{}:\n".format(else_label_id)
        code += else_code

        # jump to end
        code += "j endif_{}:\n".format(endif_label_id)

        # end of branch statement
        code += "endif_{}:\n".format(endif_label_id)

        return code, -1

    def whileStatement(self, node: WhileStmt):
        """
            Convert the while statement to MIPS code.
        """

        cond_code, cond_reg = self.astNodeToMIPS(node.getCondExpr())

        # check of the condition expression is float
        is_float = node.getCondExpr().getExpressionType().toString() == "float"

        body_code, body_reg = self.astNodeToMIPS(node.getBody())

        cond_label_id = self.getUniqueLabelId()
        loop_label_id = self.getUniqueLabelId()
        endwhile_label_id = self.getUniqueLabelId()

        code = "cond_{}:\n".format(cond_label_id)
        code += cond_code

        if is_float:
            raise Exception("While statements with float are not yet implemented.")
        else:
            # if the result is false => go to endwhile
            code += "beq {} $0 endwhile_{}:\n".format(cond_reg, endwhile_label_id)

        code += "loop_{}:\n".format(loop_label_id)
        code += body_code

        code += "j cond_{}:\n".format(cond_label_id)

        code += "endwhile_{}:\n".format(endwhile_label_id)

        return code, -1

    def statementContainer(self, node):
        # iterate over statements and process
        code = ""
        for child in node.getChildren():
            new_code, reg = self.astNodeToMIPS(child)
            code += new_code

        return code, -1

    def funcDef(self, node: FuncDef):
        code = ""

        # set the frame pointer offset to zero
        self.resetSpOffset()
        # $sp+0 now points to the top of the former stackframe

        # the stack structure at this moment
        """
            ----------
            old $sp
            ----------
            old $ra
            ----------
            old t3
            ----------
            old t2
            ----------
            old t1
            ----------
            old t0
            ----------
            param_n-1
            ----------
            ...
            ----------
            param_0
            ---------- <- $sp, $fp
        """
        # the stack structure will evolve after the $sp is adjusted
        """
            ----------
            param_0
            ---------- <- old $sp, $fp
            local_vars
            ---------- <- new $sp
        """

        # TODO make parameters accesible after $sp is adjusted
        # TODO make offsets into pairs (reg, offset)


        # function label
        function_name = node.getFuncID()

        code += "{}:\n".format(function_name)

        # function body
        # return value is placed into $v0 or $f31 by a return expression
        func_body, reg = self.astNodeToMIPS(node.getBody())
        code += func_body

        # return
        if node.getFuncID() == "main":
            code += "j end_program\n"
        else:
            code += "jr $ra\n"

        # adjust $sp at the beginning
        code = "addi $sp, $sp, {}\n".format(self.getSpOffset()) + code

        # we don't return a register since a function definition does not return anything
        return code, -1

    def funcCallExpr(self, node: FuncCallExpr):
        code = ""

        # TODO add function call code.

        # store $sp:

        """
            local_vars
            ---------- <- old $sp
            old t3
            ---------- <- old $sp-4
            old t2
            ---------- <- old $sp-8
            old t1
            ---------- <- old $sp-12
            old t0
            ---------- <- old $sp-16
            old return addr
            ----------
            old frame_ptr
            ----------
            old stack_ptr
            ---------- <- $fp + len(args)*4
            param_n-1
            ---------- <- $fp + (len(args)-1)*4
            ...
            ---------- <- $fp+4
            param_0
            ---------- <- $sp, $fp+0
        """

        # here we create a bit of space in between two proper stackframes
        # this space will be used to store $sp, $fp, $ra, $t0-$t3, and parameters

        temp_offset = 0

        # save t0-t3, t0 last
        temp_offset -= 4
        code += self.storeRegister("$t3", "$sp", temp_offset)

        temp_offset -= 4
        code += self.storeRegister("$t2", "$sp", temp_offset)

        temp_offset -= 4
        code += self.storeRegister("$t1", "$sp", temp_offset)

        temp_offset -= 4
        code += self.storeRegister("$t0", "$sp", temp_offset)

        # save old $ra
        temp_offset -= 4
        code += self.storeRegister("$ra", "$sp", temp_offset)

        # save old $fp
        temp_offset -= 4
        code += self.storeRegister("$fp", "$sp", temp_offset)

        # save old sp
        temp_offset -= 4
        code += self.storeRegister("$sp", "$sp", temp_offset)

        # count params
        # adjust $fp: $fp = $sp + temp_offset(neg) - len(args) * 4
        code += "addi $fp, $sp, {}\n".format(temp_offset - len(node.getArguments()) * 4)

        fp_arg_offset = 0

        # save params on the stack relative to the $fp
        for i in range(0, len(node.getArguments())):
            arg = node.getArguments()[i]
            arg_code, arg_reg = self.astNodeToMIPS(arg)
            code += arg_code

            is_arg_float = arg.getExpressionType().toString() == "float"
            code += self.storeRegister(arg_reg, "$fp", fp_arg_offset, is_float=is_arg_float)

            fp_arg_offset += 4 # do this after since the $fp points to the a free stack place

            funcdef_node = self.function_defs[node.getFunctionID().getIdentifierName()]
            param_name = funcdef_node.getParamList()[i].getParamID()
            function_scopename = funcdef_node.getSymbolTable().getName()

            self.var_offset_dict[function_scopename + "." + param_name] = ("$fp", fp_arg_offset)

        code += "addi $sp, $fp, 0\n"
        # $fp and $sp point now to the first parameter
        # the callee will adjust $sp to the end of the stackframe.

        # call function
        code += "jal {}\n".format(node.getFunctionID().getIdentifierName())

        sp_location_rel_to_fp = len(node.getArguments()) * 4

        # load $sp, this is just below the parameters relative to the current $fp
        code += "lw $sp, {}($fp)\n".format(sp_location_rel_to_fp)

        # load $fp
        code += "lw $fp, {}($fp)\n".format(sp_location_rel_to_fp + 4)


        # load t0-t3
        code += "lw $t3, {}($sp)\n".format(-4)
        code += "lw $t3, {}($sp)\n".format(-8)
        code += "lw $t3, {}($sp)\n".format(-12)
        code += "lw $t3, {}($sp)\n".format(-16)

        retval_type = node.getExpressionType()

        if retval_type.toString() == "float":
            ret_reg = self.getFreeFloatReg()
            # copy $f31 into ret_reg
            code += "mov.s {}, {}\n".format(ret_reg, self.float_return_reg)

        else:
            ret_reg = self.getFreeReg()
            # copy $v0 into ret_reg
            code += "mov {}, {}, 0\n".format(ret_reg, self.return_reg)

        return code, ret_reg

    def identifierExpr(self, node):
        return self.loadVariable(node)

    def arithmeticExpr(self, node, operation):
        # dest = src1 op src2
        # op dest, src, src2
        # int -> op
        # float ->  op + ".s"
        code = ""

        type_left = self.getMipsType(node.getLeft().getExpressionType())
        type_right = self.getMipsType(node.getRight().getExpressionType())

        code_left, reg_left = self.astNodeToMIPS(node.getLeft())
        code_right, reg_right = self.astNodeToMIPS(node.getRight())

        code += code_left
        code += code_right

        if type_left == "float" or type_right == "float":

            convert, reg_left = self.convertToType(reg_left, type_left, "float")
            code += convert
            convert, reg_right = self.convertToType(reg_right, type_right, "float")
            code += convert

            if not reg_left.startswith("$f"):
                raise Exception("Specified register {} is not a float register".format(reg_left))

            operation += ".s"


        # re-use reg_left as destination register
        code += "{} {}, {}, {}\n".format(operation, reg_left, reg_left, reg_right)

        self.releaseReg(reg_right)
        return code, reg_left

    def returnWithExprStatement(self, node: ReturnWithExprStatement):
        code = ""

        # resolve expression
        expr_code, expr_reg = self.astNodeToMIPS(node.getExpression())

        code += expr_code

        if node.getExpression().getExpressionType().toString() == "float":
            code += "mov.s $f31, {}\n".format(expr_reg)
        else:
            code += "mov $v0, {}\n".format(expr_reg)

        self.releaseReg(expr_reg)

        # this expression has a register, but it is a technical register that should not be used further
        return code, -1

    def comparisonExpr(self, node, op):
        # cond = (src1 op src2)
        # op src, src2
        # int -> op
        # float ->  "c." + op + ".s"

        code = ""

        type_left = node.getLeft().getExpressionType().toString()
        type_right = node.getRight().getExpressionType().toString()

        code_left, reg_left = self.astNodeToMIPS(node.getLeft())
        code_right, reg_right = self.astNodeToMIPS(node.getRight())

        code += code_left
        code += code_right

        if type_left == "float" or type_right == "float":
            op = "c." + op + ".s"
            code_left, reg_left = self.convertToType(reg_left, type_left, "float")
            code_right, reg_right = self.convertToType(reg_right, type_right, "float")

            code += code_left
            code += code_right

        code += "{} {}, {}\n".format(op, reg_left, reg_right)
        return code, - 1

    def assignmentExpr(self, node):
        # array[element] = value has to be done differently
        if isinstance(node.getLeft(), ArrayAccessExpr):
            # TODO handle arrays
            return self.arrayElementAssignment(node)

        code, register = self.astNodeToMIPS(node.getRight())
        right_type = self.getMipsType(node.getRight().getExpressionType())
        left_type = self.getMipsType(node.getLeft().getExpressionType())

        # type conversion
        if right_type != left_type:
            convert, register = self.convertToType(register, right_type, left_type)
            code += convert

        code += self.storeVariable(register, node.getLeft())
        return code, -1

    def expressionStatement(self, node):
        return self.astNodeToMIPS(node.getExpression())

    def addressExpr(self, node):
        pass

    def pointerDerefExpr(self, node):
        pass

    def arrayDecl(self, node):
        # array size expression must be of a IntegerConstantExpression
        array_size = node.getSizeExpr().getIntValue()

        array_id = node.getID()
        array_type, table = node.getSymbolTable().lookup(array_id)
        array_type = self.getMipsType(array_type)
        code = ""
        is_global = node.getSymbolTable().isGlobal(array_id)
        print(array_type)
        if is_global:
            array_string = "{}: .{}".format(array_id, array_type)
            for i in range(0, array_size):
                array_string += " 0,"

            self.data_string += array_string[:-1] + "\n"

        else:
            # push new array to the stack using size
            # get full var id
            full_id = table + "." + array_id

            # TODO make room on stack (and fill with zeros?)

        return code, -1

    def arrayElementAssignment(self, node):
        # TODO
        # get start of array
        # adjust offset with index
        # store new value
        pass

    def arrayElementAccess(self, node):
        # TODO
        # get start of array
        # adjust offset with index
        # load value into reg
        pass

    def castExpr(self, node):
        """
            Generate code to perform a cast to the specified type.
        """
        code, expr_reg = self.astNodeToMIPS(node.getExpr())  # convert expression to MIPS code

        source_type = self.getMipsType(node.getExpr().getExpressionType())  # get type of expression
        target_type = self.getMipsType(node.getTargetType())  # get target type

        convert, convert_reg = self.convertToType(expr_reg, source_type, target_type)  # perform conversion

        code += convert
        return code, convert_reg  # return code, and the location of the conversion

    def prefixArithmetics(self, node, operation):
        pass

    def postfixArithmetics(self, node, operation):
        pass

    ############################################# TYPE METHODS #############################################

    def arrayAccessHelperString(self, reg_to, reg_from, element_type, index, is_global):
        pass

    def convertIntegerToFloat(self, int_reg):
        # mtc1 $t0, $f0 : copy $t0 to $f0
        # cvt.s.w FRdest, FRsrc : Convert Integer to Single
        float_reg = self.getFreeFloatReg()
        code = "mtc1 {}, {}\n".format(int_reg, float_reg)
        code += "cvt.s.w {}, {}\n".format(float_reg, float_reg)

        # int_reg isn't necessary anymore
        self.releaseReg(int_reg)
        return code, float_reg

    def convertFloatToInteger(self, float_reg):
        # mfc1 $t0, $f0 : copy $f0 to $t0
        # cvt.w.s FRdest, FRsrcConvert Single to Integer
        int_reg = self.getFreeReg()
        code = "cvt.w.s {}, {}\n".format(float_reg, float_reg)
        code += "mfc1 {}, {}\n".format(int_reg, float_reg)


        # float_reg isn't necessary anymore
        self.releaseReg(float_reg)
        return code, int_reg

    def convertToType(self, reg, old_type, new_type):
        if "float" in new_type and "float" not in old_type:
            return self.convertIntegerToFloat(reg)
        elif "float" in old_type and "float" not in new_type:
            return self.convertFloatToInteger(reg)
        else:
            return "", reg

    def convertConstant(self, new_type, old_type, value):
        if old_type == "character":
            value = value[1:-1]
            value = ord(value)

        elif old_type == "word" and new_type != old_type:
            value = int(value)

        elif old_type == "float" and new_type != old_type:
            value = float(value)

        if old_type == "byte" and new_type != old_type:
            value = False if value == "false" else value
            value = True if value == "true" else value

        if new_type == old_type:
            return value

        elif new_type == "byte":
            return bool(value)

        # character
        elif old_type == "character" and new_type == "float":
            return float(ord(value))

        elif old_type == "character" and new_type == "word":
            return ord(value)

        # integer
        elif old_type == "word" and new_type == "float":
            return float(int(value))

        elif old_type == "word" and new_type == "character":
            return chr(int(value))

        # bool
        elif old_type == "bool" and new_type == "character":
            return chr(int(value))

        elif old_type == "byte" and new_type == "word":
            return int(bool(value))

        elif old_type == "byte" and new_type == "float":
            return float(bool(value))

        elif old_type == "float" and new_type == "word":
            return int(round(value))

        elif old_type == "float":
            return self.convertConstant(new_type, "word", int(round(value)))
        else:
            return value

    # QUESTION type methods still needed?
    def getCType(self, type_node):
        """ Converts a symbolType to an LLVM type"""
        if type_node.isFunction():
            return type_node.getReturnTypeAsString()

        elif type_node.isVar():
            return type_node.toString()

        elif type_node.isArray():
            return type_node.getEntryTypeAsString()

        else:
            raise Exception("Incorrect type node")

    # QUESTION type methods still needed?
    def getMipsType(self, type_node):
        """ Converts a symbolType to a Mips type"""
        if type_node.isFunction():
            type_string = type_node.getReturnTypeAsString()

        elif type_node.isVar():
            type_string = type_node.toString()

        elif type_node.isArray():
            type_string = type_node.getEntryTypeAsString()

        else:
            raise Exception("Incorrect type node")
        type_string = type_string.replace("int", "word")
        type_string = type_string.replace("bool", "byte")
        type_string = type_string.replace("char", "character")
        return type_string
