#include <stdio.h>

void a(int q);
void t(int b){
    int a[5];
    a[2 + 1] = 255;
    a[0] = 5;
    a[3] += a[0];
    printf("%d", a[b+1+2-2]);

}
int main(int argc, char** argv)
{
    a(2);


    return 0;
}