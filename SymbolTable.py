

class SymbolTable:

    table_counter = 0  # to name the tables

    def __init__(self, parent=None):
        self.name = 'T' + str(self.table_counter)
        SymbolTable.table_counter += 1
        self.parent = parent
        self.children = list()
        self.symbols = dict()

    def lookup(self, symbol, own_scope_only=False):
        """
        Lookup a symbol in the symbol table
        :param symbol: The symbol to be found
        :param own_scope_only: only check own scope or also parents
        :return: (0, None) when not found, (type, scope_name) when found.
        """
        # symbol found in current scope
        if symbol in self.symbols:
            return self.symbols[symbol], self.name

        # look for symbol in parent symbol table
        elif self.parent is not None and not own_scope_only:
            return self.parent.lookup(symbol, own_scope_only)

        # symbol isn't found
        else:
            return 0, None

    def insert(self, symbol, sym_type):
        """
        Insert a symbol in the symbol table
        :param symbol: symbol name
        :param sym_type: symbol type
        :return: None
        """
        self.symbols[symbol] = sym_type

    def allocate(self):
        """
        Allocate a new symbol table (new scope)
        :param name: table name
        :return: new symbol table
        """
        child = SymbolTable(self)
        self.children.append(child)
        return child

    def isGlobal(self, symbol):
        """
                Lookup a symbol in the symbol table
                :param symbol: The symbol to be found
                :param own_scope_only: only check own scope or also parents
                :return: 0 when not found, symbol type when found
                """
        # symbol found in current scope, and is global
        if symbol in self.symbols and self.parent is None:
            return True

        # symbol found in current scope, isn't global
        elif symbol in self.symbols:
            return False

        # look for symbol in parent symbol table
        elif self.parent is not None:
            return self.parent.isGlobal(symbol)

        # symbol isn't found
        else:
            return 0

    def getGlobalScope(self):
        """
            Retrieve the global scope. This is the scope in the scope tree that has no parent and is thus the root.
        """
        cur = self

        while(cur.parent is not None):
            cur = cur.parent

        return cur

    def toDot(self):
        """
        Print the symbol table in dot
        :return: A string that contains the representation of the symbol
        table in dot-format.
        """
        dot = "digraph G {\n"

        new_dot, i = recursive_symbol_table(parent=self, cur_id=0)
        dot += new_dot
        dot += "}\n"
        return dot

def recursive_symbol_table(parent, cur_id):
    """
    Print symbol table recursively
    :param parent: Parent of symbol table
    :param cur_id: current node id
    :return: dot, new id
    """
    i = cur_id
    dot = ""

    dot += print_symbol_table_node_to_dot(parent, cur_id)
    for child in parent.children:
        dot += "\t{} -> {};\n".format(cur_id, i + 1)
        new_dot, i = recursive_symbol_table(child, i + 1)
        dot += new_dot

    return dot, i


def print_symbol_table_node_to_dot(node, cur_id):
    """
    Print the node of a symbol table as html table
    :param node: symbol table
    :param cur_id: current node id
    :return: dot string
    """
    dot = "\t{} [\n\t shape=plaintext \n \tlabel=< <table border=\'0\' cellborder=\'1\' cellspacing=\'0\'\n\t>".format(cur_id)

    dot += "\t<tr><td colspan=\"2\"> {} </td></tr>\n".format(node.name)
    for symbol, sym_type in node.symbols.items():
        dot += "\t<tr>"
        if sym_type.isFunction():
            dot += "\t<td>{}</td>\n".format(sym_type.toString(True))
        else:
            dot += "\t<td>{}</td>\n".format(sym_type.toString())
        dot += "\t<td>{}</td>\n".format(symbol)
        dot += "\t</tr>\n"
    dot += "\t</table>  >];\n"
    return dot

class SymbolType:
    def __init__(self):
        pass

    def isFunction(self):
        return False

    def isArray(self):
        return False

    def isVar(self):
        return False

class FunctionType(SymbolType):
    def __init__(self, return_type : str, param_types : list, is_defined = False):
        """
            Constructor
        """
        self.return_type = return_type
        self.param_types = param_types
        self.is_defined = is_defined

    def getReturnTypeAsString(self):
        """
            Returns a string that represents the return type.
        """
        return self.return_type

    def getReturnType(self):
        """
            Returns a VariableType object that represents the return type.
        """
        return VariableType(self.return_type)

    def getParamTypes(self):
        return self.param_types

    def isFunction(self):
        return True

    def isDefined(self):
        return self.is_defined

    def setDefined(self):
        self.is_defined = True

    def toString(self, included_definition_flag=False):

        retval = self.return_type + "(" + ",".join(self.param_types) + ")"

        if included_definition_flag and self.is_defined:
            retval += "{def}"

        return retval

class VariableType(SymbolType):
    def __init__(self, variable_type : str):
        """
             Constructor.

             Params:
                'entry_type': String that contains the name of the type of the variable.
        """

        self.variable_type = variable_type

    def getVariableType(self):
        return self.variable_type

    def toString(self):
        return self.variable_type

    def isVar(self):
        return True

    def isPtr(self):
        return self.variable_type.endswith("*")

    def getUnderlayingPrimive(self):
        return VariableType(self.variable_type.rstrip("*"))

    def addPointerLayer(self):
        return VariableType(self.variable_type + "*")

    def removePointerLayer(self):
        if not self.isPtr():
            raise Exception("Pointer layer can only be removed if target is pointer.")

        return VariableType(self.variable_type[:-1])


class ArrayType(SymbolType):
    def __init__(self, entry_type : str):
        """
            Constructor.

            Params:
                'entry_type': String that contains the name of the type of the array entries.
        """
        self.entry_type = entry_type

    def getEntryTypeAsString(self):
        return self.entry_type

    def getEntryType(self):
        return VariableType(self.entry_type)

    def toString(self):
        return self.entry_type + "[]"

    def isArray(self):
        return True

def main():
    root = SymbolTable()
    root.insert("i", "int")
    root.insert("b", "float")

    child1 = root.allocate()

    child2 = child1.allocate()
    child2.insert("p", "int")

    child3 = root.allocate()
    child3.insert("i", "float")




if __name__ == "__main__":
    main()
