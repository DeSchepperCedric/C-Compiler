declare i32 @printf(i8*, ...) nounwind 
declare i32 @scanf(i8*, ...) nounwind 
@a = global i32 5
define i32 @main(){
%1 = load i32, i32* @a 
%T1.b = alloca i32
store i32 %1, i32* %T1.b 

%2 = alloca i32
store i32 2, i32* %2
%3 = load i32, i32* %2 
store i32 %3, i32* %T1.b 
%4 = load i32, i32* %T1.b 
%T1.c = alloca i32
store i32 %4, i32* %T1.c 

%5 = load i32, i32* %T1.b 
ret i32 %5}

