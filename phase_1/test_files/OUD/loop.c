/**
 * @file: file to demonstate that loops work as intended.
 */

#include <stdio.h>

int main(int arc, char** argv)
{
    int k = 0;
    for(int i = 0; i < 5; i++)
    {
        printf("i: %d\n", i);
        k = i;
    }

    int j;
    for(j = k, k = 0; j < 20; j+= 2, k++)
    {
        printf("i: %d, j: %d\n", k, j);
    }


    float f = 50.0;

    while(-f < -40 && true)
    {
        f -= 0.5;
        printf("f: %f\n", f);
    }

    return 0;
}
