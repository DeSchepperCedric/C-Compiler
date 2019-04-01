grammar C;


if_else: 'if' '(' expression ')' statement ('else' statement)?;

iteration_statement:  WHILE '(' expression ')' statement;


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





