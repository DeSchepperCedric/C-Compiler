#include <stdio.h>

    int b[5];
int main(int argc, char** argv)
{
    float a = 5.5;
    b[3] = 500;

    b[2] = b[3];

    ++b[2];

    int q = 5;
    q++;
    a++;
    printf("%f", a);
    return 0;
}