

class SymbolTable:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = list()
        self.symbols = dict()

    def lookup(self, symbol, own_scope_only=False):
        """
        Lookup a symbol in the symbol table
        :param symbol: The symbol to be found
        :param own_scope_only: only check own scope or also parents
        :return: 0 when not found, symbol type when found
        """
        # symbol found in current scope
        if symbol in self.symbols:
            return self.symbols[symbol]

        # look for symbol in parent symbol table
        elif self.parent is not None and not own_scope_only:
            return self.parent.lookup(symbol, own_scope_only)

        # symbol isn't found
        else:
            return 0

    def insert(self, symbol, sym_type):
        """
        Insert a symbol in the symbol table
        :param symbol: symbol name
        :param sym_type: symbol type
        :return: None
        """
        self.symbols[symbol] = sym_type

    def allocate(self, name):
        """
        Allocate a new symbol table (new scope)
        :param name: table name
        :return: new symbol table
        """
        child = SymbolTable(name, self)
        self.children.append(child)
        return child


def print_symbol_table_to_dot(root):
    """
    Print the symbol table in dot
    :param root: Symbol table root
    :return: None
    """
    print("digraph G {")

    cur_id = 0
    recursive_symbol_table(root, cur_id)

    print("}")


def recursive_symbol_table(parent, cur_id):
    """
    Print symbol table recursively
    :param parent: Parent of symbol table
    :param cur_id: current node id
    :return: new id
    """
    i = cur_id

    print_symbol_table_node_to_dot(parent, cur_id)

    for child in parent.children:
        print("\t{} -> {};".format(cur_id, i + 1))
        i = recursive_symbol_table(child, i + 1)

    return i


def print_symbol_table_node_to_dot(node, cur_id):
    """
    Print the node of a symbol table as html table
    :param node: symbol table
    :param cur_id: current node id
    :return: None
    """
    print("\t{} [\n shape=plaintext \nlabel=< <table border=\'0\' cellborder=\'1\' cellspacing=\'0\'>".format(cur_id))

    print("\t<tr><td colspan=\"2\"> {} </td></tr>".format(node.name))
    for symbol, sym_type in node.symbols.items():
        print("\t<tr>")
        print("\t<td>{}</td>".format(sym_type))
        print("\t<td>{}</td>".format(symbol))
        print("\t</tr>")
    print("\t</table>  >];")


def main():
    root = SymbolTable("root")
    root.insert("i", "int")
    root.insert("b", "float")

    child1 = root.allocate("child1")

    child2 = child1.allocate("child2")
    child2.insert("p", "int")

    child3 = root.allocate("child3")
    child3.insert("i", "float")

    print_symbol_table_to_dot(root)


if __name__ == "__main__":
    main()
