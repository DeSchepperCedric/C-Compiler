/**
 * @file: file to demonstate that the boolean type works.
 */

#include <stdio.h>

int main(int arc, char** argv)
{
    bool b = true;

    printf("%b", b); // true

    b = b && false; // boolean operators work

    printf("%b", b); // false
}

