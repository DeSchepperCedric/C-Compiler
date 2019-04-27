/**
 * @file: file to demonstrate that integer expressions work as intended.
 */

#include <stdio.h>

void expressions()
{
    int l = 1;
    int r = 2;

    // +,-,*,/,%
    int plus = l + r;
    int sub  = l - r;
    int mul  = l * r;
    int div  = l / r;
    int mod  = l % r;

    // ++, --
    int inc = 50;
    inc++;
    ++inc;

    int dec = 50;
    dec--;
    --dec;

    // unary +,-
    int other = -5;
    other = -l;
    other = +l;
    other = +10;

    int a = 1;
    int b = 0;

    // logic operators
    int c = a && b;
    c = a || b;
    c = !b;
    
    // assignment
    a = c;
    a += c;
    a -= c;
    a *= c;
    a = 6;
    c = 7; 
    a /= c;

    // comparison
    int comp = 0;
    comp = l <= b;
    comp = l >= b;
    comp = l < b;
    comp = l > b;
    comp = l == b;
    comp = l != b;


    
}

void nested_expressions()
{


}

int main(int arc, char** argv)
{}
