/**
 * Tests for arithmetic operations on integers.
 */

#include <stdio.h>

int main(int argc, char** argv)
{
	int received_int = 0;
	printf("Enter integer:\n");
	scanf("%d", &received_int);
	printf("Received int: %d\n", received_int);

	float recieved_float = 0.0;
	printf("Enter float:\n");
	scanf("%f", &recieved_float);
	printf("Received float: %f\n", recieved_float);

	char str[255];
	printf("Enter string:\n");
	scanf("%s", &str);
	printf("Received string: '%s'\n", str);

	return 0;
}

