grammar C;

program : top_level_node+ EOF;

top_level_node
        : include
        | declaration SC
        | func_def SC?
        ;

// include for <stdio.h>
include : INCLUDE STDIO_H ;

/// a declaration introduces one or more identifiers into the program
declaration : prim_type declarator (COMMA declarator)*;

/// a declarator introduces one identifier into the program
declarator
        : id_with_ptr LEFT_PAREN (param (COMMA param)*)? RIGHT_PAREN  # funcDecl
        | id_with_ptr                                                 # varDeclSimple
        | id_with_ptr LEFT_BRACKET assignment_expr RIGHT_BRACKET      # varDeclArray
        | id_with_ptr ASSIGNMENT assignment_expr                      # varDeclInit
        ; 

// function declarator
param : prim_type id_with_ptr;

// function definition
func_def : prim_type id_with_ptr LEFT_PAREN (param (COMMA param)*)? RIGHT_PAREN compound_statement ;

// different types of statements
statement
        : if_statement
		| compound_statement
		| iteration_statement
		| expression_statement
		| jump_statement
		;

if_statement: IF LEFT_PAREN assignment_expr RIGHT_PAREN statement (ELSE statement)? ;

iteration_statement
        : WHILE LEFT_PAREN assignment_expr RIGHT_PAREN statement  # WhileLoop
	    | FOR LEFT_PAREN for_condition RIGHT_PAREN statement      # forLoop
	    ;

// note: usually the conditions in forloops can be multiple expressions, but these
// are ignored anyway so we leave them out.
for_condition
	: declaration SC assignment_expr? SC expression? 
	| expression? SC assignment_expr? SC expression? 
	;

compound_statement : LEFT_BRACE block_item* RIGHT_BRACE ;
block_item
        : statement      # blockItemStatement
        | declaration SC # blockItemDeclaration
        ;

jump_statement
	    : RETURN SC                        # jumpReturn
        | RETURN assignment_expr? SC       # jumpReturnWithExpr
	    | BREAK SC                         # jumpBreak
        | CONTINUE SC                      # jumpContinue
        ;

expression_statement : expression? SC ;

// expression
expression : assignment_expr (COMMA assignment_expr)* ;


assignment_expr
        : logical_or_expr
		| unary_expr assignment_operator logical_or_expr
	    ;

assignment_operator
        : ASSIGNMENT
        | ADD_ASSIGN
        | SUB_ASSIGN
        | MUL_ASSIGN
        | DIV_ASSIGN
        ;

logical_or_expr
        : logical_and_expr
        | logical_or_expr OR logical_and_expr
        ;

logical_and_expr
        : equality_expr
        | logical_and_expr AND equality_expr
        ;

equality_expr
        : relational_expr
    	| equality_expr EQUAL relational_expr
    	| equality_expr NOT_EQUAL relational_expr
	    ;

relational_expr
        : additive_expr
        | relational_expr LESS_THAN additive_expr
        | relational_expr GREATER_THAN additive_expr
        | relational_expr GREATER_EQUAL_THAN additive_expr
        | relational_expr LESS_EQUAL_THAN additive_expr
        ;

additive_expr
        : multiplicative_expr
	    | additive_expr PLUS  multiplicative_expr
	    | additive_expr MINUS multiplicative_expr
	    ;

multiplicative_expr : cast_expr
					| multiplicative_expr STAR cast_expr
					| multiplicative_expr DIVIDE cast_expr
					| multiplicative_expr MOD cast_expr
					;


cast_expr: (LEFT_PAREN prim_type RIGHT_PAREN)* unary_expr;

unary_expr // note: does not get visited
        : postfix_expr             # unaryAsPostfix
        | unary_operator cast_expr # unaryOp
        ;

unary_operator
        : PLUS
        | MINUS
        | pointer // dereference
        | NOT
        | AMPERSAND // address
        | DECREMENT // --x
        | INCREMENT // ++x
        ;

