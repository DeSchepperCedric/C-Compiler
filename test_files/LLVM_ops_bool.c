/**
 * Tests for arithmetic operations on bools.
 */

#include <stdio.h>

int main(int argc, char** argv)
{
    //// +,-,*,/
    bool a = true;
    bool b = false;
    bool c = true;
    bool d = false;

    printf("### Binary +,-,*,/\n");
    bool add_1 = a + c; // 1
    printf("a+c = %d + %d = %d. Expected: 1\n", a, c, add_1);
    bool add_2 = a + b; // 1
    printf("a+b = %d + %d = %d. Expected: 1\n", a, b, add_2);
    bool add_3 = b + a; // 1
    printf("b+a = %d + %d = %d. Expected: 1\n", a, b, add_3);
    bool add_4 = b + d; // 0
    printf("b+d = %d + %d = %d. Expected: 0\n", a, b, add_4);

    bool sub_1 = a - b; // 1 - 0 = 1
    printf("a-b = %d - %d = %d. Expected: 1\n", a, b, sub_1);
    bool sub_2 = b - a; // 0 - 1 = 1
    printf("b-a = %d - %d = %d. Expected: 1\n", b, a, sub_2);
    bool sub_3 = a - c; // 1 - 1 = 0
    printf("a-c = %d - %d = %d. Expected: 0\n", a, c, sub_3);

    bool mul_1 = a * c; // 1
    printf("a*c = %d * %d = %d. Expected: 1\n", a, c, mul_1);
    bool mul_2 = a * b; // 0
    printf("a*b = %d * %d = %d. Expected: 0\n", a, b, mul_2);
    bool mul_3 = b * a; // 0
    printf("b*a = %d * %d = %d. Expected: 0\n", a, b, mul_3);
    bool mul_4 = b * d; // 0
    printf("b*d = %d * %d = %d. Expected: 0\n", a, b, mul_4);


    bool div_1 = a / c; // 0
    printf("a / c = %d / %d = %d. Expected: 1\n", a, c, div_1);
    bool div_2 = b / c; // 4
    printf("b / c = %d / %d = %d. Expected: 0\n", b, c, div_2);


    bool mod_1 = a % c; // 5
    printf("a %% c = %d %% %d = %d. Expected 0\n", a, c, mod_1);
    bool mod_2 = b % c; // 0
    printf("b %% c = %d %% %d = %d. Expected 0\n", b, c, mod_2);

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
    bool eq_true = b == d;
    printf("b == d = %d == %d = %d. Expected: 1\n", b, d, eq_true);
    bool eq_false = b == a;
    printf("b == a = %d == %d = %d. Expected: 0\n", b, a, eq_false);
    bool neq_true = b != a;
    printf("b != a = %d == %d = %d. Expected: 1\n", b, a, neq_true);
    bool neq_false = b != d;
    printf("b != d = %d == %d = %d. Expected: 0\n", b, d, neq_false);

    printf("### Comparison >\n");
    bool gt_true = b > a;
    printf("b > a = %d > %d = %d. Expected: 0\n", b, a, gt_true);
    bool gt_false_1 = a > b;
    printf("a > b = %d > %d = %d. Expected: 1\n", a, b, gt_false_1);
    bool gt_false_2 = a > c; // a == c
    printf("a > c = %d > %d = %d. Expected: 0\n", a, c, gt_false_2);

    printf("### Comparison <\n");
    bool lt_true = a < b;
    printf("a < b = %d < %d = %d. Expected: 0\n", a, b, lt_true);
    bool lt_false_1 = b < a;
    printf("b < a = %d < %d = %d. Expected: 1\n", b, a, lt_false_1);
    bool lt_false_2 = c < a; // a == c
    printf("c < a = %d < %d = %d. Expected: 0\n", c, a, lt_false_2);

    printf("### Comparison >=\n");
    bool geq_true_1 = b >= a; // b > a
    printf("b >= a = %d < %d = %d. Expected: 0\n", b, a, geq_true_1);
    bool geq_true_2 = a >= c; // a == c
    printf("a >= c = %d < %d = %d. Expected: 1\n", a, c, geq_true_2);
    bool geq_false = a >= b; // b > a
    printf("a >= b = %d < %d = %d. Expected: 1\n", a, b, geq_false);

    printf("### Comparison <=\n");
    bool leq_true_1 = a <= b; // b > a
    printf("a <= b = %d < %d = %d. Expected: 0\n", a, b, leq_true_1);
    bool leq_true_2 = a <= c; // a == c
    printf("a <= c = %d < %d = %d. Expected: 1\n", a, c, leq_true_2);
    bool leq_false = b <= a; // b > a
    printf("b <= a = %d < %d = %d. Expected: 1\n", b, a, leq_false);


    //// ++, --
    // printf("### Prefix ++, --\n");
    // int h = 50;
    // printf("h=%d\n", h);
    // int h_pp_ret = ++h; // 51
    // printf("h after ++h = %d. Expected 51\n", h);
    // printf("return value of ++h = %d. Expected 51\n", h_pp_ret);
    // int h_mm_ret = --h; // 50
    // printf("h after --h = %d. Expected 50\n", h);
    // printf("return value of --h = %d. Expected 50\n", h_mm_ret);

    // printf("### Postfix ++, --\n");
    // int i = 23;
    // int i_pp_retval = i++; // 24
    // printf("i after i++ = %d. Expected 24\n", i);
    // printf("return value of i++ = %d. Expected 23\n", i_pp_retval);
    // int i_mm_retval = i--; // 23
    // printf("i after i-- = %d. Expected 23\n", i);
    // printf("return value of i-- = %d. Expected 24\n", i_mm_retval);


    //// !, &&, ||
    // int j = 50;
    // print("j=%d\n", j);
    // int j_not = !j; // 0
    // printf("!j = !%d = %d. Expected 0\n", j, j_not);

    // int k = 50;
    // print("k=%d\n", k);

    // int l = 0;
    // print("l=%d\n", l);
    // int l_not = !k; // 1
    // printf("!l = !%d = %d. Expected 1\n", l, l_not);

    // int m = 0;
    // print("m=%d\n", m);

    // int j_and_k = j && k; // 1
    // printf("j && k = %d && %d = %d. Expected 1\n", j, k, j_and_k);
    // int j_and_l = j && l; // 0
    // printf("j && l = %d && %d = %d. Expected 0\n", j, l, j_and_l);
    // int l_and_j = l && j; // 0
    // printf("l && j = %d && %d = %d. Expected 0\n", l, j, l_and_j);
    // int l_and_m = j && m; // 0
    // printf("l && m = %d && %d = %d. Expected 0\n", l, m, l_and_m);

    // int j_or_k = j || k; // 1
    // printf("j || k = %d && %d = %d. Expected 1\n", j, k, j_or_k);
    // int j_or_l = j || l; // 1
    // printf("j || l = %d && %d = %d. Expected 1\n", j, l, j_or_l);
    // int l_or_j = l || j; // 1
    // printf("l || j = %d && %d = %d. Expected 1\n", l, j, l_or_j);
    // int l_or_m = l || m; // 0
    // printf("l || m = %d && %d = %d. Expected 0\n", l, m, l_or_m);

    return 0;
}
