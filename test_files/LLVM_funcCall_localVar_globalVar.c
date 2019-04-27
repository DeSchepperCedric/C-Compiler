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


int main(int argc, char** argv)
{
	global_predicate = false;

	printf("Calling funcDecide(). Expected: calling funcB()\n");
	funcDecide();

	global_predicate = true;

	printf("Calling funcDecide(). Expected: calling funcA()\n");
	funcDecide();

	return 0;
}

