/**
 * Tests for arithmetic operations on integers.
 */

#include <stdio.h>

int val_a()
{
    return 5;
}

int val_b()
{
    return 20;
}

int val_c()
{
    return -20;
}

int val_d()
{
    return 20;
}

int val_e()
{
    return 5;
}

int val_j()
{
    return 50;
}

int val_k()
{
    return 50;
}

int val_l()
{
    return 0;
}

int val_m()
{
    return 0;
}

int main(int argc, char** argv)
{
    printf("a=%d\n", val_a());
    printf("b=%d\n", val_b());
    printf("c=%d\n", val_c());
    printf("d=%d\n", val_d());
    printf("e=%d\n", val_e());

    //// +,-,*,/
    printf("### Binary +,-,*,/\n");
    int add_1 = val_a() + val_b(); // 25
    printf("a+b = %d + %d = %d. Expected: 25\n", val_a(), val_b(), add_1);
    int add_2 = val_a() + val_c(); // -15
    printf("a+c = %d + %d = %d. Expected: -15\n", val_a(), val_c(), add_2);

    int sub_1 = val_a() - val_b(); // -15
    printf("a-b = %d - %d = %d. Expected: -15\n", val_a(), val_b(), sub_1);
    int sub_2 = val_b() - val_a(); // 15
    printf("b-a = %d - %d = %d. Expected: 15\n", val_b(), val_a(), sub_2);

    int mul = val_a() * val_b(); // 100
    printf("a * b = %d * %d = %d. Expected: 100\n", val_a(), val_b(), mul);

    int div_1 = val_a() / val_b(); // 0
    printf("a / b = %d / %d = %d. Expected: 0\n", val_a(), val_b(), div_1);
    int div_2 = val_b() / val_a(); // 4
    printf("b / a = %d / %d = %d. Expected: 4\n", val_b(), val_a(), div_2);
    int div_3 = val_c() / val_a(); // -4
    printf("c / a = %d / %d = %d. Expected: -4\n", val_c(), val_a(), div_3);

    // a = 5
    // b = 20
    int mod_1 = val_a() % val_b(); // 5
    printf("a %% b = %d %% %d = %d. Expected 5\n", val_a(), val_b(), mod_1);
    int mod_2 = val_b() % val_a(); // 0
    printf("b %% a = %d %% %d = %d. Expected 0\n", val_b(), val_a(), mod_2);

    // +, -
    printf("### Unary +,-\n");
    int plus_1 = +val_a(); // 5
    printf("+a = +%d = %d. Expected 5\n", val_a(), plus_1);
    int plus_2 = +val_c(); // -20
    printf("+c = +%d = %d. Expected -20\n", val_c(), plus_2);
    int min_1 = -val_a(); // -5
    printf("-a = -%d = %d. Expected -5\n", val_a(), min_1);
    int min_2 = -val_c(); // 20
    printf("-c = -%d = %d. Expected 20\n", val_c(), min_2);


    //// ==, !=, >, <, >=, <=
    printf("### Comparison ==, !=\n");
    int eq_true = val_b() == val_d();
    printf("b == d = %d == %d = %d. Expected: 1\n", val_b(), val_d(), eq_true);
    int eq_false = val_b() == val_a();
    printf("b == a = %d == %d = %d. Expected: 0\n", val_b(), val_a(), eq_false);
    int neq_true = val_b() != val_a();
    printf("b != a = %d == %d = %d. Expected: 1\n", val_b(), val_a(), neq_true);
    int neq_false = val_b() != val_d();
    printf("b != d = %d == %d = %d. Expected: 0\n", val_b(), val_d(), neq_false);

    printf("### Comparison >\n");
    int gt_true = val_b() > val_a();
    printf("b > a = %d > %d = %d. Expected: 1\n", val_b(), val_a(), gt_true);
    int gt_false_1 = val_a() > val_b();
    printf("a > b = %d > %d = %d. Expected: 0\n", val_a(), val_b(), gt_false_1);
    int gt_false_2 = val_a() > val_e(); // a == e
    printf("a > e = %d > %d = %d. Expected: 0\n", val_a(), val_e(), gt_false_2);

    printf("### Comparison <\n");
    int lt_true = val_a() < val_b();
    printf("a < b = %d < %d = %d. Expected: 1\n", val_a(), val_b(), lt_true);
    int lt_false_1 = val_b() < val_a();
    printf("b < a = %d < %d = %d. Expected: 0\n", val_b(), val_a(), lt_false_1);
    int lt_false_2 = val_e() < val_a(); // a == e
    printf("e < a = %d < %d = %d. Expected: 0\n", val_e(), val_a(), lt_false_2);

    printf("### Comparison >=\n");
    int geq_true_1 = val_b() >= val_a(); // b > a
    printf("b >= a = %d < %d = %d. Expected: 1\n", val_b(), val_a(), geq_true_1);
    int geq_true_2 = val_a() >= val_e(); // a == e
    printf("a >= e = %d < %d = %d. Expected: 1\n", val_a(), val_e(), geq_true_2);
    int geq_false = val_a() >= val_b(); // b > a
    printf("a >= b = %d < %d = %d. Expected: 0\n", val_a(), val_b(), geq_false);

    printf("### Comparison <=\n");
    int leq_true_1 = val_a() <= val_b(); // b > a
    printf("a <= b = %d < %d = %d. Expected: 1\n", val_a(), val_b(), leq_true_1);
    int leq_true_2 = val_a() <= val_e(); // a == e
    printf("a <= e = %d < %d = %d. Expected: 1\n", val_a(), val_e(), leq_true_2);
    int leq_false = val_b() <= val_a(); // b > a
    printf("b <= a = %d < %d = %d. Expected: 0\n", val_b(), val_a(), leq_false);

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

    int g = -5;
    printf("g=%d\n",g);

    g += 2; // -3
    printf("g += 2 = %d. Expected: -3\n", g);
    g -= 3; // -6
    printf("g -= 3 = %d. Expected: -6\n", g);
    g *= 10; // -60
    printf("g *= 10 = %d. Expected: -60\n", g);
    g /= 3; // -20
    printf("g /= 3 = %d. Expected: -20\n", g);


    // ++, --
    printf("### Prefix ++, --\n");
    int h = 50;
    printf("h=%d\n", h);
    int h_pp_ret = ++h; // 51
    printf("h after ++h = %d. Expected 51\n", h);
    printf("return value of ++h = %d. Expected 51\n", h_pp_ret);
    int h_mm_ret = --h; // 50
    printf("h after --h = %d. Expected 50\n", h);
    printf("return value of --h = %d. Expected 50\n", h_mm_ret);

    printf("### Postfix ++, --\n");
    int i = 23;
    printf("i=%d\n", i);
    int i_pp_retval = i++; // 24
    printf("i after i++ = %d. Expected 24\n", i);
    printf("return value of i++ = %d. Expected 23\n", i_pp_retval);
    int i_mm_retval = i--; // 23
    printf("i after i-- = %d. Expected 23\n", i);
    printf("return value of i-- = %d. Expected 24\n", i_mm_retval);

    // !, &&, ||
    printf("j=%d\n", val_j());
    int j_not = !val_j(); // 0
    printf("!j = !%d = %d. Expected 0\n", val_j(), j_not);

    printf("k=%d\n", val_k());

    printf("l=%d\n", val_l());
    int l_not = !val_l(); // 1
    printf("!l = !%d = %d. Expected 1\n", val_l(), l_not);

    printf("m=%d\n", val_m());

    int j_and_k = val_j() && val_k(); // 1
    printf("j && k = %d && %d = %d. Expected 1\n", val_j(), val_k(), j_and_k);
    int j_and_l = val_j() && val_l(); // 0
    printf("j && l = %d && %d = %d. Expected 0\n", val_j(), val_l(), j_and_l);
    int l_and_j = val_l() && val_j(); // 0
    printf("l && j = %d && %d = %d. Expected 0\n", val_l(), val_j(), l_and_j);
    int l_and_m = val_j() && val_m(); // 0
    printf("l && m = %d && %d = %d. Expected 0\n", val_l(), val_m(), l_and_m);

    int j_or_k = val_j() || val_k(); // 1
    printf("j || k = %d && %d = %d. Expected 1\n", val_j(), val_k(), j_or_k);
    int j_or_l = val_j() || val_l(); // 1
    printf("j || l = %d && %d = %d. Expected 1\n", val_j(), val_l(), j_or_l);
    int l_or_j = val_l() || val_j(); // 1
    printf("l || j = %d && %d = %d. Expected 1\n", val_l(), val_j(), l_or_j);
    int l_or_m = val_l() || val_m(); // 0
    printf("l || m = %d && %d = %d. Expected 0\n", val_l(), val_m(), l_or_m);

    return 0;
}