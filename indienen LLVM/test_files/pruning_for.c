/**
 * @file: file to demonstate that pruning dead code is possible within for loops.
 */

#include <stdio.h>

void prune_for_continue()
{
    for(int i = 0; i < 50; i++)
    {
        int j = 1;

        printf("%d", j);

        continue;

        printf("ok"); // pruned

    }

    printf("another print"); // NOT pruned
}

#include <stdio.h>

void prune_for_break()
{
    for(int i = 0; i < 50; i++)
    {
        int j = 1;

        printf("%d", j);

        break;

        printf("ok"); // pruned

    }

    printf("another print"); // NOT pruned
}


void prune_for_return()
{
    for(int i = 0; i < 50; i++)
    {
        int j = 1;

        printf("%d", j);

        return;

        printf("ok"); // pruned

    }

    printf("another print"); // NOT pruned, since a forloop is not always executed
}

void prune_if_return()
{
    for(int i = 0; i < 50; i++)
    {
        int j = 1;

        printf("%d", j);

        if(i < 5)
        {

            char* str = "abcdef";

            return;

            printf("%s", str); // pruned
        }

        printf("ok"); //NOT pruned since if statements are not always executed

    }

    printf("another print"); // NOT pruned, since a forloop is not always executed
}

void prune_ifelse_return()
{
    for(int i = 0; i < 50; i++)
    {
        int j = 1;

        printf("%d", j);

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

    printf("another print"); // NOT pruned, since a forloop is not always executed
}

int main(int arc, char** argv)
{}


