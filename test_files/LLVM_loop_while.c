
#include <stdio.h>

int main(int argc, char** argv)
{
	int a[3+3];
	int i = 60;
	while(i > 20);
	{
        i -= 1;
	}

	printf("Whileloop complete\n");

	int j = 0;
	while(i < 60)
	{
		print("j=%d\n", j);
		j++;

		if(j % 2 == 0)
			continue;

		if(j >= 40)
			break;
	}

    return 0;
}