postfix_expr
        : identifier LEFT_BRACKET assignment_expr RIGHT_BRACKET   # arrayAccesExpr // we use assignment_expr here since "expression" is a list
        | postfix_expr DECREMENT                                  # postfixDec
        | postfix_expr INCREMENT                                  # postfixInc
        | identifier LEFT_PAREN expression? RIGHT_PAREN           # funcCall
        | prim_expr                                               # primitiveExpr
        ;

prim_expr : LEFT_PAREN assignment_expr RIGHT_PAREN # parenExpr
		  | identifier                             # idExpr
		  | constant                               # constantExpr
          ;

//-----------------------------------------------------------------------------------------------

prim_type
        : type_int
        | type_float
        | type_char
        | type_void 
        | type_bool
        ;
	  
type_int   : INT ;
type_float : FLOAT ;
type_char  : CHAR ;
type_void  : VOID ;
type_bool  : BOOL ;

// an identifier that has a pointer
id_with_ptr : pointer* identifier;
identifier  : ID ;
pointer     : STAR ; 

constant : int_constant 
         | float_constant 
         | str_constant 
         | char_constant
         | bool_constant 
         ;

int_constant   : INTEGER_CONSTANT ;
float_constant : FLOAT_CONSTANT ;
str_constant   : STRING_CONSTANT ;
char_constant  : CHAR_CONSTANT ;
bool_constant  : BOOL_CONSTANT ;

INCLUDE : '#include';
STDIO_H : '<stdio.h>';

// types
CHAR  : 'char';
INT   : 'int';
FLOAT : 'float';
VOID  : 'void';
BOOL  : 'bool';

COMMA : ',';
SC    : ';';

IF       : 'if';
ELSE     : 'else';
RETURN   : 'return';
WHILE    : 'while';
BREAK    : 'break';
CONTINUE : 'continue';
FOR      : 'for';

//operations
INCREMENT : '++';
DECREMENT : '--';

PLUS   : '+';
MINUS  : '-';
STAR   : '*';
DIVIDE : '/';
MOD    : '%';

LEFT_PAREN    : '(';
RIGHT_PAREN   : ')';
LEFT_BRACKET  : '[';
RIGHT_BRACKET : ']';
LEFT_BRACE    : '{';
RIGHT_BRACE   : '}';

EQUAL         : '==';
NOT_EQUAL     : '!=';

ASSIGNMENT : '=';
ADD_ASSIGN : '+=';
SUB_ASSIGN : '-=';
MUL_ASSIGN : '*=';
DIV_ASSIGN : '/=';

AND : '&&' | 'and';
OR  : '||' | 'or';
NOT : '!' | 'not'; // must be before '!=' for precedence reasons.

// must be after '&&' for precedence reasons.
AMPERSAND : '&';

GREATER_THAN       : '>';
LESS_THAN          : '<';
GREATER_EQUAL_THAN : '>=';
LESS_EQUAL_THAN    : '<=';

// escapes like '\n'. This is a backslash followed by a specific set of characters.
fragment ESCAPED_CHAR : '\\' ['"?abfnrtv\\] ;

// character that belongs in a character literal
fragment CHARACTER_CHAR : ~['\\\r\n]
                        | ESCAPED_CHAR
                        ;

// character that belongs in a string literal
fragment STRING_CHAR : ~["\\\r\n]
                     | ESCAPED_CHAR
                     ;

BOOL_CONSTANT    : 'true' | 'false';
INTEGER_CONSTANT : [0-9][0-9]*;
FLOAT_CONSTANT   : [0-9]* '.' [0-9]+;
CHAR_CONSTANT    : '\'' CHARACTER_CHAR+ '\'';
STRING_CONSTANT  : '"' STRING_CHAR* '"'; // expansion might be needed

BLOCK_COMMENT : '/*' .*? '*/' -> skip;
LINE_COMMENT  : '//' ~[\r\n]* -> skip;

// keep this at the BOTTOM of the lexer. The identifier DFA will match almost anything, and thus has
// to have the LOWEST priority because otherwise no other tokens will be matched!
ID : [a-zA-Z_][a-zA-Z0-9_]*;
WS : [ \t\r\n]+ -> skip; // skip spaces, tabs, newlines



