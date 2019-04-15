import sys

class SymbolTable:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = list()
        self.symbols = dict()

    def lookup(self, symbol):
        # symbol found in current scope
        if symbol in self.symbols:
            return self.symbols[symbol]

        # look for symbol in parent symbol table
        elif self.parent is not None:
            return self.parent.lookup(symbol)

        # symbol isn't found
        else:
            return 0


    def insert(self, symbol, sym_type):
        self.symbols[symbol] = sym_type

    def allocate(self, name):
        child = SymbolTable(name, self)
        self.children.append(child)
        return child


def print_symbol_table_to_dot(root):
    print("digraph G {")

    cur_id = 0
    recursive_symbol_table(root, cur_id)

    print("}")


def recursive_symbol_table(parent, cur_id):
    i = cur_id

    print_symbol_table_node_to_dot(parent, cur_id)

    for child in parent.children:
        print("\t{} -> {};".format(cur_id, i + 1))
        i = recursive_symbol_table(child, i + 1)

    return i

def print_symbol_table_node_to_dot(node, cur_id):
    print("\t{} [\n shape=plaintext \nlabel=< <table border=\'0\' cellborder=\'1\' cellspacing=\'0\'>".format(cur_id))

    print("\t<tr><td colspan=\"2\"> {} </td></tr>".format(node.name))
    for symbol, type in node.symbols.items():
        print("\t<tr>")
        print("\t<td>{}</td>".format(type))
        print("\t<td>{}</td>".format(symbol))
        print("\t</tr>")
    print("\t</table>  >];")


def main(argv):
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
    main(sys.argv)



