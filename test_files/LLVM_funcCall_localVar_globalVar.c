/**
 * Tests for arithmetic operations on integers.
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

	printf("Returning '%s'", str);

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

	printf("Calling function with (%d, %f, %c)\n", i, j, x);

	char* retval = retrieveValue(i, j, x);

	printf("Received '%s'", retval);

	void func_defined_after_call();

	func_defined_after_call();

	printf("Entering compound statement.\n");
	{
		printf("i=%d\n", i);

		printf("Declaring variable i\n");
		int i = 20;
		printf("i=%d\n", i);
	}

	return 0;
}


void func_defined_after_call()
{
	printf("Called 'func_defined_after_call'\n");
}