from antlr4 import *
from antlr4.error import *
import sys
from Logger import Logger

class ParserErrorListener(ErrorListener.ErrorListener):

    def __init__(self):
        self.has_errored = False

    def hasErrored(self):
        return self.has_errored

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.has_errored = True
        Logger.error("line " + str(line) + ":" + str(column) + " " + msg)
