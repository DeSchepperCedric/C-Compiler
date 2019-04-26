#include <stdio.h>

int t(int a){

return a * 3;
}

int main(){

int a = 5;
int* b = &a;
printf("%d\n", a);
printf("%d", *b);
return a;
}





