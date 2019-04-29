/**
 * Demonstration file.
 */

#include <stdio.h>

void printFibIterative()
{
	return;
}

int fib_recursive(int n)
{
	if (n == 0)
	{
		return 0;
	}
	else if(n == 1)
	{
		return 1;
	}
	else
	{
		return fib_recursive(n-1) + fib_recursive(n-2);
	}

	return 0;
}

int main(int argc, char** argv)
{
    int fib_result = fib_recursive(10);

    // Demonstrate pointers
    int* ptr_fib_result = &fib_result;
    int** ptr_ptr_fib_result = &ptr_fib_result;

    printf("10th fibonacci number (calculated using recursion): %d\n", **ptr_ptr_fib_result);


    printf("Calculating the first 25 fibonacci numbers.\n");
    int fib_nrs[25];
    fib_nrs[0] = 0;
    fib_nrs[1] = 1;

    int i = 2;
    while(i < 25)
    {
    	fib_nrs[i] = fib_nrs[i-1] + fib_nrs[i-2];

    	i += 1;
    }

    int j = 0;
    while(j < 25)
    {
    	printf("fib[%d] = %d\n", j, fib_nrs[j]);

    	j += 1;
    }

	return 0;
}