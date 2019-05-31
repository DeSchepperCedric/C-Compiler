from ASTTreeNodes import *
import struct as struct
from itertools import zip_longest

import re


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

        self.sp_offset = 0  # offset to the final stack pointer

        self.label_counter = 0

        # NOTE: $v0, $f0 and $f12 are reserved.
        # NOTE: $f31 and $v1 also cannot be used for temp regs since they are used for returns
        # NOTE: $f30 is the float register that is always zero just like $0
        # NOTE: $s0 is also used to temporarily store the $fp, so it is also reserved

        self.float_return_reg = "$f31"
        self.return_reg = "$v1"
        self.float_zero_reg = "$f30"

        # list of all registers that are available for this program
        self.all_temp_regs = {"$t0", "$t1", "$t2", "$t3"}
        self.all_float_regs = {"$f1", "$f2", "$f3", "$f4"}

        # initialise registers
        self.resetRegs()

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
            return "", -1
        elif isinstance(node, FuncDecl):
            return "", -1
        elif isinstance(node, FuncDef):
            return self.funcDef(node)
        elif isinstance(node, FuncCallExpr):
            # no need for complicated function calling mechanisms
            # manual printf processing is easier
            if node.getFunctionID().getIdentifierName() == "printf":
                return self.printfExpr(node)
            elif node.getFunctionID().getIdentifierName() == "scanf":
                return self.scanfExpr(node)
            else:
                return self.funcCallExprLooped(node)

        elif isinstance(node, AddExpr):
            return self.arithmeticExpr(node, "add")
        elif isinstance(node, SubExpr):
            return self.arithmeticExpr(node, "sub")
        elif isinstance(node, MulExpr):
            return self.arithmeticExpr(node, "mul")
        elif isinstance(node, DivExpr):
            return self.arithmeticExpr(node, "div")
        elif isinstance(node, ModExpr):
            return self.modExpr(node)

        elif isinstance(node, PrefixIncExpr):
            return self.prefixArithmetics(node, "add")
        elif isinstance(node, PrefixDecExpr):
            return self.prefixArithmetics(node, "sub")
        elif isinstance(node, PostfixIncExpr):
            return self.postfixArithmetics(node, "add")
        elif isinstance(node, PostfixDecExpr):
            return self.postfixArithmetics(node, "sub")

        elif isinstance(node, LogicAndExpr):
            return self.logicBinopExpr(node, op="and")
        elif isinstance(node, LogicOrExpr):
            return self.logicBinopExpr(node, op="or")
        elif isinstance(node, LogicNotExpr):
            return self.logicNotExpr(node)

        # format here is (node, int-op, float-op)
        elif isinstance(node, EqualityExpr):
            return self.comparisonExpr(node, "seq", "c.eq.s", False)
        elif isinstance(node, InequalityExpr):
            return self.comparisonExpr(node, "sne", 'c.eq.s', True)
        elif isinstance(node, CompGreater):
            return self.comparisonExpr(node, "sgt", "c.le.s", True)
        elif isinstance(node, CompLess):
            return self.comparisonExpr(node, "slt", "c.lt.s", False)
        elif isinstance(node, CompGreaterEqual):
            return self.comparisonExpr(node, "sge", "c.lt.s", True)
        elif isinstance(node, CompLessEqual):
            return self.comparisonExpr(node, "sle", "c.le.s", False)

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
            Mark the specified register as available.
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

    def resetRegs(self):
        """
            Free all used registers.
        """
        self.free_regs = list(self.all_temp_regs)
        self.free_float_regs = list(self.all_float_regs)

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
        if amount % 4 != 0:
            raise Exception("Amount of bytes should be multiple of 4.")
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

    def loadRegister(self, addr_reg: str, offset, is_float=False, target_reg=None) -> str:
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

    def storeVariable(self, source_reg, node: [IdentifierExpr, VarDeclWithInit]) -> str:
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
        var_count = node.getNodecounter() if isinstance(node, IdentifierExpr) else 0
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
            type, scopename = node.getSymbolTable().lookup(varname, var_count, False)

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

            type, scopename = id_node.getSymbolTable().lookup(varname, id_node.getNodecounter(), False)
            # get full var id
            full_id = scopename + "." + varname

            # determine if the variable already is stored on the stack
            if full_id in self.var_offset_dict:
                # retrieve offset and store

                reg, offset = self.var_offset_dict[full_id]

                return self.loadRegister(reg, offset, is_float)
            else:
                raise Exception(
                    "Error when loading variable '{}': variable is not yet stored on the stack".format(varname))

    ################################### CONSTANT EXPRESSIONS ###################################

    def boolConstantExpr(self, expr):
        """
        Return a constant bool and the register it's stored in
        """

        value = 1 if expr.getValue() is True else 0
        reg = self.getFreeReg()
        code = "li {}, {}\n".format(reg, value)
        return code, reg

    def floatConstantExpr(self, expr):
        """
        Return a constant float and the register it's stored in
        """

        # add to data segment
        float_id = "float." + str(self.float_counter)
        self.float_counter += 1
        self.data_string += "{}: .float {}\n".format(float_id, expr.getValue())
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

    def integerConstantExpr(self, expr):
        """
        Return a constant integer and the register it's stored in
        """
        reg = self.getFreeReg()
        code = "li {}, {}\n".format(reg, expr.getValue())
        return code, reg

    def charConstantExpr(self, expr):
        """
        Return a constant char and the register it's stored in
        """
        reg = self.getFreeReg()

        char_val = expr.getValue()[1:-1]  # strip '
        char_val = self.handleSpecialCharacters(char_val)

        code = "li {}, {}\n".format(reg, ord(char_val))
        return code, reg

    def stringConstantExpr(self, expr):
        """
            Return a a constant string and the register it's stored in
        """
        string = "\"" + self.handleSpecialCharacters(expr.getValue()) + "\""
        string_id = "string." + str(self.string_counter)
        self.string_counter += 1
        self.data_string += "{}: .asciiz {}\n".format(string_id, string)

        register = self.getFreeReg()
        return "la {}, {}\n".format(register, string_id), register

    def handleSpecialCharacters(self, string):
        string = string.replace("\\\\", "\\")
        string = string.replace("\\t", "\t")
        string = string.replace("\\n", "\n")
        string = string.replace("\\0", "\0")
        string = string.replace("\\'", "'")
        return string

    ################################### AST NODES ###################################

    def programNode(self, node: ProgramNode):
        """
            Process a program node. This will return the full .text segment.
        """

        code = ".text\n"

        # init zero reg to 0
        self.data_string += "float_zero: .float 0.0\n"

        code += "la $t0, float_zero\n"
        code += "lwc1 $f30, 0($t0)\n"

        code += "j func_main\n"  # jump to main function

        # discover function nodes
        for child in node.getChildren():
            if isinstance(child, FuncDef):
                # add function decl node to list of functions
                self.function_defs[child.getFuncID()] = child

        # process top level nodes
        for child in node.getChildren():
            child_code, child_reg = self.astNodeToMIPS(child)
            code += child_code

        # newline after data segment for clarity
        code = self.data_string + "\n" + code
        return code

    def varDeclDefault(self, node):
        # make room on stack and save offset

        # get scopename
        type, scopename = node.getSymbolTable().lookup(node.getID(), 0, False)

        # get full var id
        full_id = scopename + "." + node.getID()
        offset = self.incrementSpOffset()
        self.var_offset_dict[full_id] = ("$sp", offset)
        return "", -1

    def varDeclWithInit(self, node):
        expr_type = self.getMipsType(node.getInitExpr().getExpressionType())
        var_id = node.getID()
        var_type, table = node.getSymbolTable().lookup(var_id)
        var_type = self.getMipsType(var_type)
        code = ""
        is_global = node.getSymbolTable().isGlobal(var_id)

        if is_global and isinstance(node.getInitExpr(), ConstantExpr):
            value = self.convertConstant(var_type, expr_type, node.getInitExpr().getValue())

            if var_type == "byte" or var_type == "character":
                var_type = "word"

            self.data_string += "{}: .{} {}\n".format(var_id, var_type, value)
        elif is_global and isinstance(node.getInitExpr(), AddressExpr):
            addr_expr: AddressExpr = node.getInitExpr()

            if not isinstance(addr_expr.getTargetExpr(), IdentifierExpr):
                raise Exception("During global assignment only the address of variables can be taken.")

            id_name = addr_expr.getTargetExpr().getIdentifierName()

            self.data_string += "{}: .word {}\n".format(var_id, id_name)

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

        label = self.getUniqueLabelId()

        code = "cond_{}:\n".format(label)
        code += cond_code

        if is_float:
            # float must first be evaluated, then the bit must be checked
            code += "c.eq.s {}, {}\n".format(cond_reg, self.float_zero_reg)

            code += "bc1t else_branch_{}\n".format(label)
        else:
            # non-float, simple branch statement is enough
            # if the result is false => go to else
            code += "beqz {}, else_branch_{}\n".format(cond_reg, label)

        self.releaseReg(cond_reg)

        if_code, reg = self.astNodeToMIPS(node.getIfBody())
        else_code, reg = self.astNodeToMIPS(node.getElseBody())

        code += "if_branch_{}:\n".format(label)
        code += if_code

        # jump to end
        code += "j endif_{}\n".format(label)

        code += "else_branch_{}:\n".format(label)
        code += else_code

        # jump to end
        code += "j endif_{}\n".format(label)

        # end of branch statement
        code += "endif_{}:\n".format(label)

        return code, -1

    def whileStatement(self, node: WhileStmt):
        """
            Convert the while statement to MIPS code.
        """

        cond_code, cond_reg = self.astNodeToMIPS(node.getCondExpr())

        # check of the condition expression is float
        is_float = node.getCondExpr().getExpressionType().toString() == "float"

        cond_label_id = self.getUniqueLabelId()
        loop_label_id = self.getUniqueLabelId()
        endwhile_label_id = self.getUniqueLabelId()

        code = "cond_{}:\n".format(cond_label_id)
        self.most_recent_whilecond = "cond_{}".format(cond_label_id)

        code += cond_code

        if is_float:
            # float must first be evaluated, then the bit must be checked
            code += "c.eq.s {}, {}\n".format(cond_reg, self.float_zero_reg)

            code += "bc1t endwhile_{}\n".format(endwhile_label_id)
        else:
            # if the result is false => go to endwhile
            code += "beq {}, $0, endwhile_{}\n".format(cond_reg, endwhile_label_id)

        self.releaseReg(cond_reg)

        # only do body now that condition is done!
        body_code, body_reg = self.astNodeToMIPS(node.getBody())

        code += "loop_{}:\n".format(loop_label_id)

        code += body_code

        code += "j cond_{}\n".format(cond_label_id)

        code += "endwhile_{}:\n".format(endwhile_label_id)
        self.most_recent_endwhile = "endwhile_{}".format(endwhile_label_id)

        return code, -1

    def breakStatement(self, node: BreakStatement):

        code = "j {}\n".format(self.most_recent_endwhile)

        return code, -1

    def continueStatement(self, node: ContinueStatement):
        code = "j {}\n".format(self.most_recent_whilecond)

        return code, -1

    def statementContainer(self, node):
        # iterate over statements and process
        code = ""
        for child in node.getChildren():
            self.resetRegs()
            new_code, reg = self.astNodeToMIPS(child)
            code += new_code
            code += "\n"

        return code, -1

    def funcDef(self, node: FuncDef):
        # set the frame pointer offset to zero
        self.resetSpOffset()
        # $sp+0 now points to the top of the former stackframe

        # the stack structure at this moment
        """
            ----------
            old t3
            ----------
            old t2
            ----------
            old t1
            ----------
            old t0
            ----------
            old f4
            ----------
            old f3
            ----------
            old f2
            ----------
            old f1
            ----------
            old return addr
            ----------
            old frame_ptr
            ----------
            old stack_ptr
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
            ---------- <- $fp
            local_vars
            ---------- <- new $sp
        """

        function_doc = "\n### {} ###\n".format(node.getFuncID())

        # function label
        func_label = "func_{}:\n".format(node.getFuncID())

        fp_arg_offset = 0

        # add function params to offset dict
        for param in node.getParamList():
            param_name = param.getParamID()
            function_scopename = node.getSymbolTable().getName()

            self.var_offset_dict[function_scopename + "." + param_name] = ("$fp", fp_arg_offset)

            fp_arg_offset += 4

        # reset all registers.
        self.resetRegs()

        # function body
        # return value is placed into $v0 or $f31 by a return expression
        func_body, reg = self.astNodeToMIPS(node.getBody())

        # return
        if node.getFuncID() == "main":
            # syscall code 17 = exit2 (= exit with value)
            func_return = "li $v0, 17\n"

            # if there is a "return" statement in "main", its result is stored in $v0
            # if not, the programmer did something wrong and this is undefined behaviour.
            func_return += "move $a0, {}\n".format(self.return_reg)
            func_return += "syscall\n"
        else:
            func_return = "jr $ra\n"

        # adjust $sp at the beginning
        sp_adjust = "addi $sp, $sp, {}\n".format(self.getSpOffset())

        code = function_doc + func_label + sp_adjust + func_body + func_return

        # we don't return a register since a function definition does not return anything
        return code, -1

    def funcCallExprLooped(self, node: FuncCallExpr):
        code = ""

        code += "# call {}\n".format(node.getFunctionID().getIdentifierName())

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
            old f4
            ---------- <- old $sp-20
            old f3
            ---------- <- old $sp-24
            old f2
            ---------- <- old $sp-28
            old f1
            ---------- <- old $sp-32
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

        used_temp_regs = self.all_temp_regs.difference(self.free_regs)
        used_float_regs = self.all_float_regs.difference(self.free_float_regs)

        for used_reg in used_temp_regs:
            temp_offset -= 4
            code += self.storeRegister(used_reg, "$sp", temp_offset, is_float=False)

        for used_reg in used_float_regs:
            temp_offset -= 4
            code += self.storeRegister(used_reg, "$sp", temp_offset, is_float=True)

        # save old $ra
        temp_offset -= 4
        code += self.storeRegister("$ra", "$sp", temp_offset)

        # save old $fp
        temp_offset -= 4
        code += self.storeRegister("$fp", "$sp", temp_offset)

        # save old sp
        temp_offset -= 4
        code += self.storeRegister("$sp", "$sp", temp_offset)

        # calculate the new $fp:
        # fp_new = $sp + temp_offset - len(args)*4
        # this will accomodate the saving of $ra,$fp,$sp and the temp regs
        # we temporarily save it to $s0, so that parameter evaluation can still use the old $fp!
        code += "addi $s0, $sp, {}\n".format(temp_offset - len(node.getArguments()) * 4)

        fp_arg_offset = 0

        # save params on the stack relative to the $fp
        for i in range(0, len(node.getArguments())):
            funcdef_node = self.function_defs[node.getFunctionID().getIdentifierName()]
            param_name = funcdef_node.getParamList()[i].getParamID()

            code += "# process param {}\n".format(param_name)
            arg = node.getArguments()[i]
            arg_code, arg_reg = self.astNodeToMIPS(arg)
            code += arg_code

            # store param value relative to the new fp
            # this is temporarily $s0
            is_arg_float = arg.getExpressionType().toString() == "float"
            code += self.storeRegister(arg_reg, "$s0", fp_arg_offset, is_float=is_arg_float)

            fp_arg_offset += 4  # do this after since the $fp points to the a free stack place

            # here we don't add variables to the var offset dict, since they are not used within
            # the current function definition!

        # adjust $fp
        code += "move $fp, $s0\n"

        # note do this AFTER param evaluation, since the param eval still needs a working $sp!
        code += "move $sp, $fp\n"
        # $fp and $sp point now to the first parameter
        # the callee will adjust $sp to the end of the stackframe.

        # call function
        code += "jal func_{}\n".format(node.getFunctionID().getIdentifierName())

        sp_location_rel_to_fp = len(node.getArguments()) * 4

        # load $sp, this is just below the parameters relative to the current $fp
        code += "lw $sp, {}($fp)\n".format(sp_location_rel_to_fp)

        # load $ra
        code += "lw $ra, {}($fp)\n".format(sp_location_rel_to_fp + 8)

        # load $fp NOTE: do this last, since the loading of $fp, $ra, $sp depends on $fp
        code += "lw $fp, {}($fp)\n".format(sp_location_rel_to_fp + 4)

        temp_offset = 0
        for used_reg in used_temp_regs:
            temp_offset -= 4
            code += self.loadRegister("$sp", offset=temp_offset, is_float=False, target_reg=used_reg)

        for used_reg in used_float_regs:
            temp_offset -= 4
            code += self.loadRegister("$sp", offset=temp_offset, is_float=True, target_reg=used_reg)

        retval_type = node.getExpressionType()

        if retval_type.toString() == "float":
            ret_reg = self.getFreeFloatReg()
            # copy $f31 into ret_reg

            code += "mov.s {}, {}\n".format(ret_reg, self.float_return_reg)

        else:
            ret_reg = self.getFreeReg()
            # copy $v0 into ret_reg
            code += "move {}, {}\n".format(ret_reg, self.return_reg)

        return code, ret_reg

    def printfExpr(self, node: FuncCallExpr):
        """
            Process a call to printf()
        :param node: The FuncCallExpr object that represents the call to printf()
        :return: A pair (code, -1) with code being the MIPS code needed for a call to printf().
        """

        # TODO special case with one argument of type char*
        # simply retrieve the address from the var and doe syscall

        # get args
        args = node.getArguments()

        # get string
        string_expr = args.pop(0)
        if not isinstance(string_expr, StringConstantExpr):
            raise Exception("First argument to printf must be string constant.")

        formatted_string = string_expr.getValue()

        split_string = self.split_formatted_string(formatted_string)

        # annotate formatters with expressions
        annotated_formatters = self.pair_formatters_values(split_string, args)

        code = ""

        substring_counter = 0

        for value in annotated_formatters:

            if isinstance(value, str):
                # add string to data segment (label?)
                # do syscall to print string

                # %% is the escape for "%"
                value = value.replace("%%", "%")

                substring_id = "string.{}.{}".format(self.string_counter, substring_counter)
                substring_counter += 1

                # note manually add "
                substring_entry = "{}: .{} \"{}\"\n".format(substring_id, "asciiz", value)

                self.data_string += substring_entry

                # place argument
                code += "la $a0, {}\n".format(substring_id)
                code += "li $v0, 4\n"
                code += "syscall\n"

            else:
                formatter: str = value[0]
                argument_expr: Expression = value[1]
                arg_type = argument_expr.getExpressionType().toString()
                arg_is_float = (arg_type == "float")

                arg_code, arg_reg = self.astNodeToMIPS(argument_expr)

                code += arg_code

                # conversion
                if arg_is_float and formatter != "%f":
                    arg_conv_code, arg_reg = self.convertFloatToInteger(arg_reg)
                    code += arg_conv_code
                elif not arg_is_float and formatter == "%f":
                    arg_conv_code, arg_reg = self.convertIntegerToFloat(arg_reg)
                    code += arg_conv_code

                if formatter == "%d":

                    # place argument
                    code += "move $a0, {}\n".format(arg_reg)

                    # place syscall code
                    code += "li $v0, 1\n"

                    # make syscall
                    code += "syscall\n"

                elif formatter == "%f":
                    # place argument
                    code += "mov.s $f12, {}\n".format(arg_reg)

                    # place syscall code
                    code += "li $v0, 2\n"

                    # make syscall
                    code += "syscall\n"

                elif formatter == "%s":
                    # place argument
                    code += "move $a0, {}\n".format(arg_reg)

                    # place syscall code
                    code += "li $v0, 4\n"

                    # make syscall
                    code += "syscall\n"

                elif formatter == "%c":
                    # place argument
                    code += "move $a0, {}\n".format(arg_reg)

                    # place syscall code
                    code += "li $v0, 11\n"

                    # make syscall
                    code += "syscall\n"

                else:
                    raise Exception("Unknown formatter code '{}'.".format(formatter))

                self.releaseReg(arg_reg)

        self.string_counter += 1

        return code, -1

    def scanfExpr(self, node: FuncCallExpr):
        """
            Process a call to scanf().
        :param node: The FuncCallExpr object that represents the call to scanf()
        :return: A pair (code, -1) with code
        """

        code = ""

        # get args
        args = node.getArguments()

        if len(args) != 2:
            raise Exception("Invalid number of arguments for scanf. Expected 2, got {}.".format(len(args)))

        formatter_expr = args[0]
        target_expr = args[1]

        if not isinstance(formatter_expr, StringConstantExpr):
            raise Exception("First argument to scanf must be string constant.")

        formatter_str = formatter_expr.getValue()

        target_code, target_addr_reg = self.astNodeToMIPS(target_expr)
        # target_addr_reg contains the address where the value needs to be stored.

        code += target_code

        if formatter_str == "%d":
            code += "li $v0, 5\n"
            code += "syscall\n"
            code += self.storeRegister("$v0", target_addr_reg, 0, is_float=False)
        elif formatter_str == "%f":
            code += "li $v0, 6\n"
            code += "syscall\n"
            code += self.storeRegister("$f0", target_addr_reg, 0, is_float=True)
        elif formatter_str == "%s":
            code += "li $v0, 8\n"

            # $a0 contains the address of the string.
            code += "move $a0, {}\n".format(target_addr_reg)
            code += "li $a1, 256\n"

            code += "syscall\n"
        elif formatter_str == "%c":
            code += "li $v0, 12\n"
            code += "syscall\n"
            code += self.storeRegister("$v0", target_addr_reg, 0, is_float=False)
        else:
            raise Exception("Invalid formatter code for scanf: '{}'".format(formatter_str))

        return code, -1

    def split_formatted_string(self, string):
        """
            Split a formatted string into formatters and normal strings.
            Note that this does take into account the '%%' escape for '%' characters.

        :param string: The raw string passed to printf or scanf.
        :return: A list whose elements are either formatters (%f, %d, etc) or normal strings.
        """

        split = re.split(r'((?<!%)%[dfsc])', string)

        split = list(filter(lambda S: len(S) > 0, split))

        return split

    def pair_formatters_values(self, split_string, expression_list):
        """

        :param split_string: A list whose elements are either formatters (%f, %d, etc) or normal strings.
        :param expression_list: A list of Expression objects, one for each formatter in split_string
        :return: A list whose elements are substrings, or pairs (formatter, Expression).
        """

        retval = []

        for substring in split_string:
            if substring in ["%d", "%f", "%s", "%c"]:
                if len(expression_list) == 0:
                    raise Exception("Not enough expressions for printf string! Str: '{}'".format("".join(split_string)))

                # add pair
                retval.append((substring, expression_list.pop(0)))
            else:
                # add string
                retval.append(substring)

        return retval

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

    def modExpr(self, node: ModExpr) -> (str, str):
        """
            Process a modulo expression.
        """

        code = ""

        code_left, reg_left = self.astNodeToMIPS(node.getLeft())
        code_right, reg_right = self.astNodeToMIPS(node.getRight())

        code += code_left
        code += code_right

        # perform div
        code += "div {}, {}\n".format(reg_left, reg_right)

        self.releaseReg(reg_right)

        # take remainder
        code += "mfhi {}\n".format(reg_left)

        return code, reg_left

    def returnWithExprStatement(self, node: ReturnWithExprStatement):
        code = ""

        # resolve expression
        expr_code, expr_reg = self.astNodeToMIPS(node.getExpression())

        code += expr_code

        # required return type
        func_rettype_name = node.getFunctionType().getReturnTypeAsString()

        # expression type
        retval_typename = node.getExpression().getExpressionType().toString()

        if func_rettype_name == "float" and retval_typename != "float":
            # conversion

            conv_code, return_reg = self.convertFloatToInteger(expr_reg)

            code += conv_code
            code += "mov.s {}, {}\n".format(self.float_return_reg, return_reg)

            # no longer needed
            self.releaseReg(return_reg)

        elif func_rettype_name != "float" and retval_typename == "float":
            # conversion
            conv_code, return_reg = self.convertFloatToInteger(expr_reg)

            code += conv_code
            code += "move {}, {}\n".format(self.return_reg, return_reg)

            # no longer needed
            self.releaseReg(return_reg)

        else:  # types are equal
            if retval_typename == "float":
                code += "mov.s {}, {}\n".format(self.float_return_reg, expr_reg)
            else:
                code += "move {}, {}\n".format(self.return_reg, expr_reg)

            self.releaseReg(expr_reg)

        # this expression has a register, but it is a technical register that should not be used further
        return code, -1

    def comparisonExpr(self, node, int_op, float_op, reverse):
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
            # when dealing with floats, branches are necessary
            # no set operation for floats like slt
            code_left, reg_left = self.convertToType(reg_left, type_left, "float")
            code_right, reg_right = self.convertToType(reg_right, type_right, "float")

            code += code_left
            code += code_right

            label = self.getUniqueLabelId()
            register = self.getFreeReg()

            code += "{} {}, {}\n".format(float_op, reg_left, reg_right)

            true_value = 1 if not reverse else 0
            false_value = 0 if not reverse else 1

            code += "bc1t comp_true_{}\n".format(label)

            code += "comp_false_{}:\n".format(label)  # false
            code += "li {}, {}\n".format(register, false_value)
            code += "j comp_end_{}\n".format(label)

            code += "comp_true_{}:\n".format(label)  # true
            code += "li {}, {}\n".format(register, true_value)
            code += "j comp_end_{}\n".format(label)

            code += "comp_end_{}:\n".format(label)

            self.releaseReg(reg_left)
            self.releaseReg(reg_right)
            return code, register
        else:

            # re-use reg_left as destination address
            code += "{} {}, {}, {}\n".format(int_op, reg_left, reg_left, reg_right)
            self.releaseReg(reg_right)
            return code, reg_left

    def assignmentExpr(self, node):
        # array[element] = value has to be done differently
        if isinstance(node.getLeft(), ArrayAccessExpr):
            return self.arrayElementAssignment(node)

        code, register = self.astNodeToMIPS(node.getRight())
        right_type = self.getMipsType(node.getRight().getExpressionType())
        left_type = self.getMipsType(node.getLeft().getExpressionType())

        # don't do anything when assigning between bool and int
        if right_type == "byte" and left_type == "word":
            pass
        elif right_type == "word" and left_type == "byte":
            pass
        # type conversion
        elif right_type != left_type:
            convert, register = self.convertToType(register, right_type, left_type)
            code += convert
        else:
            pass

        code += self.storeVariable(register, node.getLeft())
        self.releaseReg(register)

        return code, -1

    def expressionStatement(self, node):
        code, register = self.astNodeToMIPS(node.getExpression())
        if register != -1:
            self.releaseReg(register)
        return code, -1

    def addressExpr(self, node: AddressExpr):

        target = node.getTargetExpr()
        if isinstance(target, IdentifierExpr):
            # variable
            # get variable from offset dict
            # retrieve information about the variable
            varname = target.getIdentifierName()
            vartype, varscope = node.getSymbolTable().lookup(varname, target.getNodecounter())
            full_id = varscope + "." + varname
            if not full_id in self.var_offset_dict:
                raise Exception("Variable with name '{}' is not present in offset list.".format(varname))

            # take register and offset, and add together to obtain
            # address
            reg, offset = self.var_offset_dict[full_id]
            addr_reg = self.getFreeReg()
            code = "addi {}, {}, {}\n".format(addr_reg, reg, offset)

            return code, addr_reg

        elif isinstance(target, ArrayAccessExpr):
            # array element
            # get array name
            #   -> get from offset dict
            # process index

            element_addr_code, element_addr_reg = self.arrayElementAddress(target)

            return element_addr_code, element_addr_reg

        else:
            raise Exception("Cannot take address of node with type '{}'".format(str(type(target))))

    def pointerDerefExpr(self, node: PointerDerefExpr):

        # *x means, take the address contained in x and perform lw on it.

        target = node.getTargetPtr()
        is_float = (target.getExpressionType().toString() == "float")
        if isinstance(target, IdentifierExpr):
            code = ""

            # get value stored at the identifier
            id_code, id_reg = self.astNodeToMIPS(target)
            code += id_code

            deref_code, deref_reg = self.loadRegister(id_reg, 0, is_float)
            code += deref_code

            self.releaseReg(id_reg)

            return code, deref_reg

        elif isinstance(target, ArrayAccessExpr):
            # get value stored in array entry

            code = ""

            arr_acc_code, arr_acc_reg = self.arrayElementAccess(target)
            code += arr_acc_code

            deref_code, deref_reg = self.loadRegister(arr_acc_reg, 0, is_float)
            code += deref_code

            self.releaseReg(arr_acc_reg)

            return code, deref_reg

        else:
            code, target_reg = self.astNodeToMIPS(target)
            load, register = self.loadRegister(target_reg, 0, is_float)
            code += load
            self.releaseReg(target_reg)  # no longer needed, and loadRegister
            # does not free the reg.
            return code, register

    def arrayDecl(self, node):
        # array size expression must be of a IntegerConstantExpression
        array_size = node.getSizeExpr().getValue()

        array_id = node.getID()
        array_type, table = node.getSymbolTable().lookup(array_id)
        array_type = self.getMipsType(array_type)
        code = ""
        is_global = node.getSymbolTable().isGlobal(array_id)
        if is_global:
            array_string = "{}: .{}".format(array_id, array_type)
            for i in range(0, array_size):
                array_string += " 0,"

            self.data_string += array_string[:-1] + "\n"

        else:
            # push new array to the stack using size
            # get full var id
            full_id = table + "." + array_id

            offset = self.getSpOffset()
            self.incrementSpOffset(array_size * 4)
            self.var_offset_dict[full_id] = ("$sp", offset)

        return code, -1

    def arrayElementAddress(self, node: ArrayAccessExpr):
        """
        Returns the address of an element of the array
        """
        """
        Example for global array:
        la $t3, array         # put address of array into $t3
        li $t2, 6            # put the index into $t2
        add $t2, $t2, $t2    # double the index
        add $t2, $t2, $t2    # double the index again (now 4x)
        add $t1, $t2, $t3    # combine the two components of the address
        """
        # get address of array
        # use add since otherwise extra register to store 4 is needed

        code, index_reg = self.astNodeToMIPS(node.getIndexArray())
        index_type = self.getMipsType(node.getIndexArray().getExpressionType())

        if index_type == "float":
            convert, index_reg = self.convertFloatToInteger(index_reg)
            code += convert

        identifier = node.getTargetArray().getIdentifierName()
        array_type, scopename = node.getSymbolTable().lookup(identifier, node.getTargetArray().getNodecounter())
        is_global = node.getSymbolTable().isGlobal(identifier)

        address_reg = self.getFreeReg()

        # put address of array into address_reg
        if is_global:
            code += "la {}, {}\n".format(address_reg, identifier)
        else:
            identifier = scopename + "." + identifier
            reg, offset = self.var_offset_dict[identifier]
            code += "addi {}, {}, {}\n".format(address_reg, reg, offset)

        # double the index twice ( = 4 * index)
        code += "add {}, {}, {}\n".format(index_reg, index_reg, index_reg)
        code += "add {}, {}, {}\n".format(index_reg, index_reg, index_reg)

        # combine the two components of the address
        code += "add {}, {}, {}\n".format(address_reg, address_reg, index_reg)

        self.releaseReg(index_reg)
        return code, address_reg

    def arrayElementAssignment(self, node):
        code = ""

        left_code, address_reg = self.arrayElementAddress(node.getLeft())
        right_code, value_reg = self.astNodeToMIPS(node.getRight())

        code += left_code
        code += right_code

        is_float = self.getMipsType(node.getRight().getExpressionType()) == "float"

        code += self.storeRegister(value_reg, address_reg, 0, is_float)
        self.releaseReg(address_reg)
        self.releaseReg(value_reg)

        return code, -1

    def arrayElementAccess(self, node):
        code, address_reg = self.arrayElementAddress(node)

        element_type = self.getMipsType(node.getExpressionType())
        is_float = element_type == "float"

        # load array element into register
        load, target_reg = self.loadRegister(address_reg, 0, is_float)
        code += load
        self.releaseReg(address_reg)
        return code, target_reg

    def castExpr(self, node):
        """
            Generate code to perform a cast to the specified type.
        """
        code, expr_reg = self.astNodeToMIPS(node.getExpr())  # convert expression to MIPS code

        # source_type = self.getMipsType(node.getExpr().getExpressionType())  # get type of expression
        # target_type = self.getMipsType(node.getTargetType())  # get target type

        source_type = node.getExpr().getExpressionType()  # get type of expression
        target_type = node.getTargetType()  # get target type

        # original code that uses get_mips type is NOT correct.
        # types such as "word", "character", "byte" are not relevant in this context.
        if target_type.toString() == "bool":
            convert, convert_reg = self.convertToBool(expr_reg)
            self.releaseReg(expr_reg)
        elif target_type.toString() == "float" and source_type.toString() != "float":
            convert, convert_reg = self.convertIntegerToFloat(expr_reg)
            # register already released
        elif target_type.toString() != "float" and source_type.toString() == "float":
            convert, convert_reg = self.convertFloatToInteger(expr_reg)
            # register already released
        else:
            # do nothing
            convert = ""
            convert_reg = expr_reg

        # else:
        #    convert, convert_reg = self.convertToType(expr_reg, source_type, target_type)  # perform conversion

        code += convert
        return code, convert_reg  # return code, and the location of the conversion

    def prefixArithmetics(self, node, operation):
        target = node.getExpr()
        expr_type = self.getMipsType(target.getExpressionType())
        code, register = self.astNodeToMIPS(target)

        operation = "{}.s".format(operation) if expr_type == "float" else operation

        constant = FloatConstantExpr(1.0) if expr_type == "float" else IntegerConstantExpr(1)

        constant_code, reg = self.astNodeToMIPS(constant)
        code += constant_code
        code += "{} {}, {}, {}\n".format(operation, register, register, reg)
        self.releaseReg(reg)

        if isinstance(target, IdentifierExpr):
            code += self.storeVariable(register, target)
            return code, register

        elif isinstance(target, ArrayAccessExpr):
            array_code, array_reg = self.arrayElementAddress(target)
            code += array_code
            code += self.storeRegister(register, array_reg, 0, expr_type == "float")
            self.releaseReg(register)

            return code, array_reg

        else:
            raise Exception("Prefix arithmetics aren't supported for type {}".format(type(target)))

    def postfixArithmetics(self, node, operation):
        target = node.getExpr()
        expr_type = self.getMipsType(target.getExpressionType())
        code, register = self.astNodeToMIPS(target)

        operation = "{}.s".format(operation) if expr_type == "float" else operation

        constant = FloatConstantExpr(1.0) if expr_type == "float" else IntegerConstantExpr(1)
        new_register = self.getFreeFloatReg() if expr_type == "float" else self.getFreeReg()
        constant_code, reg = self.astNodeToMIPS(constant)
        code += constant_code
        code += "{} {}, {}, {}\n".format(operation, new_register, register, reg)
        self.releaseReg(reg)

        if isinstance(target, IdentifierExpr):
            code += self.storeVariable(new_register, target)
            self.releaseReg(new_register)
            return code, register

        elif isinstance(target, ArrayAccessExpr):
            array_code, array_reg = self.arrayElementAddress(target)
            code += array_code
            code += self.storeRegister(new_register, array_reg, 0, expr_type == "float")
            self.releaseReg(new_register)
            self.releaseReg(array_reg)
            return code, register

        else:
            raise Exception("Prefix arithmetics aren't supported for type {}".format(type(target)))

    def logicBinopExpr(self, node, op) -> (str, str):
        """
         Process the logical and expression: x && y; x and y

         :param op: the operator. can be "and", "or"
        """

        code = ""

        # process left and right, and convert to bool
        code_left, reg_left = self.astNodeToMIPS(node.getLeft())
        code += code_left
        conv_left, left_bool_reg = self.convertToBool(reg_left)
        code += conv_left
        self.releaseReg(reg_left)

        code_right, reg_right = self.astNodeToMIPS(node.getRight())
        code += code_right
        conv_right, right_bool_reg = self.convertToBool(reg_right)
        code += conv_right
        self.releaseReg(reg_right)

        # perform and on the two bools
        code += "{} {}, {}, {}\n".format(op, left_bool_reg, left_bool_reg, right_bool_reg)

        self.releaseReg(right_bool_reg)

        return code, left_bool_reg

    def logicNotExpr(self, node: LogicNotExpr) -> (str, str):
        """
            Process a "not" expression.
        """

        target_code, target_reg = self.astNodeToMIPS(node.getExpr())
        bool_code, bool_reg = self.convertToBool(target_reg)
        self.releaseReg(target_reg)

        code = ""
        code += target_code
        code += bool_code

        code += "not {}, {}\n".format(bool_reg, bool_reg)
        # we do and on 1. This is since "0x00001" will be inverted to "0x11110"
        # we now need to set the other bits to zero.
        # also 0x00000 is converted into 0x11111, the other bits need to be set
        # to zero.
        code += "andi {}, {}, 1\n".format(bool_reg, bool_reg)

        return code, bool_reg

    ############################################# TYPE METHODS #############################################

    def convertIntegerToFloat(self, int_reg) -> (str, str):
        """
            Convert the specified integer register into an float value.
            Note: this will free the "int_reg" register.
        :param int_reg: The register that contains the integer value.
        :return: A tuple (code, reg) with "code" being the conversion code and "reg" the register with the float-value.
        """
        # mtc1 $t0, $f0 : copy $t0 to $f0
        # cvt.s.w FRdest, FRsrc : Convert Integer to Single
        float_reg = self.getFreeFloatReg()
        code = "mtc1 {}, {}\n".format(int_reg, float_reg)
        code += "cvt.s.w {}, {}\n".format(float_reg, float_reg)

        # int_reg isn't necessary anymore
        self.releaseReg(int_reg)
        return code, float_reg

    def convertFloatToInteger(self, float_reg) -> (str, str):
        """
            Convert the specified float register into an integer value.
            Note: this will free the "float_reg" register.
        :param float_reg: The register that contains the float value.
        :return: A tuple (code, reg) with "code" being the conversion code and "reg" the register with the integer-value.
        """
        # mfc1 $t0, $f0 : copy $f0 to $t0
        # cvt.w.s FRdest, FRsrcConvert Single to Integer
        int_reg = self.getFreeReg()
        code = "cvt.w.s {}, {}\n".format(float_reg, float_reg)
        code += "mfc1 {}, {}\n".format(int_reg, float_reg)

        # float_reg isn't necessary anymore
        self.releaseReg(float_reg)
        return code, int_reg

    def convertToBool(self, source_reg: str) -> (str, str):
        """
            Convert to value in the specified register to a boolean.

            The method will automatically detect if the register is
            a float or int reg.

            This means that source_reg will be compared to zero so that
                0x00000 -> False
                Anything else is True

        :return: (code, reg) with code being the conversion code and reg being a register with the result.
        """

        # check if it is a $f0-$f31 reg
        is_float = not (re.compile(r'^\$f\d+$').match(source_reg) is None)

        code = ""

        # request reg for result
        result_reg = self.getFreeReg()

        # id of branch label
        label_id = self.getUniqueLabelId()

        # compare to zero, float and int separately
        if is_float:
            code += "c.eq.s {}, {}\n".format(source_reg, self.float_zero_reg)
            code += "bc1t comp_iszero_{}\n".format(label_id)
        else:

            code += "beq {}, $zero, comp_iszero_{}\n".format(source_reg, label_id)

        # no branch, so non-zero -> return true
        code += "li {}, 1\n".format(result_reg)
        code += "j end_comp_{}\n".format(label_id)
        code += "comp_iszero_{}:\n".format(label_id)  # label for when the reg is zero.
        code += "li {}, 0\n".format(result_reg)
        code += "end_comp_{}:\n".format(label_id)

        return code, result_reg

    def convertToType(self, reg, old_type, new_type):
        if "float" in new_type and "float" not in old_type:
            return self.convertIntegerToFloat(reg)
        elif "float" in old_type and "float" not in new_type:
            return self.convertFloatToInteger(reg)
        else:
            return "", reg

    def convertConstant(self, new_type, old_type, value):
        if old_type == "byte":
            value = 1 if value else 0

        elif old_type == "character":
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
