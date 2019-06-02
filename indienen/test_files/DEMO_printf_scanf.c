/**
 * Tests for printf, scanf functions.
 */

#include <stdio.h>

int main(int argc, char** argv)
{
	int received_int = 0;
	printf("Enter integer:\n");
	scanf("%d", &received_int);
	printf("Received int: %d\n", received_int);

	float received_float = 0.0;
	printf("Enter float:\n");
	scanf("%f", &received_float);
	printf("Received float: %f\n", received_float);

	return 0;
}

