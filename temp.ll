declare i32 @printf(i8*, ...) nounwind 
declare i32 @scanf(i8*, ...) nounwind 
@a = global i32 5
define i32 @main(){
%1 = alloca i32
store i32 5, i32* %1
%2 = load i32, i32* %1 
%3 = alloca i32
store i32 1, i32* %3
%4 = load i32, i32* %3 
%5 = add i32 %2, %4
%6 = alloca i32
store i32 %5, i32* %6 
%T1.c = alloca i32
%7 = load i32, i32* %6 
store i32 %7, i32* %T1.c 

%8 = alloca float
store float 5.0, float* %8
%9 = load float, float* %8 
%10 = alloca float
store float 1.0, float* %10
%11 = load float, float* %10 
%12 = fadd float %9, %11
%13 = alloca float
store float %12, float* %13 
%T1.b = alloca float
%14 = load float, float* %13 
store float %14, float* %T1.b 

%15 = alloca i32
store i32 0, i32* %15
%16 = load i32, i32* %15 
ret i32 %16}

