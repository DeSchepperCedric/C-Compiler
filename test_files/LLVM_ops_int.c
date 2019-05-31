/**
 * Tests for arithmetic operations on integers.
 */

#include <stdio.h>

int main(int argc, char** argv)
{
    //// +,-,*,/
    int a = 5;
    int b = 20;
    int c = 0-20;
    int d = 20;
    int e = 5;

    printf("a=%d\n", a);
    printf("b=%d\n", b);
    printf("c=%d\n", c);
    printf("d=%d\n", d);
    printf("e=%d\n", e);


    printf("### Binary +,-,*,/\n");
    int add_1 = a + b; // 25
    printf("a+b = %d + %d = %d. Expected: 25\n", a, b, add_1);
    int add_2 = a + c; // -15
    printf("a+c = %d + %d = %d. Expected: -15\n", a, c, add_2);

    int sub_1 = a - b; // -15
    printf("a-b = %d - %d = %d. Expected: -15\n", a, b, sub_1);
    int sub_2 = b - a; // 15
    printf("b-a = %d - %d = %d. Expected: 15\n", b, a, sub_2);

    int mul = a * b; // 100
    printf("a * b = %d * %d = %d. Expected: 100\n", a, b, mul);

    int div_1 = a / b; // 0
    printf("a / b = %d / %d = %d. Expected: 0\n", a, b, div_1);
    int div_2 = b / a; // 4
    printf("b / a = %d / %d = %d. Expected: 4\n", b, a, div_2);
    int div_3 = c / a; // -4
    printf("c / a = %d / %d = %d. Expected: -4\n", b, a, div_3);

    int mod_1 = a % b; // 5
    printf("a %% b = %d %% %d = %d. Expected 5\n", a, b, mod_1);
    int mod_2 = b % a; // 0
    printf("b %% a = %d %% %d = %d. Expected 0\n", b, a, mod_2);

    //// +, -
    // printf("### Unary +,-\n");
    // int plus_1 = +a; // 5
    // printf("+a = +%d = %d. Expected 5\n", a, plus_1);
    // int plus_2 = +c; // -20
    // printf("+c = +%d = %d. Expected -20\n", c, plus_2);
    // int min_1 = -a; // -5
    // printf("-a = -%d = %d. Expected -5\n", a, min_1);
    // int min_2 = -c; // 20
    // printf("-c = -%d = %d. Expected 20\n", c, min_2);


    //// ==, !=, >, <, >=, <=
    printf("### Comparison ==, !=\n");
    int eq_true = b == d;
    printf("b == d = %d == %d = %d. Expected: 1\n", b, d, eq_true);
    int eq_false = b == a;
    printf("b == a = %d == %d = %d. Expected: 0\n", b, a, eq_false);
    int neq_true = b != a;
    printf("b != a = %d == %d = %d. Expected: 1\n", b, a, neq_true);
    int neq_false = b != d;
    printf("b != d = %d == %d = %d. Expected: 0\n", b, d, neq_false);

    printf("### Comparison >\n");
    int gt_true = b > a;
    printf("b > a = %d > %d = %d. Expected: 1\n", b, a, gt_true);
    int gt_false_1 = a > b;
    printf("a > b = %d > %d = %d. Expected: 0\n", a, b, gt_false_1);
    int gt_false_2 = a > e; // a == e
    printf("a > e = %d > %d = %d. Expected: 0\n", a, e, gt_false_2);

    printf("### Comparison <\n");
    int lt_true = a < b;
    printf("a < b = %d < %d = %d. Expected: 1\n", a, b, lt_true);
    int lt_false_1 = b < a;
    printf("b < a = %d < %d = %d. Expected: 0\n", b, a, lt_false_1);
    int lt_false_2 = e < a; // a == e
    printf("e < a = %d < %d = %d. Expected: 0\n", e, a, lt_false_2);

    printf("### Comparison >=\n");
    int geq_true_1 = b >= a; // b > a
    printf("b >= a = %d < %d = %d. Expected: 1\n", b, a, geq_true_1);
    int geq_true_2 = a >= e; // a == e
    printf("a >= e = %d < %d = %d. Expected: 1\n", a, e, geq_true_2);
    int geq_false = a >= b; // b > a
    printf("a >= b = %d < %d = %d. Expected: 0\n", a, b, geq_false);

    printf("### Comparison <=\n");
    int leq_true_1 = a <= b; // b > a
    printf("a <= b = %d < %d = %d. Expected: 1\n", a, b, leq_true_1);
    int leq_true_2 = a <= e; // a == e
    printf("a <= e = %d < %d = %d. Expected: 1\n", a, e, leq_true_2);
    int leq_false = b <= a; // b > a
    printf("b <= a = %d < %d = %d. Expected: 0\n", b, a, leq_false);


    //// +=, -=, *=, /=
    printf("### Assignment +=, -=, *=, /=\n");
    int f = 5;
    printf("f=%d\n",f);

    f += 2; // 7
    printf("f += 2 = %d. Expected: 7\n", f);
    f -= 3; // 4
    printf("f -= 3 = %d. Expected: 4\n", f);
    f *= 10; // 40
    printf("f *= 10 = %d. Expected: 40\n", f);
    f /= 3; // 13
    printf("f /= 3 = %d. Expected: 13\n", f);

    int g = 0-5;
    printf("g=%d\n",g);

    g += 2; // -3
    printf("g += 2 = %d. Expected: -3\n", g);
    g -= 3; // -6
    printf("g -= 3 = %d. Expected: -6\n", g);
    g *= 10; // -60
    printf("g *= 10 = %d. Expected: -60\n", g);
    g /= 3; // -20
    printf("g /= 3 = %d. Expected: -20\n", g);


    return 0;
}
