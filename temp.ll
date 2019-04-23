@a = global i32 5
define i32 @main(){
%1 = alloca i32
store i32 2, i32* %1
%T1.b = alloca i32
%2 = load i32, i32* %1 
store i32 %2, i32* %T1.b 

%3 = load i32, i32* %T1.b 
%4 = alloca i32
store i32 2, i32* %4
%5 = load i32, i32* %4 
%6 = add i32 %3, %5
%7 = alloca i32
store i32 %6, i32* %7 
%8 = load i32, i32* %7 
%9 = alloca i32
store i32 4, i32* %9
%10 = load i32, i32* %9 
%11 = add i32 %8, %10
%12 = alloca i32
store i32 %11, i32* %12 
%13 = load i32, i32* %12 
%14 = alloca i32
store i32 20, i32* %14
%15 = load i32, i32* %14 
%16 = add i32 %13, %15
%17 = alloca i32
store i32 %16, i32* %17 
%18 = load i32, i32* %17 
%19 = load i32, i32* %T1.b 
%20 = add i32 %18, %19
%21 = alloca i32
store i32 %20, i32* %21 
%T1.c = alloca i32
%22 = load i32, i32* %21 
store i32 %22, i32* %T1.c 

%23 = load i32, i32* %T1.c 
ret i32 %23}

