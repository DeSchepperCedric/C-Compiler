grammar C;

program : (include | declaration SC | func_def)+ EOF;

// include for <stdio.h>
include : INCLUDE STDIO_H ;

/// a declaration introduces one or more identifiers into the program
declaration : types init_decltr_list;
init_decltr_list : declarator (COMMA declarator)*;

/// a declarator introduces one identifier into the program
declarator
        : var_decltr
        | func_decltr;

// variable declarator
var_decltr
        : id_with_ptr
        | id_with_ptr LEFT_BRACKET expression RIGHT_BRACKET
        | id_with_ptr ASSIGNMENT expression // assignment can happen at time of declaration: "int i = 5; char* j = &k", etc.
        ; 

// function declarator
func_decltr : id_with_ptr LEFT_PAREN (param (COMMA param)*)? RIGHT_PAREN;
param : types id_with_ptr;

// function definition
func_def : types id_with_ptr LEFT_PAREN (param (COMMA param)*)? RIGHT_PAREN compound_statement ;

// different types of statements
statement
        : if_statement
		| compound_statement
		| iteration_statement
		| expression_statement
		| jump_statement
		;

if_statement: IF LEFT_PAREN expression RIGHT_PAREN statement (ELSE statement)? ;

iteration_statement
        : WHILE LEFT_PAREN expression RIGHT_PAREN statement
	    | FOR LEFT_PAREN for_condition RIGHT_PAREN statement
	    ;

for_condition
	: declaration SC expression? SC expression?
	| expression? SC expression? SC expression?
	;

compound_statement : LEFT_BRACE block_item* RIGHT_BRACE ;
block_item
        : statement
        | declaration
        ;

jump_statement
	    : RETURN SC
	    | BREAK SC
        | CONTINUE SC
        ;

expression_statement : expression? SC ;

// expression
expression : assignment_expr (COMMA expression)* ;

assignment_expr
        : logical_or_expr
		| unary_expr assignment_operator assignment_expr
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


cast_expr: (LEFT_PAREN types RIGHT_PAREN)* unary_expr;

unary_expr
        : postfix_expr
        | DECREMENT unary_expr
        | INCREMENT unary_expr
        | unary_operator cast_expr
        ;

unary_operator
        : PLUS
        | MINUS
        | pointer // dereference
        | NOT
        ;

postfix_expr
        : postfix_expr LEFT_BRACKET expression RIGHT_BRACKET // array access
        | postfix_expr DECREMENT
        | postfix_expr INCREMENT
        | postfix_expr LEFT_PAREN arguments? RIGHT_PAREN // function call
        | prim_expr
        ;

arguments
        : assignment_expr (COMMA assignment_expr)*
        ;

prim_expr : LEFT_PAREN expression RIGHT_PAREN
		  | identifier
		  | constant ;

//-----------------------------------------------------------------------------------------------

types
        : type_int
        | type_float
        | type_char
        | type_void 
//        | type_bool
        ;
	  
type_int   : INT ;
type_float : FLOAT ;
type_char  : CHAR ;
type_void  : VOID ;
//type_bool : BOOL ;

// an identifier that has a pointer
id_with_ptr : pointer* identifier;
identifier  : ID ;
pointer     : STAR ; 

constant : int_constant 
         | float_constant 
         | str_constant 
         | char_constant
//         | bool_constant 
         ;

int_constant   : INTEGER_CONSTANT ;
float_constant : FLOAT_CONSTANT ;
str_constant   : STRING_CONSTANT ;
char_constant  : CHAR_CONSTANT ;
//bool_constant  : BOOL_CONSTANT ;

INCLUDE : '#include';
STDIO_H : '<stdio.h>';

// types
CHAR  : 'char';
INT   : 'int';
FLOAT : 'float';
VOID  : 'void';
//BOOL  : 'bool';

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

AND : '&&';
OR  : '||';
NOT : '!' ; // must be before '!=' for precedence reasons.

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

CHAR_CONSTANT    : '\'' CHARACTER_CHAR+ '\'';
INTEGER_CONSTANT : [0-9][0-9]*;
FLOAT_CONSTANT   : [0-9]* '.' [0-9]+;
STRING_CONSTANT  : '"' STRING_CHAR* '"'; // expansion might be needed
//BOOL_CONSTANT    : 'true' | 'false';

BLOCK_COMMENT : '/*' .*? '*/' -> skip;
LINE_COMMENT  : '//' ~[\r\n]* -> skip;

// keep this at the BOTTOM of the lexer. The identifier DFA will match almost anything, and thus has
// to have the LOWEST priority because otherwise no other tokens will be matched!
ID : [a-zA-Z_][a-zA-Z0-9_]*;
WS : [ \t\r\n]+ -> skip; // skip spaces, tabs, newlines



