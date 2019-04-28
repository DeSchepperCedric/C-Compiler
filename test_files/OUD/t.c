#include <stdio.h>

    int b[5];
int main(int argc, char** argv)
{
    int a = 5;
    b[3] = 500;

    b[2] = b[3];

    ++b[2];

    int q = 5;
    q++;
    printf("%d\n", q);
    printf("%d\n", q++);
    printf("%d\n", q);

    printf("%d\n", b[2]);
    printf("%d\n", b[2]++);
    printf("%d\n", b[2]);
    return 0;
}