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

    printf("fib recursive: %d\n", fib_result);

	return 0;
}