# Generated from ./C.g4 by ANTLR 4.7.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3$")
        buf.write("X\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16\t")
        buf.write("\16\3\2\6\2\36\n\2\r\2\16\2\37\3\3\3\3\3\3\3\3\3\4\3\4")
        buf.write("\3\4\3\4\3\4\5\4+\n\4\3\5\3\5\5\5/\n\5\3\6\3\6\3\6\3\6")
        buf.write("\3\6\5\6\66\n\6\3\7\3\7\3\7\5\7;\n\7\3\7\3\7\3\b\3\b\5")
        buf.write("\bA\n\b\3\t\3\t\3\t\3\t\3\n\3\n\3\n\3\13\3\13\3\f\3\f")
        buf.write("\3\r\7\rO\n\r\f\r\16\rR\13\r\3\r\3\r\3\16\3\16\3\16\2")
        buf.write("\2\17\2\4\6\b\n\f\16\20\22\24\26\30\32\2\4\3\2\7\n\3\2")
        buf.write("\"$\2Q\2\35\3\2\2\2\4!\3\2\2\2\6*\3\2\2\2\b.\3\2\2\2\n")
        buf.write("\65\3\2\2\2\f\67\3\2\2\2\16@\3\2\2\2\20B\3\2\2\2\22F\3")
        buf.write("\2\2\2\24I\3\2\2\2\26K\3\2\2\2\30P\3\2\2\2\32U\3\2\2\2")
        buf.write("\34\36\5\4\3\2\35\34\3\2\2\2\36\37\3\2\2\2\37\35\3\2\2")
        buf.write("\2\37 \3\2\2\2 \3\3\2\2\2!\"\5\26\f\2\"#\5\6\4\2#$\7\3")
        buf.write("\2\2$\5\3\2\2\2%&\5\b\5\2&\'\7\4\2\2\'(\5\6\4\2(+\3\2")
        buf.write("\2\2)+\5\b\5\2*%\3\2\2\2*)\3\2\2\2+\7\3\2\2\2,/\5\n\6")
        buf.write("\2-/\5\f\7\2.,\3\2\2\2.-\3\2\2\2/\t\3\2\2\2\60\66\5\30")
        buf.write("\r\2\61\62\5\30\r\2\62\63\7\35\2\2\63\64\5\24\13\2\64")
        buf.write("\66\3\2\2\2\65\60\3\2\2\2\65\61\3\2\2\2\66\13\3\2\2\2")
        buf.write("\678\7\13\2\28:\7\27\2\29;\5\20\t\2:9\3\2\2\2:;\3\2\2")
        buf.write("\2;<\3\2\2\2<=\7\30\2\2=\r\3\2\2\2>A\7\n\2\2?A\5\20\t")
        buf.write("\2@>\3\2\2\2@?\3\2\2\2A\17\3\2\2\2BC\5\22\n\2CD\7\4\2")
        buf.write("\2DE\5\20\t\2E\21\3\2\2\2FG\5\26\f\2GH\5\30\r\2H\23\3")
        buf.write("\2\2\2IJ\5\32\16\2J\25\3\2\2\2KL\t\2\2\2L\27\3\2\2\2M")
        buf.write("O\7\25\2\2NM\3\2\2\2OR\3\2\2\2PN\3\2\2\2PQ\3\2\2\2QS\3")
        buf.write("\2\2\2RP\3\2\2\2ST\7\13\2\2T\31\3\2\2\2UV\t\3\2\2V\33")
        buf.write("\3\2\2\2\t\37*.\65:@P")
        return buf.getvalue()


