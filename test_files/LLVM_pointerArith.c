/**
 * Tests for arithmetic operations on integers.
 */

#include <stdio.h>

void funcWithPtrParam(int* param_ptr)
{
	printf("param ptr addr = %d\n", param_ptr);
	printf("param ptr value = %d\n", *param_ptr);
}

int main(int argc, char** argv)
{
	// int x[5];
 //    x[2] = 20;
 //    int* ptr = x;

	int i = 5;
	printf("i=%d\n", i);

	int* i_ptr = &i;
	// int i_addr = i_ptr;
	// printf("addr of i=%d", i_addr);

	int j = *i_ptr;

	printf("j=%d\n", j);

	funcWithPtrParam(i_ptr);

	return 0;
}

