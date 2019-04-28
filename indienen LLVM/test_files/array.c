/**
 * @file: file to demonstate that arrays work.
 */

#include <stdio.h>

int main(int arc, char** argv)
{
    int some_integer = 60;

    // array init
    int a[3];

    // array assignment
    a[0] = 20;
    a[1] = some_integer;
    a[2] = 1289;

    // array access
    a[2] = a[0] + a[1];
}

