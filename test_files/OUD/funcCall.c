/**
 * @file: file to demonstate that function calling and parameters work.
 */

#include <stdio.h>

float func(int a, char c)
{
    printf("param a: %d", a);
    printf("param c: %c", c);

    return 5.3;
}


int main(int arc, char** argv)
{
    float retval = func(20, 'b');

    printf("%f", retval);
}
