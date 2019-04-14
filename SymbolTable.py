

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







