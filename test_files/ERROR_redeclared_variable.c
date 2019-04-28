/**
 * Tests that re-declarations of variables are detected and reported.
 */

#include <stdio.h>

void func()
{
    int i = 5;

    // [Error] Redeclaration of variable 'i' on line 13. The identifier was already declared with type 'int'.
    // [Error] Compiler was terminated due to errors in the specified C source file.
    float i = 6;
}


int main(int arc, char** argv)
{}
