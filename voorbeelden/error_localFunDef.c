/**
 * @file: file to demonstate that local function
 * definitions are not allowed.
 */

#include <stdio.h>

void global_func()
{
    int local_func()
    {
        return 20;
    }

}

int main(int arc, char** argv)
{}

