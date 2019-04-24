declare i32 @printf(i8*, ...) nounwind 
declare i32 @scanf(i8*, ...) nounwind 
@a = global i32 5
define i32 @main(){
%1 = alloca i32
store i32 5, i32* %1
%T1.a = alloca i32*
%2 = load i32*, i32** %1 
store i32* %2, i32** %T1.a 

%3 = alloca i32
store i32 0, i32* %3
%4 = load i32, i32* %3 
ret i32 %4}

