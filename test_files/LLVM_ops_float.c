/**
 * Tests for arithmetic operations on floats.
 * What is checked here:
 *  - Operations on float.
 * What is not checked here:
 *  - Conversions: All expressions here are done by respecting the types of each expression. No conversions where performed.
 */

#include <stdio.h>

int main()
{
    //// +,-,*,/
    float a = 5.0;
    float b = 20.0;
    float c = 0.0-20.0;
    float d = 20.0;
    float e = 5.0;

    printf("a=%f\n", a);
    printf("b=%f\n", b);
    printf("c=%f\n", c);
    printf("d=%f\n", d);
    printf("e=%f\n", e);

    printf("### Binary +,-,*,/\n");
    float add_1 = a + b; // 25
    printf("a+b = %f + %f = %f. Expected: 25.0\n", a, b, add_1);
    float add_2 = a + c; // -15
    printf("a+c = %f + %f = %f. Expected: -15.0\n", a, c, add_2);

    float sub_1 = a - b; // -15
    printf("a-b = %f - %f = %f. Expected: -15.0\n", a, b, sub_1);
    float sub_2 = b - a; // 15
    printf("b-a = %f - %f = %f. Expected: 15.0\n", b, a, sub_2);

    float mul = a * b; // 100
    printf("a * b = %f * %f = %f. Expected: 100.0\n", a, b, mul);

    float div_1 = a / b; // 0
    printf("a / b = %f / %f = %f. Expected: 0.25\n", a, b, div_1);
    float div_2 = b / a; // 4
    printf("b / a = %f / %f = %f. Expected: 4.0\n", b, a, div_2);
    float div_3 = c / a; // -4
    printf("c / a = %f / %f = %f. Expected: -4.0\n", b, a, div_3);

    // +, -
    printf("### Unary +,-\n");
    float plus_1 = +a; // 5
    printf("+a = +%f = %f. Expected 5\n", a, plus_1);
    float plus_2 = +c; // -20
    printf("+c = +%f = %f. Expected -20\n", c, plus_2);
    float min_1 = -a; // -5
    printf("-a = -%f = %f. Expected -5\n", a, min_1);
    float min_2 = -c; // 20
    printf("-c = -%f = %f. Expected 20\n", c, min_2);


    //// ==, !=, >, <, >=, <=
    printf("### Comparison ==, !=\n");
    bool eq_true = b == d;
    printf("b == d = %f == %f = %d. Expected: 1\n", b, d, eq_true);
    bool eq_false = b == a;
    printf("b == a = %f == %f = %d. Expected: 0\n", b, a, eq_false);
    bool neq_true = b != a;
    printf("b != a = %f == %f = %d. Expected: 1\n", b, a, neq_true);
    bool neq_false = b != d;
    printf("b != d = %f == %f = %d. Expected: 0\n", b, d, neq_false);

    printf("### Comparison >\n");
    bool gt_true = b > a;
    printf("b > a = %f > %f = %d. Expected: 1\n", b, a, gt_true);

    bool gt_false_1 = a > b;
    printf("a > b = %f > %f = %d. Expected: 0\n", a, b, gt_false_1);

    bool gt_false_2 = a > e; // a == e
    printf("a > e = %f > %f = %d. Expected: 0\n", a, e, gt_false_2);


    printf("### Comparison <\n");
    bool lt_true = a < b;
    printf("a < b = %f < %f = %d. Expected: 1\n", a, b, lt_true);
    bool lt_false_1 = b < a;
    printf("b < a = %f < %f = %d. Expected: 0\n", b, a, lt_false_1);
    bool lt_false_2 = e < a; // a == e
    printf("e < a = %f < %f = %d. Expected: 0\n", e, a, lt_false_2);

    printf("### Comparison >=\n");
    bool geq_true_1 = b >= a; // b > a
    printf("b >= a = %f < %f = %d. Expected: 1\n", b, a, geq_true_1);
    bool geq_true_2 = a >= e; // a == e
    printf("a >= e = %f < %f = %d. Expected: 1\n", a, e, geq_true_2);
    bool geq_false = a >= b; // b > a
    printf("a >= b = %f < %f = %d. Expected: 0\n", a, b, geq_false);

    printf("### Comparison <=\n");
    bool leq_true_1 = a <= b; // b > a
    printf("a <= b = %f < %f = %d. Expected: 1\n", a, b, leq_true_1);
    bool leq_true_2 = a <= e; // a == e
    printf("a <= e = %f < %f = %d. Expected: 1\n", a, e, leq_true_2);
    bool leq_false = b <= a; // b > a
    printf("b <= a = %f < %f = %d. Expected: 0\n", b, a, leq_false);


    //// +=, -=, *=, /=
    printf("### Assignment +=, -=, *=, /=\n");
    float f = 5;
    printf("f=%f\n",f);

    f += 2; // 7
    printf("f += 2 = %f. Expected: 7.0\n", f);
    f -= 3; // 4
    printf("f -= 3 = %f. Expected: 4.0\n", f);
    f *= 10; // 40
    printf("f *= 10 = %f. Expected: 40.0\n", f);
    f /= 3; // 13
    printf("f /= 3 = %f. Expected: 13.333...\n", f);

    float g = 0-5;
    printf("g=%f\n",g);

    g += 2; // -3
    printf("g += 2 = %f. Expected: -3.0\n", g);
    g -= 3; // -6
    printf("g -= 3 = %f. Expected: -6.0\n", g);
    g *= 10; // -60
    printf("g *= 10 = %f. Expected: -60.0\n", g);
    g /= 3; // -20
    printf("g /= 3 = %f. Expected: -20.0\n", g);


    // ++, --
    printf("### Prefix ++, --\n");
    float h = 50;
    printf("h=%f\n", h);
    float h_pp_ret = ++h; // 51
    printf("h after ++h = %f. Expected 51\n", h);
    printf("return value of ++h = %f. Expected 51\n", h_pp_ret);
    float h_mm_ret = --h; // 50
    printf("h after --h = %f. Expected 50\n", h);
    printf("return value of --h = %f. Expected 50\n", h_mm_ret);

    printf("### Postfix ++, --\n");
    float i = 23;
    printf("h=%f\n", i);
    float i_pp_retval = i++; // 24
    printf("i after i++ = %f. Expected 24\n", i);
    printf("return value of i++ = %f. Expected 23\n", i_pp_retval);
    float i_mm_retval = i--; // 23
    printf("i after i-- = %f. Expected 23\n", i);
    printf("return value of i-- = %f. Expected 24\n", i_mm_retval);


    // !, &&, ||
    float j = 50;
    printf("j=%f\n", j);
    float j_not = !j; // 0
    printf("!j = !%f = %f. Expected 0\n", j, j_not);

    float k = 50;
    printf("k=%f\n", k);

    float l = 0;
    printf("l=%f\n", l);
    float l_not = !l; // 1
    printf("!l = !%f = %f. Expected 1\n", l, l_not);

    float m = 0;
    printf("m=%f\n", m);

    float j_and_k = j && k; // 1
    printf("j && k = %f && %f = %f. Expected 1\n", j, k, j_and_k);
    float j_and_l = j && l; // 0
    printf("j && l = %f && %f = %f. Expected 0\n", j, l, j_and_l);
    float l_and_j = l && j; // 0
    printf("l && j = %f && %f = %f. Expected 0\n", l, j, l_and_j);
    float l_and_m = j && m; // 0
    printf("l && m = %f && %f = %f. Expected 0\n", l, m, l_and_m);

    float j_or_k = j || k; // 1
    printf("j || k = %f && %f = %f. Expected 1\n", j, k, j_or_k);
    float j_or_l = j || l; // 1
    printf("j || l = %f && %f = %f. Expected 1\n", j, l, j_or_l);
    float l_or_j = l || j; // 1
    printf("l || j = %f && %f = %f. Expected 1\n", l, j, l_or_j);
    float l_or_m = l || m; // 0
    printf("l || m = %f && %f = %f. Expected 0\n", l, m, l_or_m);

    return 0;
}
