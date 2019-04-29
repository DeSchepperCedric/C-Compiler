
class CompilerException(Exception):
    """
        Base class for exceptions thrown during the compilation process.
    """
    pass

class ParserException(CompilerException):
    """
        Exception thrown when an error occurs during parsing.
    """
    pass

class AstCreationException(CompilerException):
    """
        Exception thrown when an error occurs during AST tree creation.
    """
    pass

class AstTypingException(CompilerException):
    """
        Exception thrown when an error occurs during AST type checking.
    """
    pass

class AstPruningException(CompilerException):
    """
        Exception thrown when an error occurs while AST pruning w.r.t. 'return', 'contine', 'break'
    """
    pass