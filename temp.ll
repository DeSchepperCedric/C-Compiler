declare i32 @printf(i8*, ...) nounwind
declare i32 @scanf(i8*, ...) nounwind 
@a = global i32 5
define i32 @main(){
%1 = alloca float
store float 5.0, float* %1
 %2 = fptosi float %1 to i32
%T1.c = alloca i32
%3 = load i32, i32* %2 
store i32 %3, i32* %T1.c 

%4 = alloca i32
store i32 0, i32* %4
%5 = load i32, i32* %4 
ret i32 %5}

