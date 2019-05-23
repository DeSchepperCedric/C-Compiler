from ASTTreeNodes import *
import struct as struct
from itertools import zip_longest


class MipsGenerator:
    def __init__(self):
        self.cur_reg = 0
        self.variable_reg = dict()
        self.reg_stack = list()
        self.data_string = ".data: \n"
        self.string_counter = 0
        self.reg_to_string = dict()
        self.array_sizes = dict()

        self.temporaries = [i for i in range(7, -1, -1)]
        self.saved = [i for i in range(7, -1, -1)]
        self.floats = [i for i in range(31, -1, -1)]
        self.stack_ptr = 0

        # maps scope_name.var_name to an offset relative to the frame pointer
        self.var_offset_dict = dict()

        self.fp_offset = 0 # offset to current frame pointer

        self.label_counter = 0
        self.free_regs = ["$t0", "$t1", "$t2", "$t3"]
        self.free_float_regs = ["$f0", "$f1", "$f2", "$f3"]

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

    def releaseReg(self, reg):
        """
            Mark the specified temp register as available.
        """
        if reg in self.free_regs:
            raise Exception("Error when releasing reg '{}': register is already free.".format(reg))

        if not reg.startswith("$t"):
            raise Exception("Specified register '{}' is not a temp register.".format(reg))

        self.free_regs.append(reg)

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


    def getFpOffset(self):
        """
            Retrieve the current fp offset.
        """
        return self.fp_offset

    def pushFpOffset(self):
        """
            Adjust the fp offset to accomodate one more variable on the stack.

            :return: The new value of the fp offset.
        """

        # 4 bytes
        self.fp_offset -= 4;

        return self.fp_offset

    def popFpOffset(self):
        """
            Adjust the fp offset to remove one variable from the stack.
            :return: The new value of the fp offset.
        """

        self.fp_offset += 4;

        return self.fp_offset

    def resetFpOffset(self):
        """
            Reset the fp offset to 0.
        """
        
        self.fp_offset = 0

    def storeRegister(self, source_reg:str, addr_reg:str, offset, is_float=False) -> str:
        """
            Store the specified register in memory at the specified address.

            Params:
                'source_reg': the register that contains the value that will be stored.
                'addr_reg': the register that contains the address where the value will be stored.
                'offset': the offset that will be added to the address stored in 'addr_reg'. Specify as integer.
        """

        if is_float and not source_reg.startswith("$f"):
            raise Exception("Error when trying to store non-float register {} as float.".format(source_reg))

        if not is_float and source_reg.startswith("$f"):
            raise Exception("Error when trying to store float register {} as non-float.".format(source_reg))

        command = "sw" if not is_float else "swc1"

        return "{} {}, {}({})\n".format(command, source_reg, offset, addr_reg)

    def loadRegister(self, target_reg: str, addr_reg:str, offset, is_float = False) -> str:
        """
            Load the value stored in the memory at the specified address into the specified register.

            Params:
                'target_reg': The register that will contain the value.
                'addr_reg': The register that contains the address at which the value is stored.
                'offset': the offset that will be added to the address stored in 'addr_reg'. Specify as integer.
        """

        if is_float and not target_reg.startswith("$f"):
            raise Exception("Error when trying to load float into non-float register {}.".format(target_reg))

        if not is_float and target_reg.startswith("$f"):
            raise Exception("Error when trying to load non-float into float register {}.".format(target_reg))

        command = "lw" if not is_float else "lwc1"

        return "{} {}, {}({})\n".format(command, target_reg, offset, addr_reg)

    def storeVariable(self, source_reg, id_node : IdentifierExpr):

        # get varname
        varname = id_node.getIdentifierName()

        # determine if the variable is a float
        if id_node.getExpressionType() == "float":
            is_float = True
        else:
            is_float = False

        # determine whether the variable is a global:
        is_global = id_node.getSymbolTable().isGlobal(varname)

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
            type, scopename = id_node.getSymbolTable().lookup(varname, False)

            # get full var id
            full_id = scopename + "." + varname

            # determine if the variable already is stored on the stack
            if full_id in self.var_offset_dict:
                # retrieve offset and store

                offset = self.var_offset_dict[full_id]

                code = self.storeRegister(source_reg, "$fp", offset, is_float)

                return code
            else:
                # push new variable to the stack

                cur_offset = self.getFpOffset()

                code = self.storeRegister(source_reg, "$fp", cur_offset, is_float)

                # adjust fp offset for new variable
                new_offset = self.pushFpOffset()

                return code

    def loadVariable(self, id_node):

        # get offset

        pass

    def astNodeToMIPS(self, node):
        """
            Returns a tuple (code, reg) with code being the MIPS code and reg 
            being the register that contains the result.
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

    ################################### CONSTANT EXPRESSIONS ###################################

    def boolConstantExpr(self, expr):
        """
        Return a constant bool with its type and the register it's stored in
        """

        # add to data segment

        pass

    def floatConstantExpr(self, expr):
        """
        Return a constant float with its type and the register it's stored in
        """

        # add to data segment
        pass

    def integerConstantExpr(self, expr):
        """
        Return a constant integer with its type and the register it's stored in
        """
        # add to data segment
        pass

    def charConstantExpr(self, expr):
        """
        Return a constant integer with its type and the register it's stored in
        """
        # add to data segment
        pass

    def stringConstantExpr(self, expr):
        # add to data segment
        pass

    ################################### AST NODES ###################################

    def programNode(self, node):
        """
            Process a program node. This will return the full .text segment.
        """

        code = ".text\n"

        # discover functions

        # main function first!

        # other functions


        return code, -1

    def varDeclDefault(self, node):
        pass

    def varDeclWithInit(self, node):
        expr_type = self.getMipsType(node.getInitExpr().getExpressionType())
        var_id = node.getID()
        var_type, table = node.getSymbolTable().lookup(var_id)
        var_type = self.getMipsType(var_type)
        code = ""
        is_global = node.getSymbolTable().isGlobal(var_id)

        if is_global and isinstance(node.getInitExpr(), ConstantExpr):
            value = self.convertConstant(var_type, expr_type, node.getInitExpr().getValue())
            self.data_string += "{}: .{} {}".format(var_id, var_type, value)

        elif is_global and isinstance(node.getInitExpr(), AddressExpr):
            pass

        else:
            pass

    def branchStatement(self, node):
        """
            Convert an BranchStmt to MIPS code.
        """

        ## process children ##
        # retrieve condition code
        cond_code, cond_reg = self.astNodeToMIPS(node.getCondExpr())

        if_code,   reg = self.astNodeToMIPS(node.getIfBody())
        else_code, reg = self.astNodeToMIPS(node.getElseBody())

        cond_label_id = self.getUniqueLabelId()
        if_label_id = self.getUniqueLabelId()
        else_label_id = self.getUniqueLabelId()
        endif_label_id = self.getUniqueLabelId()

        code = "cond_{}:\n".format(cond_label_id)
        code += cond_code

        # if the result is false => go to else
        code += "beq {} $0 else_branch_{}\n".format(cond_reg, else_label_id)

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

    def whileStatement(self, node):
        """
            Convert the while statement to MIPS code.
        """

        cond_code, cond_reg = self.astNodeToMIPS(node.getCondExpr())
        body_code, body_reg = self.astNodeToMIPS(node.getIfBody())

        cond_label_id     = self.getUniqueLabelId()
        loop_label_id     = self.getUniqueLabelId()
        endwhile_label_id = self.getUniqueLabelId()

        code = "cond_{}:\n".format(cond_label_id)
        code += cond_code

        # if the result is false => go to endwhile
        code += "beq {} $0 endwhile_{}:\n".format(cond_reg, endwhile_label_id)

        code += "loop_{}:\n".format(loop_label_id)
        code += body_code

        code += "j cond_{}:\n".format(cond_label_id)

        code += "endwhile_{}:\n".format(endwhile_label_id)

        return code, -1

    def statementContainer(self, node):
        # iterate over statements and process
        # if a return with expression is encountered, use that expression's register as return register for this function call
        pass

    def funcParam(self, node):
        # ignore
        pass

    def funcDecl(self, node):
        # ignore
        pass

    def funcDef(self, node):
        fp_offset = 0

        code = ""
        return_reg = ""

        # function label
        function_name = node.getFuncID()

        code += "{}:\n".format(function_name)


        # load params from stack

        # TODO params need to be loaded from stack
        # function body
        func_body, reg = self.astNodeToMIPS(node.getBody())
        code += func_body

        # return
        code += "jr $ra\n"

        # we don't return a register since a function definition
        # does not return anything
        return code, -1

    def funcCallExpr(self, node):
        code = ""

        # save t0-t3 registers to stack
        for reg in ["$t0", "$t1", "$t2", "$t3"]:
            # TODO check if correct
            # TODO store reg on the stack
            # increment stack pointer?
            code += self.storeRegister(reg, "$sp", 0)

        # resolve each argument expression
        for arg in node.getArguments():
            arg_code, arg_reg = self.astNodeToMIPS(arg)

            # TODO store reg on the stack
            # increment stack pointer?
            code += arg_code
            code += self.storeRegister(arg_reg, "$sp", 0)

        # save return value on stack
        code += self.storeRegister("$ra", "$sp", 0)

        # jump and link
        code += "jal {}\n".format(node.getFunctionID().getIdentifierName())

        code += self.loadRegister("$ra", "$sp", 0)

        # restore registers from stack
        for reg in ["$t0", "$t1", "$t2", "$t3"]:
            # TODO decrement stackptr?
            # TODO check
            code += self.loadRegister(reg, "$sp", 0)

        # TODO do something with return value, return register?

        return code, ret_reg

    def identifierExpr(self, node):
        # ignore?
        pass

    def arithmeticExpr(self, node, operation):
        # dest = src1 op src2
        # op dest, src, src2
        # int -> op
        # float ->  op + ".s"
        pass

    def returnStatement(self):
        # ignore
        pass

    def returnWithExprStatement(self, node):
        # resolve expression
        # return register
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

    def arrayDecl(self, node):
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

    ############################################# TYPE METHODS #############################################

    def arrayAccessHelperString(self, reg_to, reg_from, element_type, index, is_global):
        pass

    def getStrongestType(self, a, b):
        INTREP = ["int", "word"]
        CHARREP = ["char", "character"]
        BOOLREP = ["bool", "byte"]

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
        """ Converts a symbolType to an LLVM type"""
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
