/**
 * Tests for function calling, global vars, local vars.
 */

#include <stdio.h>

bool global_predicate = false;

void funcA()
{
	printf("Called funcA\n");
}

void funcB()
{
	printf("Called funcB\n");
}

void funcDecide()
{
	if(global_predicate)
	{
		funcA();
	}
	else
	{
		funcB();
	}
}

char* retrieveValue(int i, float f, char c)
{
	printf("i=%d\n", i);
	printf("f=%f\n", f);
	printf("c=%c\n", c);

	char* str = "A string that will be returned.";

	printf("Returning '%s'\n", str);

	return str;
}


int main(int argc, char** argv)
{
	global_predicate = false;

	printf("Calling funcDecide(). Expected: calling funcB()\n");
	funcDecide();

	global_predicate = true;

	printf("Calling funcDecide(). Expected: calling funcA()\n");
	funcDecide();

	int i = 0;
	float j = 3.141592;
	char x = 'a';

	printf("Calling function 'retrieveValue' with (%d, %f, '%c')\n", i, j, x);

	char* retval = retrieveValue(i, j, x);

	printf("Received '%s'\n", retval);

    i = 5;

	printf("Entering compound statement.\n");
	{
	    printf("printing i from previous scope: %d. Expected: 5.\n", i);

		printf("Declaring variable i with initialiser '20'\n");
		int i = 20;
		printf("i=%d\n", i);
	}

	return 0;
}


