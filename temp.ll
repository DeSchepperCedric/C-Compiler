declare i32 @printf(i8*, ...) nounwind 
declare i32 @scanf(i8*, ...) nounwind 
@a = global i32 5
define i32 @main(){
%1 = load i32, i32* @a 
%2 = alloca i32
store i32 5, i32* %2
%3 = load i32, i32* %2 
%4 = icmp sgt i32 %1, %3
br i1 %4, label %if4, label %else4
if4:
%5 = alloca i32
store i32 5, i32* %5
%6 = load i32, i32* %5 
ret i32 %6
br label %end4
else4:
%8 = alloca i32
store i32 20, i32* %8
%9 = load i32, i32* %8 
ret i32 %9
br label %end4
end4:
ret void
}

