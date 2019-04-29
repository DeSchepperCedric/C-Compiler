/**
 * Tests that syntax errors are reported.
 * In this case a missing semicolon.
 */

#include <stdio.h>

int main(int argc, char** argv)
{

    // [Error] line 15:1 missing ';' at 'return'
    // [Error] Compiler was terminated due to errors in the specified C source file.
	int a = 50

	return 0;
}

