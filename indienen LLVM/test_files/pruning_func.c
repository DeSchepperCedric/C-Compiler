/**
 * @file: file to demonstate that pruning dead code is possible within functions.
 */

#include <stdio.h>

void prune_func_return()
{
    int i = 5;

    return;

    float j = 5 + 6 * i; // pruned    
}

void prune_compound_return()
{
    int i = 5;

    {

        char* str = "abcdef";

        return;

        printf("%s", str); // pruned
    }

    printf("abcdef"); // pruned
}

void prune_if_return()
{
    int i = 5;

    if(i < 5)
    {

        char* str = "abcdef";

        return;

        printf("%s", str); // pruned
    }

    printf("abcdef"); // NOT pruned, since the else clause does not return
}

void prune_ifelse_return()
{
    int i = 5;

    if(i < 5)
    {

        char* str = "abcdef";

        return;

        printf("%s", str); // pruned
    }
    else
    {
        return;
    }

    printf("abcdef"); // pruned, since all branches return
}

int main(int arc, char** argv)
{}




