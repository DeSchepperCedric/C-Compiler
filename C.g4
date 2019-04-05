grammar C;

program : declaration+;

declaration : type_spec init_decl_list ';';
init_decltr_list : declarator ',' init_decltr_list
                 | declarator;

/// a declarator introduces one identifier into the program
declarator
        : var_decltr
        | func_decltr;

// variable declarator
var_decltr
        : ID
        | ID = simpl_expr;

// function declarator
func_decltr : ID '(' param_list? ')';
param_spec
        : VOID
        | param_list;
param_list : param ',' param_list;
param : type_spec ID;



if_else: 'if' '(' expression ')' statement ('else' statement)?;

iteration_statement:  WHILE '(' expression ')' statement;

expression
        : assigment_expression
        | assignment_expression ',' expression; // example?

assignment_expression
        : conditional_expression
        | unary_expression assignment_operator assignment_expression;

assignment_operator
        : '='; // can be expanded with optional assignment operators like (ex. +=)

unary_expression
	    : unary_operator unary_expression
	    ;

primary_expression
        : ID
        | FLOATING_CONSTANT
        | INTEGER_CONSTANT
        | STRING_CONSTANT
        | '(' expression ')'
        ;


unary_operator
        : '+'
        | '-'
        | '&' // addresss. Needed?
        ;

cast_expression
        : unary_expression
        // unary operator|
        ;

additive_expression
        : multiplicative_expression
        | multiplicative_expression '+' additive_expression
        | multiplicative_expression '-' additive_expression
        ;

multiplicative_expression
        : cast_expression
        | cast_expression '*' multiplicative_expression
        | cast_expression '/' multiplicative_expression
        // cast_expression '%' multiplicative_expression (optional)
        ;

equality_expression
        : relational_expression
        | relational_expression '==' relation_expression
        // | | relational_expression '!=' relation_expression (optional)
        ;

relational_expression
        : additive_expression
        | additive_expression '<' relational_expression
        | additive_expression '>' relational_expression
        // | additive_expression '<=' relational_expression (optional)
        // | additive_expression '=>' relational_expression (optional)
        ;


type_spec: INT | FLOAT | CHAR | VOID ;

INCLUDE: '#include';
STDIO_H: '<stdio.h>';

ID: [a-zA-Z_][a-zA-Z0-9_]*;
WS: [ \t\r\n]+ -> skip; // skip spaces, tabs, newlines

BLOCK_COMMENT: '/*' .*? '*/' -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;

IF: 'if';
ELSE: 'else';
RETURN: 'return';
WHILE: 'while';

// types
CHAR: 'char';
INT: 'int';
FLOAT: 'float';
VOID: 'void';

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

INTEGER_CONSTANT: [1-9][0-9]*;
FLOATING_CONSTANT: [0-9]* '.' [0-9]+;
STRING_CONSTANT: '"' ~["\\\r\n] '"' // expansion might be needed





