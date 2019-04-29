/**
 * Tests that that declaring a variable 'void' is not valid.
 * However, void functions are supported.
 */

#include <stdio.h>

// fine
void f();

// invalid
// [Error] Cannot declare variable or pointer with type 'void' at line 14.
// [Error] Compiler was terminated due to errors in the specified C source file.
void* polymorphic_ptr;

int main(int arc, char** argv)
{}


