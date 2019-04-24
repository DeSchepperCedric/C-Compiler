declare i32 @printf(i8*, ...) nounwind 
declare i32 @scanf(i8*, ...) nounwind 
@a = global i32 5
define i32 @main(i32){
%T1.q = alloca i32
store i32 %0, i32* %T1.q 
%2 = alloca i32
store i32 5, i32* %2
%3 = load i32, i32* %2 
store i32 %3, i32* %T1.q 
%4 = load i32, i32* %T1.q 
%T1.b = alloca i32
store i32 %4, i32* %T1.b 

%5 = alloca i32
store i32 0, i32* %5
%6 = load i32, i32* %5 
ret i32 %6
}

