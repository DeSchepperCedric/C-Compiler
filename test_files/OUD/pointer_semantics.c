/**
 * @file: file to demonstate that pointers are supported, including dereferencing
 * and retrieving the address with the '&' operator.
 */

#include <stdio.h>

int main(int arc, char** argv)
{
    int i = 6;

    int* i_ptr = &i;

    printf("i is at address %d with value %d", i_ptr, *i_ptr);
}
