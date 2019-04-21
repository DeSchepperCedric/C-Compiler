/**
 * @file: file to demonstrate that boolean expressions work as boolended.
 */

#include <stdio.h>

void expressions()
{
    bool l = true;
    bool r = false;

    // +,-,*,/,%
    bool plus = l + r;
    bool sub  = l - r;
    bool mul  = l * r;
    bool div  = l / r;
    bool mod  = l % r;

    // ++, --
    bool inc = false;
    inc++;
    ++inc;

    bool dec = true;
    dec--;
    --dec;

    // unary +,-
    bool other = false;
    other = -l;
    other = +l;
    other = +true;

    bool a = true;
    bool b = false;

    // logic operators
    bool c = a && b;
    c = a || b;
    c = !b;
    
    // assignment
    a = c;
    a += c;
    a -= c;
    a *= c;
    a = true;
    c = true; 
    a /= c;

    // comparison
    bool comp = false;
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

bool main(bool arc, char** argv)
{}


