from antlr4 import *
import sys

from antlr_files.CLexer import CLexer
from antlr_files.CListener import CListener
from antlr_files.CParser import CParser



def main(argv):
    in_stream = FileStream(argv[1])
    lexer = CLexer(in_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.program()
    printer = PrintListener()
    walker = ParseTreeWalker()

    print("digraph G {")
    walker.walk(printer, tree)
    print("}")

def rec_visit(cur_node, cur_id):
    """
    Recursive tree traverser. Starts at the specified node, and numbers each node starting with the given index.
    It will also printout graphviz dot code to visualise the tree.
    """
    i = cur_id
    if cur_node.getChildCount() > 0:
        rule_idx = cur_node.getRuleIndex()
        rule_name = CParser.ruleNames[rule_idx]
        print("\t{} [label=\"{}\"];".format(cur_id, rule_name))
        for child in cur_node.getChildren():
            print("\t{} -> {};".format(cur_id, i+1))
            i = rec_visit(child, i+1)
            
        # ENDFOR
    else:
        try:
            rule_idx = cur_node.getRuleIndex()
            rule_name = CParser.ruleNames[rule_idx]
        except:
            rule_name = "TERM"

        text = cur_node.getText()

        if text.endswith("\""):
            text = text[:-1]

        if text.startswith("\""):
            text = text[1:]
            
        print("\t{} [label=\"{}: '{}'\"];".format(cur_id, rule_name, text))
    # ENDIF

    return i
# ENDFUNCTION

class PrintListener(CListener):
    def enterProgram(self, ctx:CParser.ProgramContext):
        rec_visit(ctx, 0)
    # ENDMETHOD
# ENDCLASS


if __name__ == "__main__":
    main(sys.argv)
