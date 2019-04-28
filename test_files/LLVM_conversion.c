/**
 * Tests for conversions.
 */

#include <stdio.h>

void func_with_int_param(int param)
{
	printf("func_with_int_param: param = %d. Original: '645.3'\n", param);
	return;
}

void func_with_float_param(float param)
{
	printf("func_with_float_param: param = %f. Original: '6942'\n", param);
	return;
}

int func_with_int_return()
{

	float f = 66953.4512;
	printf("func_with_int_return: returning '%f'.\n", f);

	return f;
}

int main(int argc, char** argv)
{
	// float to integer
	int i_1 = 0.5;
	int i_2 = 65.55;
	printf("int = 0.5   => int = %d\n", i_1);
	printf("int = 65.55 => int = %d\n", i_2);

	// integer to float
	float f_1 = 50;
	float f_2 = 622;
	printf("float = 50  => float = %f\n", f_1);
	printf("float = 622 => float = %f\n", f_2);

	// int to char
	char c_1 = 50;
	char c_2 = 97;

	printf("char = 50 => char = '%c'\n", c_1);
	printf("char = 97 => char = '%c'\n", c_2);

	// char to int

	// int to bool
	bool b_1 = 50;
	bool b_2 = 0;

	printf("bool = 50 => bool = %d\n", b_1);
	printf("bool = 0 =>  bool = %d\n", b_2);

	// float to bool
	bool b_3 = 0.784;
	bool b_4 = 1.445;
	bool b_5 = 0.0;

	printf("bool = 0.784 => bool = %d\n", b_3);
	printf("bool = 1.445 => bool = %d\n", b_4);
	printf("bool = 0.000 => bool = %d\n", b_5);

	// char to bool
	bool b_6 = 'a' - 'a';
	bool b_7 = 'b';

	printf("bool = '\\0' => bool = %d\n", b_6);
	printf("bool = 'b'   => bool = %d\n", b_7);

	// expression: float + int
	float x = 563.454 + 20;
	printf("float = 563.454 + 20 => float = %f\n", x);

	func_with_int_param(645.3); 	// function call: narrowed
	func_with_float_param(6942); 	// function call: integer -> float

	// return value
	int retval = func_with_int_return();
	printf("func_with_int_return: received '%d'.\n", retval);

	return 0;
}
