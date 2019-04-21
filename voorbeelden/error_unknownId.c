/**
 * @file: file to demonstate that expressions that contain
 * unknown identifiers are detected and reported.
 */

void func()
{
    int i;

    // invalid, b does not exist.
    i = 6 * (b + 234.6);
}


int main(int arc, char** argv)
{}
