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
func_def : types id_with_ptr LEFT_PAREN param_spec? RIGHT_PAREN LEFT_BRACE statement* RIGHT_BRACE ;

statement : 'a = x + 5;' ; // TODO expand this to: while-loop, if-clause, assignment-expr etc

// if_else: 'if' '(' expression ')' statement ('else' statement)?;

// iteration_statement:  WHILE '(' expression ')' statement;

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
//         | FLOATING_CONSTANT
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

constant : INTEGER_CONSTANT | FLOATING_CONSTANT | STRING_CONSTANT;

INCLUDE: '#include';
STDIO_H: '<stdio.h>';

// types
CHAR: 'char';
INT: 'int';
FLOAT: 'float';
VOID: 'void';

ID: [a-zA-Z_][a-zA-Z0-9_]*;
WS: [ \t\r\n]+ -> skip; // skip spaces, tabs, newlines

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

GREATER: '>';
LESS: '<';
EQUAL: '==';

CHAR_CONSTANT: '\'' ~['\\\r\n] '\'';
INTEGER_CONSTANT: [1-9][0-9]*;
FLOATING_CONSTANT: [0-9]* '.' [0-9]+;
STRING_CONSTANT: '"' ~["\\\r\n] '"'; // expansion might be needed





