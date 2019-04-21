/**
 * @file: file to demonstrate that character expressions work as charended.
 */

#include <stdio.h>

void expressions()
{
    char l = 'a';
    char r = 'b';

    // +,-,*,/,%
    char plus = l + r;
    char sub  = l - r;
    char mul  = l * r;
    char div  = l / r;
    char mod  = l % r;

    // ++, --
    char inc = 'd';
    inc++;
    ++inc;

    char dec = 'e';
    dec--;
    --dec;

    // unary +,-
    char other = -'a';
    other = -l;
    other = +l;
    other = +'a';

    char a = 'x';
    char b = '0';

    // logic operators
    char c = a && b;
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
    char comp = '6';
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

char main(char arc, char** argv)
{}
