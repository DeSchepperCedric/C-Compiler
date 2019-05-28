/**
 * Demonstration file.
 */

#include <stdio.h>


int main(int argc, char** argv)
{
int b = 150;
    int a[5];
    a[2] = 200;
     printf("%d\n",  a[2]);
     printf("%d\n",  b);
      printf("%d\n",  a[2]);
    int t = 522;
    int qqq = 32;
    int* tt =&t;
    int** ttt = &tt;
    printf("%d\n", **ttt);


    int* d = &a[2];
    int** dd = &d;
    int*** ddd = &dd;

printf("%d\n", qqq);
printf("%d",  ***ddd);
}