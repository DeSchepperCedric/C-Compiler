/**
 * @file: file to demonstate that pruning dead code is possible within while loops.
 */

#include <stdio.h>

void prune_for_continue()
{
    int i = 0;
    while(i < 50)
    {
        int j = 1;

        printf("%d", j);

        i++;

        continue;

        printf("ok"); // pruned

    }

    printf("another print"); // NOT pruned, since while loop is not always executed
}

#include <stdio.h>

void prune_for_break()
{
    int i = 0;
    while(i < 50)
    {
        int j = 1;

        printf("%d", j);

        i++;

        break;

        printf("ok"); // pruned

    }

    printf("another print"); // NOT pruned, since while loop is not always executed
}


void prune_for_return()
{
    int i = 0;
    while(i < 50)
    {
        int j = 1;

        printf("%d", j);

        i++;

        return;

        printf("ok"); // pruned

    }

    printf("another print"); // NOT pruned, since while loop is not always executed
}

void prune_if_return()
{
    int i = 0;
    while(i < 50)
    {
        int j = 1;

        printf("%d", j);

        i++;

        if(i < 5)
        {

            char* str = "abcdef";

            return;

            printf("%s", str); // pruned
        }

        printf("ok"); //NOT pruned since if statements are not always executed

    }

    printf("another print"); // NOT pruned, since while loop is not always executed
}

void prune_ifelse_return()
{
    int i = 0;
    while(i < 50)
    {
        int j = 1;

        printf("%d", j);

        i++;

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

    printf("another print"); // NOT pruned, since while loop is not always executed
}

int main(int arc, char** argv)
{}



