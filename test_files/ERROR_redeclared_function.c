/**
 * Tests that re-declarations of functions are detected and reported.
 */

#include <stdio.h>

void func(){}

// [Error] Invalid redefinition of existing function 'func' on line 11.
// [Error] Compiler was terminated due to errors in the specified C source file.
int func(int a){
    return a;
}


int main(int arc, char** argv)
{}
