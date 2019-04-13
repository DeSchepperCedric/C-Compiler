grammar C;

program : (include | declaration | func_def)+ EOF;

// include for <stdio.h>
include : INCLUDE STDIO_H ;

/// a declaration introduces one or more identifiers into the program
declaration : types init_decltr_list ';';
init_decltr_list : declarator (',' declarator)*;

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
func_decltr : id_with_ptr LEFT_PAREN (param (',' param)*)? RIGHT_PAREN;
param : types id_with_ptr;

// function definition
func_def : types id_with_ptr LEFT_PAREN (param (',' param)*)? RIGHT_PAREN compound_statement ;

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
	    | FOR LEFT_PAREN for_condition RIGHT_PAREN
	    ;

for_condition
        : expression_statement expression_statement expression
        | expression_statement expression_statement
        ;

compound_statement : LEFT_BRACE block_item* RIGHT_BRACE ;
block_item : statement | declaration ;

jump_statement
	    : RETURN ';'
	    | BREAK ';'
        | CONTINUE ';'
        ;

expression_statement : expression ';' ;

// expression
expression : assignment_expr (',' expression)* ;

assignment_expr
        : cond_expr
		| unary_expr ASSIGNMENT assignment_expr
	    ;

cond_expr : equality_expr ; 

equality_expr
        : relational_expr
    	| equality_expr EQUAL relational_expr
	    ;

relational_expr
        : additive_expr
        | relational_expr LESS_THAN equality_expr
        | relational_expr GREATER_THAN equality_expr
        | relational_expr GREATER_EQUAL_THAN equality_expr
        | relational_expr LESS_EQUAL_THAN equality_expr
        | relational_expr NOT_EQUAL equality_expr
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
        ;

postfix_expr
        : postfix_expr LEFT_BRACKET expression RIGHT_BRACKET // array access
        | prim_expr
        | postfix_expr DECREMENT
        | postfix_expr INCREMENT
        ;


// TODO: function call expression! "identifier ( (param ", param")? )"

prim_expr : LEFT_PAREN expression RIGHT_PAREN
		  | identifier
		  | constant ;

//-----------------------------------------------------------------------------------------------

types : type_int 
	  | type_float 
	  | type_char 
	  | type_void ;
	  
type_int : INT ;
type_float : FLOAT ;
type_char : CHAR ;
type_void : VOID ;

// an identifier that has a pointer
id_with_ptr : pointer* identifier;
identifier : ID ;
pointer : STAR ; 

constant : INTEGER_CONSTANT | FLOAT_CONSTANT | STRING_CONSTANT;

INCLUDE: '#include';
STDIO_H: '<stdio.h>';

// types
CHAR: 'char';
INT: 'int';
FLOAT: 'float';
VOID: 'void';

BLOCK_COMMENT: '/*' .*? '*/' -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;

IF: 'if';
ELSE: 'else';
RETURN: 'return';
WHILE: 'while';
BREAK: 'break';
CONTINUE: 'continue';
FOR: 'for';

//operations
PLUS: '+';
MINUS: '-';
STAR: '*';
DIVIDE: '/';
MOD: '%';

INCREMENT: '++';
DECREMENT: '--';

LEFT_PAREN: '(';
RIGHT_PAREN: ')';
LEFT_BRACKET: '[';
RIGHT_BRACKET: ']';
LEFT_BRACE: '{';
RIGHT_BRACE: '}';

ASSIGNMENT: '=';

GREATER_THAN: '>';
LESS_THAN: '<';
EQUAL: '==';
GREATER_EQUAL_THAN: '>=';
LESS_EQUAL_THAN: '<=';
NOT_EQUAL: '!=';

CHAR_CONSTANT: '\'' ~['\\\r\n] '\'';
INTEGER_CONSTANT: [1-9][0-9]*;
FLOAT_CONSTANT: [0-9]* '.' [0-9]+;
STRING_CONSTANT: '"' ~["\\\r\n] '"'; // expansion might be needed

// keep this at the BOTTOM of the lexer. The identifier DFA will match almost anything, and thus has
// to have the LOWEST priority because otherwise no other tokens will be matched!
ID: [a-zA-Z_][a-zA-Z0-9_]*;
WS: [ \t\r\n]+ -> skip; // skip spaces, tabs, newlines



