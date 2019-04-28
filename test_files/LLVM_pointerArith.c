/**
 * Tests for pointer semantics.
 */

#include <stdio.h>

void funcWithPtrParam(int* param_ptr)
{
	printf("param ptr addr = %d\n", param_ptr);
	printf("param ptr value = %d\n", *param_ptr);
}

int main(int argc, char** argv)
{
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

