/**
 * Tests for if-elseif-else statements.
 */

#include <stdio.h>

int main(int argc, char** argv)
{
	if(true)
	{
		printf("If-branch. EXPECTED.\n");
	}
	else if(true)
	{
		printf("Else-if branch. UNEXPECTED.\n");
	}
	else
	{
		printf("Else-branch. UNEXPECTED.\n");
	}

	if(false)
	{
		printf("If-branch. UNEXPECTED.\n");
	}
	else if(true)
	{
		printf("Else-if-Branch. EXPECTED.\n");
	}
	else
	{
		printf("Else-branch. UNEXPECTED.\n");
	}

	if(false)
	{
		printf("If-branch. UNEXPECTED.\n");
	}
	else if(false)
	{
		printf("Else-if-Branch. UNEXPECTED.\n");
	}
	else
	{
		printf("Else-branch. EXPECTED.\n");
	}

	return 0;
}

