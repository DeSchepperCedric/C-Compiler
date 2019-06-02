/**
 * Tests for arrays.
 */

#include <stdio.h>

int main(int argc, char** argv)
{
	int arr[50];

	arr[0] = 0-30;
	arr[1] = 697541;
	printf("arr[0] = %d. Expected -30\n", arr[0]);
	printf("arr[1] = %d. Expected 697541\n", arr[1]);

	float f_array[21];
	f_array[0] = 0.0-3.16476;
	f_array[1] = 0.612861;
	printf("f_array[0] = %f. Expected -3.16476\n", f_array[0]);
	printf("f_array[1] = %f. Expected 0.612861\n", f_array[1]);

	return 0;
}

