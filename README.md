<html>
<h1>Compiler</h1>

Compiles C code to either LLVM or MIPS.

<h2> Features</h2>

<ul>
    <li>Types: pointer, void, char, int, float</li>
    <li>Import, printf, scanf</li>
    <li>If/else statement</li>
    <li>Local variables</li>
    <li>Global variables</li>
    <li>Comments</li>
    <li>Operations: =, +, -, *, /, <, >, ==</li>
    <li>Functions, function calling</li>
    <li>1-dimensional arrays (constant size)</li>
    <li>Syntax errors</li>
    <li>Typing errors</li>
    <li>%, +=, -=, *=, /=, <=, >=, !=</li>
    <li>Conversions in assignments, parameter passing, expressions, etc</li>
    <li>Type casting</li>
    <li>Bool type, 'not', 'and', 'or', 'true', 'false' keywords (in grammar).</li>
    <li>Bool type used as result of boolean expressions: comparisons, logic, etc.</li>
    <li>++, --, prefix and postfix</li>
    <li>Unary +,-</li>
    <li>while/for loop</li>
    <li>&&, ||, !</li>
</ul>

<h2>Optimisations</h2>
<ul>
    <li>Constant folding</li>
    <li>Constant propagation</li>
    <li>Null sequences</li>
    <li>Unreachable code and dead code:</li>
        <ul>
            <li>Do not generate code for statements that appear after a return in a function</li>
            <li>Do not generate code for variables that are not used. This includes arrays and functions.</li>
        </ul>
    <li>Pruning of dead code for 'continue', 'return', 'break'</li>
</ul>


<h2>Constant folding/propagation and Null sequences</h2>
<ul>
    <li>Constant folding: Evaluate constant expressions at compile time.</li>
    <li>Constant propagation: Substitute the values of known constants in expressions at compile time.
        This can then be used for further constant folding.
    </li>
    <li>Null sequences: Do not generate code for useless operations (e.g. +0 ) and statements.</li>
</ul>

More details on what is all implemented:
<h3>Arithmetics</h3>
<ul>
    <li> x + 0 => x</li>
    <li> 0 + x => x</li>
    <li> x - 0 => x</li>
    <li> x * 1 => x</li>
    <li> 1 * x => x</li>
    <li> x / 1 => x</li>
    <li> cst + cst => cst</li>
    <li> cst - cst => cst</li>
    <li> cst / cst => cst</li>
    <li> cst * cst => cst</li>
    <li> cst % cst => cst</li>
</ul>

<h3>Expressions with no effect</h3>
<ul>
    <li> Comparisons (ex. 5 > 2;)</li>
    <li> Identifier (ex. x;)</li>
    <li> Constants (ex. 5;)</li>
    <li> Logic operations (ex. &&, ||,...)</li>
    <li> Arithmetics(ex. 5 + 1:)</li>
    <li> MinPrefix(ex. -x;)</li>
    <li> PlusPrefix(ex. +x;)</li>
</ul>

<h3>Logical operations</h3>

Cast operations are sometimes necessary to avoid altering the outcome. For example if func() returns 5:
int a = func() && 1 != func() but == (bool) func()
<ul>
    <li>x && 1 => (bool) x</li>
    <li>1 && x => (bool) x</li>
    <li>x && 0 => 0</li>
    <li>0 && x => 0</li>
    <li>x || 0 => (bool) x</li>
    <li>0 || x => (bool) x</li>
    <li>x || 1 => 1</li>
    <li>1 || x => 1</li>
    <li>cst && cst => 0/1</li>
    <li>cst || cst => 0/1</li>
    <li>!0 => 1</li>
    <li>!1 => 0</li>
    <li>!!x => x</li>
</ul>

<h2>Instructions</h2>

The compiler comes in the form of a python 3 file <b>run_compiler.py</b>. It can be used as follows:
<p style="text-align: center;">python3 run_compiler.py &lt;language&gt; &lt;path_to_c_file&gt;</p>

The language can either be mips or llvm.
This will create an <b>output</b> folder that contains a dot representation of the AST-tree and the symbol table.
It will also generate a .ll or .asm file for respectively llvm and mips.

</html> 

