/**
 * Tests for decrement operation (--), both postfix and prefix
 */

#include <stdio.h>

int main(int argc, char** argv)
{
    int a = 5;

    printf("a-- = %d. Expected: 5\n", a--);
    printf("a = %d. Expected: 4\n", a);
    printf("--a = %d. Expected: 3\n", --a);

    a--;
    --a;
    printf("a = %d. Expected: 1\n\n", a);


    float b = 5.5;

    printf("b-- = %f. Expected: 5.5\n", b--);
    printf("b = %f. Expected: 4.5\n", b);
    printf("--b = %f. Expected: 3.5\n", --b);

    b--;
    --b;
    printf("b = %f. Expected: 1.5\n", b);

    return 0;
}
