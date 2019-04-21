/**
 *  @file: file to demonstate that type conversions work.
 */

void casts()
{
    int a = 5;

    float f = (float) a;

    int* a_ptr = &a;

    float* f_ptr = (int*) a_ptr;
}

int main(int arc, char** argv)
{

}