class CParser ( Parser ):

    grammarFileName = "C.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "';'", "','", "'#include'", "'<stdio.h>'", 
                     "'char'", "'int'", "'float'", "'void'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'if'", "'else'", 
                     "'return'", "'while'", "'+'", "'-'", "'*'", "'/'", 
                     "'('", "')'", "'['", "']'", "'{'", "'}'", "'='", "'>'", 
                     "'<'", "'=='" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "INCLUDE", 
                      "STDIO_H", "CHAR", "INT", "FLOAT", "VOID", "ID", "WS", 
                      "BLOCK_COMMENT", "LINE_COMMENT", "IF", "ELSE", "RETURN", 
                      "WHILE", "PLUS", "MINUS", "STAR", "DIVIDE", "LEFT_PAREN", 
                      "RIGHT_PAREN", "LEFT_BRACKET", "RIGHT_BRACKET", "LEFT_BRACE", 
                      "RIGHT_BRACE", "ASSIGNMENT", "GREATER", "LESS", "EQUAL", 
                      "CHAR_CONSTANT", "INTEGER_CONSTANT", "FLOATING_CONSTANT", 
                      "STRING_CONSTANT" ]

    RULE_program = 0
    RULE_declaration = 1
    RULE_init_decltr_list = 2
    RULE_declarator = 3
    RULE_var_decltr = 4
    RULE_func_decltr = 5
    RULE_param_spec = 6
    RULE_param_list = 7
    RULE_param = 8
    RULE_simpl_expr = 9
    RULE_types = 10
    RULE_var_decltr_id = 11
    RULE_constant = 12

    ruleNames =  [ "program", "declaration", "init_decltr_list", "declarator", 
                   "var_decltr", "func_decltr", "param_spec", "param_list", 
                   "param", "simpl_expr", "types", "var_decltr_id", "constant" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    INCLUDE=3
    STDIO_H=4
    CHAR=5
    INT=6
    FLOAT=7
    VOID=8
    ID=9
    WS=10
    BLOCK_COMMENT=11
    LINE_COMMENT=12
    IF=13
    ELSE=14
    RETURN=15
    WHILE=16
    PLUS=17
    MINUS=18
    STAR=19
    DIVIDE=20
    LEFT_PAREN=21
    RIGHT_PAREN=22
    LEFT_BRACKET=23
    RIGHT_BRACKET=24
    LEFT_BRACE=25
    RIGHT_BRACE=26
    ASSIGNMENT=27
    GREATER=28
    LESS=29
    EQUAL=30
    CHAR_CONSTANT=31
    INTEGER_CONSTANT=32
    FLOATING_CONSTANT=33
    STRING_CONSTANT=34

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CParser.DeclarationContext)
            else:
                return self.getTypedRuleContext(CParser.DeclarationContext,i)


        def getRuleIndex(self):
            return CParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)




    def program(self):

        localctx = CParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 26
                self.declaration()
                self.state = 29 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CParser.CHAR) | (1 << CParser.INT) | (1 << CParser.FLOAT) | (1 << CParser.VOID))) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclarationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def types(self):
            return self.getTypedRuleContext(CParser.TypesContext,0)


        def init_decltr_list(self):
            return self.getTypedRuleContext(CParser.Init_decltr_listContext,0)


        def getRuleIndex(self):
            return CParser.RULE_declaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclaration" ):
                listener.enterDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclaration" ):
                listener.exitDeclaration(self)




    def declaration(self):

        localctx = CParser.DeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31
            self.types()
            self.state = 32
            self.init_decltr_list()
            self.state = 33
            self.match(CParser.T__0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Init_decltr_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def declarator(self):
            return self.getTypedRuleContext(CParser.DeclaratorContext,0)


        def init_decltr_list(self):
            return self.getTypedRuleContext(CParser.Init_decltr_listContext,0)


        def getRuleIndex(self):
            return CParser.RULE_init_decltr_list

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInit_decltr_list" ):
                listener.enterInit_decltr_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInit_decltr_list" ):
                listener.exitInit_decltr_list(self)




    def init_decltr_list(self):

        localctx = CParser.Init_decltr_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_init_decltr_list)
        try:
            self.state = 40
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 35
                self.declarator()
                self.state = 36
                self.match(CParser.T__1)
                self.state = 37
                self.init_decltr_list()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 39
                self.declarator()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclaratorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def var_decltr(self):
            return self.getTypedRuleContext(CParser.Var_decltrContext,0)


        def func_decltr(self):
            return self.getTypedRuleContext(CParser.Func_decltrContext,0)


        def getRuleIndex(self):
            return CParser.RULE_declarator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclarator" ):
                listener.enterDeclarator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclarator" ):
                listener.exitDeclarator(self)




    def declarator(self):

        localctx = CParser.DeclaratorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_declarator)
        try:
            self.state = 44
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 42
                self.var_decltr()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 43
                self.func_decltr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Var_decltrContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def var_decltr_id(self):
            return self.getTypedRuleContext(CParser.Var_decltr_idContext,0)


        def ASSIGNMENT(self):
            return self.getToken(CParser.ASSIGNMENT, 0)

        def simpl_expr(self):
            return self.getTypedRuleContext(CParser.Simpl_exprContext,0)


        def getRuleIndex(self):
            return CParser.RULE_var_decltr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVar_decltr" ):
                listener.enterVar_decltr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVar_decltr" ):
                listener.exitVar_decltr(self)




    def var_decltr(self):

        localctx = CParser.Var_decltrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_var_decltr)
        try:
            self.state = 51
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 46
                self.var_decltr_id()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 47
                self.var_decltr_id()
                self.state = 48
                self.match(CParser.ASSIGNMENT)
                self.state = 49
                self.simpl_expr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Func_decltrContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(CParser.ID, 0)

        def LEFT_PAREN(self):
            return self.getToken(CParser.LEFT_PAREN, 0)

        def RIGHT_PAREN(self):
            return self.getToken(CParser.RIGHT_PAREN, 0)

        def param_list(self):
            return self.getTypedRuleContext(CParser.Param_listContext,0)


        def getRuleIndex(self):
            return CParser.RULE_func_decltr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunc_decltr" ):
                listener.enterFunc_decltr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunc_decltr" ):
                listener.exitFunc_decltr(self)




    def func_decltr(self):

        localctx = CParser.Func_decltrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_func_decltr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 53
            self.match(CParser.ID)
            self.state = 54
            self.match(CParser.LEFT_PAREN)
            self.state = 56
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CParser.CHAR) | (1 << CParser.INT) | (1 << CParser.FLOAT) | (1 << CParser.VOID))) != 0):
                self.state = 55
                self.param_list()


            self.state = 58
            self.match(CParser.RIGHT_PAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Param_specContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VOID(self):
            return self.getToken(CParser.VOID, 0)

        def param_list(self):
            return self.getTypedRuleContext(CParser.Param_listContext,0)


        def getRuleIndex(self):
            return CParser.RULE_param_spec

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParam_spec" ):
                listener.enterParam_spec(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParam_spec" ):
                listener.exitParam_spec(self)




    def param_spec(self):

        localctx = CParser.Param_specContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_param_spec)
        try:
            self.state = 62
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 60
                self.match(CParser.VOID)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 61
                self.param_list()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Param_listContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def param(self):
            return self.getTypedRuleContext(CParser.ParamContext,0)


        def param_list(self):
            return self.getTypedRuleContext(CParser.Param_listContext,0)


        def getRuleIndex(self):
            return CParser.RULE_param_list

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParam_list" ):
                listener.enterParam_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParam_list" ):
                listener.exitParam_list(self)




    def param_list(self):

        localctx = CParser.Param_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_param_list)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 64
            self.param()
            self.state = 65
            self.match(CParser.T__1)
            self.state = 66
            self.param_list()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def types(self):
            return self.getTypedRuleContext(CParser.TypesContext,0)


        def var_decltr_id(self):
            return self.getTypedRuleContext(CParser.Var_decltr_idContext,0)


        def getRuleIndex(self):
            return CParser.RULE_param

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParam" ):
                listener.enterParam(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParam" ):
                listener.exitParam(self)




    def param(self):

        localctx = CParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_param)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 68
            self.types()
            self.state = 69
            self.var_decltr_id()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Simpl_exprContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def constant(self):
            return self.getTypedRuleContext(CParser.ConstantContext,0)


        def getRuleIndex(self):
            return CParser.RULE_simpl_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimpl_expr" ):
                listener.enterSimpl_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimpl_expr" ):
                listener.exitSimpl_expr(self)




    def simpl_expr(self):

        localctx = CParser.Simpl_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_simpl_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 71
            self.constant()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypesContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(CParser.INT, 0)

        def FLOAT(self):
            return self.getToken(CParser.FLOAT, 0)

        def CHAR(self):
            return self.getToken(CParser.CHAR, 0)

        def VOID(self):
            return self.getToken(CParser.VOID, 0)

        def getRuleIndex(self):
            return CParser.RULE_types

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypes" ):
                listener.enterTypes(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypes" ):
                listener.exitTypes(self)




    def types(self):

        localctx = CParser.TypesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_types)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 73
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CParser.CHAR) | (1 << CParser.INT) | (1 << CParser.FLOAT) | (1 << CParser.VOID))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Var_decltr_idContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(CParser.ID, 0)

        def STAR(self, i:int=None):
            if i is None:
                return self.getTokens(CParser.STAR)
            else:
                return self.getToken(CParser.STAR, i)

        def getRuleIndex(self):
            return CParser.RULE_var_decltr_id

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVar_decltr_id" ):
                listener.enterVar_decltr_id(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVar_decltr_id" ):
                listener.exitVar_decltr_id(self)




    def var_decltr_id(self):

        localctx = CParser.Var_decltr_idContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_var_decltr_id)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 78
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==CParser.STAR:
                self.state = 75
                self.match(CParser.STAR)
                self.state = 80
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 81
            self.match(CParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConstantContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER_CONSTANT(self):
            return self.getToken(CParser.INTEGER_CONSTANT, 0)

        def FLOATING_CONSTANT(self):
            return self.getToken(CParser.FLOATING_CONSTANT, 0)

        def STRING_CONSTANT(self):
            return self.getToken(CParser.STRING_CONSTANT, 0)

        def getRuleIndex(self):
            return CParser.RULE_constant

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstant" ):
                listener.enterConstant(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstant" ):
                listener.exitConstant(self)




    def constant(self):

        localctx = CParser.ConstantContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_constant)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 83
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CParser.INTEGER_CONSTANT) | (1 << CParser.FLOATING_CONSTANT) | (1 << CParser.STRING_CONSTANT))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





