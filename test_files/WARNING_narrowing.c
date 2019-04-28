/**
 * Tests that warnings are given for narrowing (using the isRicherThan rules: float isRicherThan int isRicherThan char).
 */

#include <stdio.h>

float return_float(float a){
    return a + 1;
}

int main(int argc, char** argv)
{

    // [Warning] Assigning expression of type 'float' to target of type 'int' will result in narrowing on line 15.
	int a = 50.5;

    // [Warning] Assigning expression of type 'int' to target of type 'char' will result in narrowing on line 18.
	char b = 500;

    // [Warning] Assigning expression of type 'float' to target of type 'int' will result in narrowing on line 21.
    int c = return_float(5.0);

	return 0;
}

