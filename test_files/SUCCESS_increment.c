/**
 * Tests for increment operation (++), both postfix and prefix
 */

#include <stdio.h>

int main(int argc, char** argv)
{
    int a = 5;

    printf("a++ = %d. Expected: 5\n", a++);
    printf("a = %d. Expected: 6\n", a);
    printf("++a = %d. Expected: 7\n", ++a);

    a++;
    ++a;
    printf("a = %d. Expected: 9\n\n", a);


    float b = 5.5;

    printf("b++ = %f. Expected: 5.5\n", b++);
    printf("b = %f. Expected: 6.5\n", b);
    printf("++b = %f. Expected: 7.5\n", ++b);

    b++;
    ++b;
    printf("b = %f. Expected: 9.5\n", b);

    return 0;
}
