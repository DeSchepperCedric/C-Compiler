@a = global i32 5
define i32 @main(){
%1 = alloca i32
store i32 2, i32* %1
%T1.b = alloca i32
%2 = load i32, i32* %1
store i32 %2, i32* %T1.b

%3 = load i32, i32* %T1.b
ret i32 %3}

