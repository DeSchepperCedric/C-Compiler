#include <stdio.h>

int a = 5;



int main(){

int* b = &a;

int** c = &b;

int*** d = &c;

int* q = **d;

q = b;

return 0;

}






