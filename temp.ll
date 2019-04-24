declare i32 @printf(i8*, ...) nounwind 
declare i32 @scanf(i8*, ...) nounwind 
@a = global i32 5
define i32 @main(){
%1 = load i32, i32* @a 
%2 = alloca i32
store i32 %1, i32* %2 
%3 = alloca i32*
store i32* %2, i32** %3 
%T1.b = alloca i32*
%4 = load i32*, i32** %3 
store i32* %4, i32** %T1.b 

%5 = load i32*, i32** %T1.b 
%6 = alloca i32*
store i32* %5, i32** %6 
%7 = alloca i32**
store i32** %6, i32*** %7 
%T1.c = alloca i32**
%8 = load i32**, i32*** %7 
store i32** %8, i32*** %T1.c 

%9 = load i32**, i32*** %T1.c 
%10 = alloca i32**
store i32** %9, i32*** %10 
%11 = alloca i32***
store i32*** %10, i32**** %11 
%T1.d = alloca i32***
%12 = load i32***, i32**** %11 
store i32*** %12, i32**** %T1.d 

%13 = load i32**, i32*** %12 
%14 = load i32*, i32** %13 
%15 = alloca i32*
store i32* %14, i32** %15 
%T1.q = alloca i32*
%16 = load i32*, i32** %15 
store i32* %16, i32** %T1.q 

%17 = load i32*, i32** %T1.b 
store i32* %17, i32** %T1.q 
%18 = alloca i32
store i32 0, i32* %18
%19 = load i32, i32* %18 
ret i32 %19
}

