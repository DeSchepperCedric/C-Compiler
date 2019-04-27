
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

	// continue statement not done yet
	// int j = 0;
	// while(i < 60)
	// {
	// 	printf("j=%d\n", j);
	// 	j += 1;

	// 	if(j % 2 == 0)
	// 		continue;

	// 	if(j >= 40)
	// 		break;
	// }

    return 0;
}
