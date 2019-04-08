grammar C;

program : (include | declaration | func_def)+;

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
        | id_with_ptr ASSIGNMENT simpl_expr; // assignment can happen at time of declaration: "int i = 5; char* j = &k", etc.

// function declarator
func_decltr : id_with_ptr LEFT_PAREN param_spec? RIGHT_PAREN;
param_spec
        : VOID
        | param (',' param)* ;
param : types id_with_ptr;

// TODO remove this later
simpl_expr : constant;

// function definition
func_def : types id_with_ptr LEFT_PAREN param_spec? RIGHT_PAREN compound_statement ;

statement : if_statement
		  | compound_statement
		  | iteration_statement
		  | expression_statement
		  | jump_statement
		  ;

if_statement: IF LEFT_PAREN expression RIGHT_PAREN statement (ELSE statement)? ;
iteration_statement: WHILE LEFT_PAREN expression RIGHT_PAREN statement;

compound_statement : LEFT_BRACE block_item* RIGHT_BRACE ;
block_item : statement | declaration ;

jump_statement : RETURN ';' ; 

expression_statement : expression ';' ;
expression : assignment_expr (',' expression)* ;

assignment_expr : cond_expr 
				| unary_expr ASSIGNMENT assignment_expr
				;

cond_expr : equality_expr ; 


equality_expr : relational_expr
			  | equality_expr EQUAL relational_expr
			  ;


relational_expr : additive_expr
			  | relational_expr LESS_THAN equality_expr
			  | relational_expr GREATER_THAN equality_expr
			  ;


additive_expr : multiplicative_expr
			  | additive_expr PLUS  multiplicative_expr
			  | additive_expr MINUS multiplicative_expr 
			  ;


multiplicative_expr : cast_expr
					| multiplicative_expr STAR cast_expr
					| multiplicative_expr DIVIDE cast_expr
					;


cast_expr : unary_expr ;

unary_expr : postfix_expr ; 

postfix_expr : postfix_expr LEFT_BRACKET expression RIGHT_BRACKET // array access
			 | prim_expr ;


prim_expr : LEFT_PAREN expression RIGHT_PAREN
		  | identifier
		  | constant ;


// TODO (mandatory) deref_expr, addr_expr

// TODO (optional) add &&, ||, etc to 'cond_expr'
// TODO (optional) x++, x--
// TODO (optional) multiplicative expr '%'
// TODO (optional) add 'goto', 'break', 'continue', etc.
// TODO (optional) 'castExpression' in the C grammar is the "(typename) ID" expression.

//-----------------------------------------------------------------------------------------------

// expression
//         : assigment_expression
//         | assignment_expression ',' expression; // example?

// assignment_expression
//         : conditional_expression
//         | unary_expression assignment_operator assignment_expression;

// assignment_operator
//         : '='; // can be expanded with optional assignment operators like (ex. +=)

// unary_expression
// 	    : unary_operator unary_expression
// 	    ;

// primary_expression
//         : ID
//         | FLOAT_CONSTANT
//         | INTEGER_CONSTANT
//         | STRING_CONSTANT
//         | '(' expression ')'
//         ;


// unary_operator
//         : '+'
//         | '-'
//         | '&' // addresss. Needed?
//         ;

// cast_expression
//         : unary_expression
//         // unary operator|
//         ;

// additive_expression
//         : multiplicative_expression
//         | multiplicative_expression '+' additive_expression
//         | multiplicative_expression '-' additive_expression
//         ;

// multiplicative_expression
//         : cast_expression
//         | cast_expression '*' multiplicative_expression
//         | cast_expression '/' multiplicative_expression
//         // cast_expression '%' multiplicative_expression (optional)
//         ;

// equality_expression
//         : relational_expression
//         | relational_expression '==' relation_expression
//         // | | relational_expression '!=' relation_expression (optional)
//         ;

// relational_expression
//         : additive_expression
//         | additive_expression '<' relational_expression
//         | additive_expression '>' relational_expression
//         // | additive_expression '<=' relational_expression (optional)
//         // | additive_expression '=>' relational_expression (optional)
//         ;

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

//operations
PLUS: '+';
MINUS: '-';
STAR: '*';
DIVIDE: '/';

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

CHAR_CONSTANT: '\'' ~['\\\r\n] '\'';
INTEGER_CONSTANT: [1-9][0-9]*;
FLOAT_CONSTANT: [0-9]* '.' [0-9]+;
STRING_CONSTANT: '"' ~["\\\r\n] '"'; // expansion might be needed

// keep this at the BOTTOM of the lexer. The identifier DFA will match almost anything, and thus has
// to have the LOWEST priority because otherwise no other tokens will be matched!
ID: [a-zA-Z_][a-zA-Z0-9_]*;
WS: [ \t\r\n]+ -> skip; // skip spaces, tabs, newlines



