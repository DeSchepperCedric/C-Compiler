/**
 * Tests for arithmetic operations on chars.
 */

#include <stdio.h>

char val_a()
{
    return 5;
}

char val_b()
{
    return 20;
}

char val_c()
{
    return 20;
}

char val_e()
{
    return 5;
}

char val_j()
{
    return 50;
}

char val_k()
{
    return 50;
}

char val_l()
{
    return 0;
}

char val_m()
{
    return 0;
}

int main(int argc, char** argv)
{
/*    //// +,-,*,/
    char a = 5;
    char b = 20;
    char c = 20;
    char e = 5;*/

    printf("a=%d\n", val_a());
    printf("b=%d\n", val_b());
    printf("c=%d\n", val_c());
    printf("e=%d\n", val_e());


    printf("### Binary +,-,*,/\n");
    char add_1 = val_a() + val_b(); // 25
    printf("a+b = %d + %d = %d. Expected: 25\n", val_a(), val_b(), add_1);

    char sub_2 = val_b() - val_a(); // 15
    printf("b-a = %d - %d = %d. Expected: 15\n", val_b(), val_a(), sub_2);

    char mul = val_a() * val_b(); // 100
    printf("a * b = %d * %d = %d. Expected: 100\n", val_a(), val_b(), mul);

    char mod_1 = val_a() % val_b(); // 5
    printf("a %% b = %d %% %d = %d. Expected 5\n", val_a(), val_b(), mod_1);
    char mod_2 = val_b() % val_a(); // 0
    printf("b %% a = %d %% %d = %d. Expected 0\n", val_b(), val_a(), mod_2);

    // +, -
    printf("### Unary +,-\n");
    char plus_1 = +val_a(); // 5
    printf("+a = +%d = %d. Expected 5\n", val_a(), plus_1);
    char plus_2 = +val_c(); // 20
    printf("+c = +%d = %d. Expected 20\n", val_c(), plus_2);
    char min_1 = -val_a(); // -5
    printf("-a = -%d = %d. Expected -5\n", val_a(), min_1);
    char min_2 = -val_c(); // -20
    printf("-c = -%d = %d. Expected -20\n", val_c(), min_2);


    //// ==, !=, >, <, >=, <=
    printf("### Comparison ==, !=\n");
    bool eq_true = val_b() == val_c();
    printf("b == c = %d == %d = %d. Expected: 1\n", val_b(), val_c(), eq_true);
    bool eq_false = val_b() == val_a();
    printf("b == a = %d == %d = %d. Expected: 0\n", val_b(), val_a(), eq_false);
    bool neq_true = val_b() != val_a();
    printf("b != a = %d == %d = %d. Expected: 1\n", val_b(), val_a(), neq_true);
    bool neq_false = val_b() != val_c();
    printf("b != c = %d == %d = %d. Expected: 0\n", val_b(), val_c(), neq_false);

    printf("### Comparison >\n");
    bool gt_true = val_b() > val_a();
    printf("b > a = %d > %d = %d. Expected: 1\n", val_b(), val_a(), gt_true);
    bool gt_false_1 = val_a() > val_b();
    printf("a > b = %d > %d = %d. Expected: 0\n", val_a(), val_b(), gt_false_1);
    bool gt_false_2 = val_a() > val_e(); // a == e
    printf("a > e = %d > %d = %d. Expected: 0\n", val_a(), val_e(), gt_false_2);

    printf("### Comparison <\n");
    bool lt_true = val_a() < val_b();
    printf("a < b = %d < %d = %d. Expected: 1\n", val_a(), val_b(), lt_true);
    bool lt_false_1 = val_b() < val_a();
    printf("b < a = %d < %d = %d. Expected: 0\n", val_b(), val_a(), lt_false_1);
    bool lt_false_2 = val_e() < val_a(); // a == e
    printf("e < a = %d < %d = %d. Expected: 0\n", val_e(), val_a(), lt_false_2);

    printf("### Comparison >=\n");
    bool geq_true_1 = val_b() >= val_a(); // b > a
    printf("b >= a = %d < %d = %d. Expected: 1\n", val_b(), val_a(), geq_true_1);
    bool geq_true_2 = val_a() >= val_e(); // a == e
    printf("a >= e = %d < %d = %d. Expected: 1\n", val_a(), val_e(), geq_true_2);
    bool geq_false = val_a() >= val_b(); // b > a
    printf("a >= b = %d < %d = %d. Expected: 0\n", val_a(), val_b(), geq_false);

    printf("### Comparison <=\n");
    bool leq_true_1 = val_a() <= val_b(); // b > a
    printf("a <= b = %d < %d = %d. Expected: 1\n", val_a(), val_b(), leq_true_1);
    bool leq_true_2 = val_a() <= val_e(); // a == e
    printf("a <= e = %d < %d = %d. Expected: 1\n", val_a(), val_e(), leq_true_2);
    bool leq_false = val_b() <= val_a(); // b > a
    printf("b <= a = %d < %d = %d. Expected: 0\n", val_b(), val_a(), leq_false);


    //// +=, -=, *=, /=
    printf("### Assignment +=, -=, *=, /=\n");
    char f = 5;
    printf("f=%d\n",f);

    f += 2; // 7
    printf("f += 2 = %d. Expected: 7\n", f);
    f -= 3; // 4
    printf("f -= 3 = %d. Expected: 4\n", f);
    f *= 10; // 40
    printf("f *= 10 = %d. Expected: 40\n", f);
    f /= 3; // 13
    printf("f /= 3 = %d. Expected: 13\n", f);

    // !, &&, ||
    printf("j=%d\n", val_j());
    char j_not = !val_j(); // 0
    printf("!j = !%d = %d. Expected 0\n", val_j(), j_not);

    printf("k=%d\n", val_k());

    printf("l=%d\n", val_l());
    char l_not = !val_l(); // 1
    printf("!l = !%d = %d. Expected 1\n", val_l(), l_not);

    printf("m=%d\n", val_m());

    char j_and_k = val_j() && val_k(); // 1
    printf("j && k = %d && %d = %d. Expected 1\n", val_j(), val_k(), j_and_k);
    char j_and_l = val_j() && val_l(); // 0
    printf("j && l = %d && %d = %d. Expected 0\n", val_j(), val_l(), j_and_l);
    char l_and_j = val_l() && val_j(); // 0
    printf("l && j = %d && %d = %d. Expected 0\n", val_l(), val_j(), l_and_j);
    char l_and_m = val_j() && val_m(); // 0
    printf("l && m = %d && %d = %d. Expected 0\n", val_l(), val_m(), l_and_m);

    char j_or_k = val_j() || val_k(); // 1
    printf("j || k = %d && %d = %d. Expected 1\n", val_j(), val_k(), j_or_k);
    char j_or_l = val_j() || val_l(); // 1
    printf("j || l = %d && %d = %d. Expected 1\n", val_j(), val_l(), j_or_l);
    char l_or_j = val_l() || val_j(); // 1
    printf("l || j = %d && %d = %d. Expected 1\n", val_l(), val_j(), l_or_j);
    char l_or_m = val_l() || val_m(); // 0
    printf("l || m = %d && %d = %d. Expected 0\n", val_l(), val_m(), l_or_m);

    return 0;
}

