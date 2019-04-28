/**
 * Tests that type-incorrect expressions are detected and reported.
 */

#include <stdio.h>

void func()
{
    int i = 60;

    // [Error] line 15:0 mismatched input '}' expecting {'++', '--', '+', '-', '*', '(', NOT, '&', BOOL_CONSTANT, INTEGER_CONSTANT, FLOAT_CONSTANT, CHAR_CONSTANT, STRING_CONSTANT, ID}
    // [Error] Compiler was terminated due to errors in the specified C source file.
    char* c =

}

int main(int arc, char** argv)
{}
