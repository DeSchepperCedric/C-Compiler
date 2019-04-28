/**
 * Tests that expressions that contain undeclared functions are detected and reported.
 */

#include <stdio.h>

void func()
{
    // [Error] Referenced undeclared symbol get at line 11.
    //[Error] Compiler was terminated due to errors in the specified C source file.
    int i = get(5);
}


int main(int arc, char** argv)
{}
