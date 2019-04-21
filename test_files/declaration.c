/**
 * @file: file to demonstate that declarations work. Here
 * we will demonstrate that the following types of declarations work:
 *  - arrays
 *  - array of pointer (not pointer to array!)
 *  - variable declaration without initialisation
 *  - variable declaration with initialisation
 *  - function declaration with and without parameters.
 * 
 * Note: only global declarations are tested here!
 */

#include <stdio.h>

// array of 50 floats.
float a[50];

// pointers
char* c_ptr;
char** c_ptr_ptr;
int* i_ptr;
float* f_ptr;
bool* bool_ptr;
void* void_ptr;

// array of 30 ptr to int
int* arr[30];

// variables
int i;
char c;
float f;
bool b;

// variables with init
int i_val = 6;
char c_val = 'a';
float f_val = 2.34165;
bool b_val = true;

// function declarations
int func();
void func_with_param(int param_i, float param_f);

int main(int arc, char** argv)
{}

