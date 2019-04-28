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


    printf("Calculating the first 50 fibonacci numbers.\n");
    int fib_nrs[50];
    fib_nrs[0] = 0;
    fib_nrs[1] = 1;

    int i = 2;
    while(i < 50)
    {
    	fib_nrs[i] = fib_nrs[i-1] + fib_nrs[i-2];

    	i += 1;
    }

    int j = 0;
    while(j < 50)
    {
    	printf("fib[%d] = %d\n", j, fib_nrs[j]);

    	j += 1;
    }

	return 0;
}