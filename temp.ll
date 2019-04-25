<class 'ASTTreeNodes.ProgramNode'>
<class 'ASTTreeNodes.IncludeNode'>
<class 'ASTTreeNodes.FuncDef'>
<class 'ASTTreeNodes.Body'>
<class 'ASTTreeNodes.VarDeclWithInit'>
<class 'ASTTreeNodes.AddExpr'>
<class 'ASTTreeNodes.IntegerConstantExpr'>
<class 'ASTTreeNodes.IntegerConstantExpr'>
<class 'ASTTreeNodes.ExpressionStatement'>
<class 'ASTTreeNodes.AssignmentExpr'>
<class 'ASTTreeNodes.DivExpr'>
<class 'ASTTreeNodes.IdentifierExpr'>
<class 'ASTTreeNodes.IntegerConstantExpr'>
<class 'ASTTreeNodes.ReturnWithExprStatement'>
<class 'ASTTreeNodes.IntegerConstantExpr'>
declare i32 @printf(i8*, ...) nounwind 
declare i32 @scanf(i8*, ...) nounwind 
define i32 @main(){
%1 = alloca i32
store i32 10, i32* %1
%2 = load i32, i32* %1 
%3 = alloca i32
store i32 5, i32* %3
%4 = load i32, i32* %3 
%5 = add i32 %2, %4
%6 = alloca i32
store i32 %5, i32* %6 
%T1.b = alloca i32
%7 = load i32, i32* %6 
store i32 %7, i32* %T1.b 

%8 = load i32, i32* %T1.b 
%9 = alloca i32
store i32 10, i32* %9
%10 = load i32, i32* %9 
%11 = div i32 %8, %10
%12 = alloca i32
store i32 %11, i32* %12 
%13 = load i32, i32* %12 
store i32 %13, i32* %T1.b 
%14 = alloca i32
store i32 0, i32* %14
%15 = load i32, i32* %14 
ret i32 %15
}

