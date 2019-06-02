/**
 * Test for compound statement.
 */

#include <stdio.h>

int main(int argc, char** argv)
{
	int i = 10;
	printf("i = %d. Expected: 10\n", i);

	{
	    printf("i = %d. Expected: 10\n", i);
	    int i = 25;
	    printf("i = %d. Expected: 25\n", i);
	}

	printf("i = %d. Expected: 10\n", i);

	return 0;
}

