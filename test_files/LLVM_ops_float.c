/**
 * Tests for arithmetic operations on floats.
 * What is checked here:
 *  - Operations on float.
 * What is not checked here:
 *  - Conversions: All expressions here are done by respecting the types of each expression. No conversions where performed.
 */

#include <stdio.h>


float val_a()
{
    return 5.0;
}

float val_b()
{
    return 20.0;
}

float val_c()
{
    return -20.0;
}

float val_d()
{
    return 20.0;
}

float val_e()
{
    return 5.0;
}

float val_j()
{
    return 50.0;
}

float val_k()
{
    return 50.0;
}

float val_l()
{
    return 0.0;
}

float val_m()
{
    return 0.0;
}

int main()
{
    printf("a=%f. Expected: 5.0\n",   val_a());
    printf("b=%f. Expected: 20.0\n",  val_b());
    printf("c=%f. Expected: -20.0\n", val_c());
    printf("d=%f. Expected: 20.0\n",  val_d());
    printf("e=%f. Expected: 5.0\n",   val_e());
    
    //// +,-,*,/

    printf("### Binary +,-,*,/\n");
    float add_1 = val_a() + val_b(); // 25
    printf("a+b = %f + %f = %f. Expected: 25.0\n",  val_a(), val_b(), add_1);
    float add_2 = val_a() + val_c(); // -15
    printf("a+c = %f + %f = %f. Expected: -15.0\n", val_a(), val_c(), add_2);

    float sub_1 = val_a() - val_b(); // -15
    printf("a-b = %f - %f = %f. Expected: -15.0\n", val_a(), val_b(), sub_1);
    float sub_2 = val_b() - val_a(); // 15
    printf("b-a = %f - %f = %f. Expected: 15.0\n",  val_b(), val_a(), sub_2);

    float mul = val_a() * val_b(); // 100
    printf("a * b = %f * %f = %f. Expected: 100.0\n", val_a(), val_b(), mul);

    float div_1 = val_a() / val_b(); // 0
    printf("a / b = %f / %f = %f. Expected: 0.25\n", val_a(), val_b(), div_1);
    float div_2 = val_b() / val_a(); // 4
    printf("b / a = %f / %f = %f. Expected: 4.0\n",  val_b(), val_a(), div_2);
    float div_3 = val_c() / val_a(); // -4
    printf("c / a = %f / %f = %f. Expected: -4.0\n", val_c(), val_a(), div_3);

    // +, -
    printf("### Unary +,-\n");
    float plus_1 = +val_a(); // 5
    printf("+a = +%f = %f. Expected 5\n",   val_a(), plus_1);
    float plus_2 = +val_c(); // -20
    printf("+c = +%f = %f. Expected -20\n", val_c(), plus_2);
    float min_1 = -val_a(); // -5
    printf("-a = -%f = %f. Expected -5\n",  val_a(), min_1);
    float min_2 = -val_c(); // 20
    printf("-c = -%f = %f. Expected 20\n",  val_c(), min_2);


    //// ==, !=, >, <, >=, <=
    printf("### Comparison ==, !=\n");
    bool eq_true = val_b() == val_d();
    printf("b == d = %f == %f = %d. Expected: 1\n", val_b(), val_d(), eq_true);
    bool eq_false = val_b() == val_a();
    printf("b == a = %f == %f = %d. Expected: 0\n", val_b(), val_a(), eq_false);
    bool neq_true = val_b() != val_a();
    printf("b != a = %f == %f = %d. Expected: 1\n", val_b(), val_a(), neq_true);
    bool neq_false = val_b() != val_d();
    printf("b != d = %f == %f = %d. Expected: 0\n", val_b(), val_d(), neq_false);

    printf("### Comparison >\n");
    bool gt_true = val_b() > val_a();
    printf("b > a = %f > %f = %d. Expected: 1\n", val_b(), val_a(), gt_true);

    bool gt_false_1 = val_a() > val_b();
    printf("a > b = %f > %f = %d. Expected: 0\n", val_a(), val_b(), gt_false_1);

    bool gt_false_2 = val_a() > val_e(); // a == e
    printf("a > e = %f > %f = %d. Expected: 0\n", val_a(), val_e(), gt_false_2);


    printf("### Comparison <\n");
    bool lt_true = val_a() < val_b();
    printf("a < b = %f < %f = %d. Expected: 1\n", val_a(), val_b(), lt_true);
    bool lt_false_1 = val_b() < val_a();
    printf("b < a = %f < %f = %d. Expected: 0\n", val_b(), val_a(), lt_false_1);
    bool lt_false_2 = val_e() < val_a(); // a == e
    printf("e < a = %f < %f = %d. Expected: 0\n", val_e(), val_a(), lt_false_2);

    printf("### Comparison >=\n");
    bool geq_true_1 = val_b() >= val_a(); // b > a
    printf("b >= a = %f < %f = %d. Expected: 1\n", val_b(), val_a(), geq_true_1);
    bool geq_true_2 = val_a() >= val_e(); // a == e
    printf("a >= e = %f < %f = %d. Expected: 1\n", val_a(), val_e(), geq_true_2);
    bool geq_false = val_a() >= val_b(); // b > a
    printf("a >= b = %f < %f = %d. Expected: 0\n", val_a(), val_b(), geq_false);

    printf("### Comparison <=\n");
    bool leq_true_1 = val_a() <= val_b(); // b > a
    printf("a <= b = %f < %f = %d. Expected: 1\n", val_a(), val_b(), leq_true_1);
    bool leq_true_2 = val_a() <= val_e(); // a == e
    printf("a <= e = %f < %f = %d. Expected: 1\n", val_a(), val_e(), leq_true_2);
    bool leq_false = val_b() <= val_a(); // b > a
    printf("b <= a = %f < %f = %d. Expected: 0\n", val_b(), val_a(), leq_false);


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
    printf("j=%f. Expected 50.0.\n", val_j());
    printf("!j = !%f = %d. Expected 0\n", val_j(), !val_j());

    printf("k=%f. Expected 50.0.\n", val_k());

    printf("l=%f. Expected 0.0.\n", val_l());
    printf("!l = !%f = %d. Expected 1\n", val_l(), !val_l());

    printf("m=%f. Expected 0.0.\n", val_m());

    bool j_and_k = val_j() && val_k(); // 1
    printf("j && k = %f && %f = %d. Expected 1\n", val_j(), val_k(), j_and_k);
    bool j_and_l = val_j() && val_l(); // 0
    printf("j && l = %f && %f = %d. Expected 0\n", val_j(), val_l(), j_and_l);
    bool l_and_j = val_l() && val_j(); // 0
    printf("l && j = %f && %f = %d. Expected 0\n", val_l(), val_j(), l_and_j);
    bool l_and_m = val_j() && val_m(); // 0
    printf("l && m = %f && %f = %d. Expected 0\n", val_l(), val_m(), l_and_m);

    bool j_or_k = val_j() || val_k(); // 1
    printf("j || k = %f || %f = %d. Expected 1\n", val_j(), val_k(), j_or_k);
    bool j_or_l = val_j() || val_l(); // 1
    printf("j || l = %f || %f = %d. Expected 1\n", val_j(), val_l(), j_or_l);
    bool l_or_j = val_l() || val_j(); // 1
    printf("l || j = %f || %f = %d. Expected 1\n", val_l(), val_j(), l_or_j);
    bool l_or_m = val_l() || val_m(); // 0
    printf("l || m = %f || %f = %d. Expected 0\n", val_l(), val_m(), l_or_m);

    return 0;
}
