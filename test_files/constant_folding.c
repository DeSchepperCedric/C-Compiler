/**
 * @file: file to demonstate that constant folding works.
 * Constant folding is the compile-time evaluation of expressions
 * that only contain constants.
 */

#include <stdio.h>

int main(int arc, char** argv)
{
    // we have a constant expression that will
    // be evaluated at compile time.

    // declaration with init works
    int a = 5 + 6 * 65 / 32;

    // comparison works
    bool b = 5 <= 6;
    
    // assignment operators work.
    a += 6 + 98 * 3;

    // nested expressions and modulo expression works.
    int k = (6235 + 65) % (6312 * 46 + 3);

    // operations on float are correctly folded
    float f = 0.3 + 621.6574 * 632.6 / 3.333;

    // boolean expression are also folded.
    bool o = (true || false) && (!false and true);


}
