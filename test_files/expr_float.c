/**
 * @file: file to demonstrate that float expressions work as floatended.
 */

#include <stdio.h>

void expressions()
{
    float l = 1;
    float r = 2;

    // +,-,*,/,%
    float plus = l + r;
    float sub  = l - r;
    float mul  = l * r;
    float div  = l / r;
    // NOTE: modulo is not fit for floats

    // ++, --
    float inc = 50;
    inc++;
    ++inc;

    float dec = 50;
    dec--;
    --dec;

    // unary +,-
    float other = -5;
    other = -l;
    other = +l;
    other = +10;

    float a = 1;
    float b = 0;

    // logic operators
    float c = a && b;
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
    float comp = 0;
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

float main(float arc, char** argv)
{}
