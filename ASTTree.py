
class ASTNode:
    """
        Class that represents a node in an AST tree.
    """

    def __init__(self):
        self.parent = None
        self.children = []
    # ENDCTOR

    def getParent(self):
        return self.parent
    # ENDMETHOD

    def getChildren(self):
        return self.children
    # ENDMETHOD
# ENDCLASS

# program:
#   list of "include","func_decl", "func_def"

# include: opaque node

# func declaration
#   "type", "id_with_ptr", list of "param"

# var declaration
#   "type", "id_with_ptr", "decl_typ"={ID_DECL, ARRAY_DECL, ID_DECL_INIT}", opt:array_size_expr, opt:init_expr

# func_def:
#   "type", "id_with_ptr", list of "param", "compound_statement"
# !!! indien er ergens een return statement is, alles daarna moet weg

# id_with_ptr:
#   "pointer_count" "id"

# param:
#   "type", "id_with_ptr"

# compound_statement:
#   list of "statement":

#  while statement
#   "condition", "body"
#   in body: alles na "continue" weg, alles na "break" weg

# for statement
#   "init", "condition", "iter", "body"
#   in body: alles na "continue" weg, alles na "break" weg

# if statement
#   "branch", "if_body", "else_body"

# expression_statement
# ???







