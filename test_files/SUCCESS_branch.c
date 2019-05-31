/**
 * Tests for if-else statements.
 */

#include <stdio.h>

int main(int argc, char** argv)
{
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

