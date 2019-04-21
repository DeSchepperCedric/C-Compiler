/**
 * @file: file to demonstate that printf, scanf, and the type code
 * c,f,d,s are supported.
 */

#include <stdio.h>

int main(int arc, char** argv)
{
	char c;
	printf("Enter character.\n");
	scanf("%c", &c);
	printf("You have entered: %c \n", c);

	int i;
	printf("Enter integer. \n");
	scanf("%d", &i);
	printf("You have entered: %d \n", i);


	char str[20];
	printf("Enter string (max 20 char). \n");
	scanf("%s", str);
	printf("You have entered: %s \n", str);


	float f;
	printf("Enter float. \n");
	scanf("%f", &f);
	printf("You have entered: %f \n", f);

}
