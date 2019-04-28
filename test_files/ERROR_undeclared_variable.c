/**
 * Tests that expressions that contain undeclared identifiers are detected and reported.
 */

#include <stdio.h>

void func()
{
    int i;

    // [Error] Referenced undeclared symbol b at line 13.
    // [Error] Compiler was terminated due to errors in the specified C source file.
    i = 6 * b;
}


int main(int arc, char** argv)
{}
