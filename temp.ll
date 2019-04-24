declare i32 @printf(i8*, ...) nounwind 
declare i32 @scanf(i8*, ...) nounwind 
@a = global i32 5
define void @t(i32){
%T1.b = alloca i32
store i32 %0, i32* %T1.b 
%2 = load i32, i32* %T1.b 
store i32 %2, i32* @a 
ret void
}
define i32 @main(){
%T2.b = alloca i32
store i32 0, i32* %T2.b

%1 = alloca i32
store i32 2555, i32* %1
%2 = load i32, i32* %1 
store i32 %2, i32* %T2.b 
%T2.c = alloca i8
store i8 0, i8* %T2.c

%T2.q = alloca float
store float 0x0000000000000000, float* %T2.q

%3 = alloca i32
store i32 0, i32* %3
%4 = load i32, i32* %3 
ret i32 %4
}

