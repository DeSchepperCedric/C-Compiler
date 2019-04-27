/**
 * Tests for arithmetic operations on integers.
 */

#include <stdio.h>

int main(int argc, char** argv)
{
	int a[5+6];

	printf("Branch taken on 'true':\n");
	if(true)
	{
		printf("If-branch. EXPECTED.\n");
	}
	else
	{
		printf("Else-branch. UNEXPECTED.\n");
	}

	printf("Branch taken on 'false':\n");
	if(false)
	{
		printf("If-branch. UNEXPECTED.\n");
	}
	else
	{
		printf("Else-branch. EXPECTED.\n");
	}

	return 0;
}

