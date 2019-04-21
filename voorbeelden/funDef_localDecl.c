/**
 * @file: file to demonstate that function definitions, and
 * local declarations work.
 */

// function with no parameters
int func()
{
    return 50;
}

// function with parameters
void func_with_param(int param_i, float param_f)
{
    return;
}

char local_scope()
{
    // array of 50 floats.
    float a[50];

    // pointers
    char* c_ptr;
    char** c_ptr_ptr;
    int* i_ptr;
    float* f_ptr;
    bool* bool_ptr;
    void* void_ptr;

    // array of 30 ptr to int
    int* arr[30];

    // variables
    int i;
    char c;
    float f;
    bool b;

    // variables with init
    int i_val = 6;
    char c_val = 'a';
    float f_val = 2.34165;
    bool b_val = true;

    // function declarations
    int func();
    void func_with_param(int param_i, float param_f);

    return 'b';
}

int main(int arc, char** argv)
{}



