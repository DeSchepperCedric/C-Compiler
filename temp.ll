['declare i32 @printf(i8*, ...) nounwind ', 'declare i32 @scanf(i8*, ...) nounwind ', '@.str = private unnamed_addr constant [3 x i8] c"%d\\00"', 'define i32 @t(i32){', '%T1.a = alloca i32', 'store i32 %0, i32* %T1.a ', '%2 = load i32, i32* %T1.a ', '%3 = alloca i32', 'store i32 3, i32* %3', '%4 = load i32, i32* %3 ', '%5 = mul i32 %2, %4', '%6 = alloca i32', 'store i32 %5, i32* %6 ', '%7 = load i32, i32* %6 ', 'ret i32 %7', '}', 'define i32 @main(){', '%1 = alloca i32', 'store i32 5, i32* %1', '%T2.a = alloca i32', '%2 = load i32, i32* %1 ', 'store i32 %2, i32* %T2.a ', '', '%3 = load i32, i32* %T2.a ', '%4 = alloca i32', 'store i32 %3, i32* %4 ', '%5 = alloca i32*', 'store i32* %4, i32** %5 ', '%T2.b = alloca i32*', '%6 = load i32*, i32** %5 ', 'store i32* %6, i32** %T2.b ', '', '%7 = alloca i8*', 'store i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i32 0, i32 0), i8** %7', '%8 = load i8*, i8** %7 ', '%9 = load i32*, i32** %T2.b ', '%10 = load i32, i32* %9 ', '%11 = alloca i32', 'store i32 %10, i32* %11 ', '%12 = load i32, i32* %11 ', '%13 = call i32 (i8*, ...) @printf(i8* %8,i32 %12)', '%14 = alloca i32', 'store i32 %13, i32* %14 ', '%15 = load i32, i32* %T2.a ', 'ret i32 %15', '}']
