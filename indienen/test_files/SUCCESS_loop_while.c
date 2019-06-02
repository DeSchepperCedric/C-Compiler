/**
 * Tests for while loops.
 */

#include <stdio.h>

int main(int argc, char** argv)
{

	int i = 60;
	while(i > 20)
	{
        i -= 1;
        printf("i=%d\n", i);
	}

	printf("Whileloop complete\n");

    return 0;
}
