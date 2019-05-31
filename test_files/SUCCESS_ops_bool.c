/**
 * Tests for arithmetic operations on bools.
 */

#include <stdio.h>

bool val_true()
{
    return true;
}

bool val_false()
{
    return false;
}

int main(int argc, char** argv)
{
    //// +,-,*,/
    bool a = true;
    bool b = false;
    bool c = true;
    bool d = false;

    printf("### Binary +,-,*,/\n");
    bool add_1 = val_true() + val_true(); // 1
    printf("1+1 = %d + %d = %d. Expected: 1\n", val_true(),  val_true(),  add_1);
    bool add_2 = val_true() + val_false(); // 1
    printf("1+0 = %d + %d = %d. Expected: 1\n", val_true(),  val_false(), add_2);
    bool add_3 = val_false() + val_true(); // 1
    printf("0+1 = %d + %d = %d. Expected: 1\n", val_false(), val_true(),  add_3);
    bool add_4 = val_false() + val_false(); // 0
    printf("0+0 = %d + %d = %d. Expected: 0\n", val_false(), val_false(), add_4);

    bool mul_1 = val_true() * val_true(); // 1
    printf("1*1 = %d * %d = %d. Expected: 1\n", val_true(),  val_true(),  mul_1);
    bool mul_2 = val_true() * val_false(); // 0
    printf("1*0 = %d * %d = %d. Expected: 0\n", val_true(),  val_false(), mul_2);
    bool mul_3 = val_false() * val_true(); // 0
    printf("0*1 = %d * %d = %d. Expected: 0\n", val_false(), val_true(),  mul_3);
    bool mul_4 = val_false() * val_false(); // 0
    printf("0*0 = %d * %d = %d. Expected: 0\n", val_false(), val_false(), mul_4);

    //// ==, !=, >, <, >=, <=
    printf("### Comparison ==, !=\n");
    bool eq_true = val_true() == val_true();
    printf("1 == 1 = %d == %d = %d. Expected: 1\n", val_true(), val_true(),  eq_true);
    bool eq_false = val_true() == val_false();
    printf("1 == 0 = %d == %d = %d. Expected: 0\n", val_true(), val_false(), eq_false);
    bool neq_true = val_true() != val_false();
    printf("1 != 0 = %d == %d = %d. Expected: 1\n", val_true(), val_false(), neq_true);
    bool neq_false = val_true() != val_true();
    printf("1 != 1 = %d == %d = %d. Expected: 0\n", val_true(), val_true(),  neq_false);

    // !, &&, ||
    printf("!1 = !%d = %d. Expected 0\n", val_true(), !val_true());
    printf("!0 = !%d = %d. Expected 1\n", val_false(), !val_false());

    printf("1 && 1 = %d && %d = %d. Expected 1\n", val_true(), val_true(),   val_true()  && val_true());
    printf("1 && 0 = %d && %d = %d. Expected 0\n", val_true(), val_false(),  val_true()  && val_false());
    printf("0 && 1 = %d && %d = %d. Expected 0\n", val_false(), val_true(),  val_false() && val_true());
    printf("0 && 0 = %d && %d = %d. Expected 0\n", val_false(), val_false(), val_false() && val_false());

    printf("1 || 1 = %d || %d = %d. Expected 1\n", val_true(), val_true(),   val_true()  || val_true());
    printf("1 || 0 = %d || %d = %d. Expected 1\n", val_true(), val_false(),  val_true()  || val_false());
    printf("0 || 1 = %d || %d = %d. Expected 1\n", val_false(), val_true(),  val_false() || val_true());
    printf("0 || 0 = %d || %d = %d. Expected 0\n", val_false(), val_false(), val_false() || val_false());

    return 0;
}
