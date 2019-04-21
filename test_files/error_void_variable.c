/**
 * @file: file to demonstate that declaring a variable 'void' is not valid.
 * However, void pointers and void functions are supported.
 */

#include <stdio.h>

// fine
void f();
void* polymorphic_ptr;

// invalid
void v;

int main(int arc, char** argv)
{}


