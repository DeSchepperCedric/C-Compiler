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

	// test break
	for(int i = 0; i < 50; i++)
	{
		printf("i=%d\n", i);

		if (i % 2 == 0)
			continue;

		if(i >= 20)
			break;
	}

	return 0;
}