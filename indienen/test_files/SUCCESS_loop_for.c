/**
 * Tests for for-loops.
 */

#include <stdio.h>

int main(int argc, char** argv)
{
	for(int i = 0; i < 5; i++)
	{
		printf("Cur iteration: %d\n", i);
	}

	printf("Forloop complete.\n");

	int k = 0;
	for(float f = 20.0, i=5; f >= 0; i++)
	{
		printf("Forloop iteration\n");
		f -= 0.5;
		k = i;
	}

	printf("k=%d, this is k-5=%d iterations.\n", k, k-5);

	return 0;
}