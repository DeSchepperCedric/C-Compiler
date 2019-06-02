/**
 * Tests that warnings are given for narrowing (using the isRicherThan rules: float isRicherThan int isRicherThan char).
 */

#include <stdio.h>

float func_a(int a){
    return a + 1;
}

int func_b(){
    // [Warning] Returning expression of type 'float' in function with return type 'int' will result in narrowing on line 13.
    return 5.5;
}

int main(int argc, char** argv)
{

    // [Warning] Assigning expression of type 'float' to target of type 'int' will result in narrowing on line 20.
	int a = 50.5;

    // [Warning] Assigning expression of type 'int' to target of type 'char' will result in narrowing on line 23.
	char b = 500;

    // [Warning] Passing expression of type 'float' as argument #1 for function 'return_float' narrowing on line 25. Expected type is 'int'.
    // [Warning] Assigning expression of type 'float' to target of type 'int' will result in narrowing on line 25.
    int c = func_a(5.0);

    // [Warning] Assigning expression of type 'float' to target of type 'bool' will result in narrowing on line 30.
    bool d = 5.5;

    int e = func_b();

	return 0;
}

