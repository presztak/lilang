# Lilang

Lilang is a toy compiled language with syntax simillar to C written in Python. The compiler uses sly and llvmlite projects. Sly for lexing and parsing, llvmlite for code generation.
The purpose of this project is to learn and experiment with compiler design.

## Installation

### Building on a unix-like systems

1. Dependencies
    * `gcc>=9.3`
    * `pip>=20.0.2`
    * `git`

2. Clone git repo:
    * `git clone https://github.com/presztak/lilang.git`
    * `cd lilang`

3. Build and install
    * `python setup.py bdist_wheel`
    * `pip install dist/lilang-*.whl`

## Development

### Installation
`pip install -e .[dev]`

### Running Tests
`python -m unittest discover -s tests`

### isort
`isort lilang`

### flake8
`flake8`

## Tutorial

### Hello world

Source code of the Hello world program is below.

Filename: hello_world.li
```
prints("Hello world");
```

```
$ lilang hello_world.li
$ ./bin/hello_world
```

### Data types

#### Integer

An integer is a number without a fractional component. It takes up 32 bits of space.

Syntax:
```
int x = 10;
printi(x);
```

#### Bool type

A bool is a data type which can store `true` or `false`.

Syntax:
```
bool b = true;
```

#### String type

String is a data type which contains collection of characters in double quotes.

Syntax:
```
string s = "Hello";
prints(s);
```


### Arrays

An Array is a collection of multiple values. Lilang supports arrays of integers and bools. In Lilang, the values going into an array are written as a comma-separated list inside square brackets.

Syntax:
```
int[] x = [1, 2, 3, 4];
printi(x[0]);
```

#### Multi-dimensional arrays

Multi-dimensional arrays can be defined using multiple squere brackets.

Syntax:
```
int[][] x = [[1, 2], [3, 4]];
printi(x[0][1]);
```


### If...else statement
Use the if statement to specify a block of code to be executed if a condition is true.

`If` statement start with `if` keyword, which is followed by condition in parentheses. The block of code we want to execute if the condition is true is placed after the condition inside curly brackets. If the condition is not true then `else` block will be executed.

Syntax:

```
int x = 1;
if (x < 5) {
    prints("true");
} else {
    prints("false");
}
```

### While statement

The while loop loops through a block of code as long as a specified condition is true.

`While` statement start with `while` keyword, which is followed by condition in parentheses. The block of code we want to execute if the condition is true is placed after the condition inside curly brackets.

Sytax:
```
int x = 0;
while (x < 10) {
    printi(x);
    x = x + 1;
}
```


### For statement

`for` statement is a repetition control structure that allows you to write a loop that needs to execute a specific number of times.
It has three parts:
 - init expresion
 - contidion expresion
 - increment expresion

The block of code to execute is placed in curly brackets.

Syntax:
```
for (int i = 0; i < 10; i += 1;) {
    printi(i);
}
```


### Break and continue statements

The `break` statement ends the loop immediately when it is encountered.

Syntax:
```
for (int i = 0; i < 10; i += 1;) {
    if (i > 5) {
        break;
    }
    printi(i);
}
```

The `continue` statement skips the current iteration of the loop and continues with the next iteration.

Syntax:
```
for (int i = 0; i < 10; i += 1;) {
    if (i < 5) {
        continue;
    }
    printi(i);
}
```

### Defining function

Function is a block of code designed to perform a particular task.

Function definition start with return type, which is followed by name of function. In parentheses we define arguments of the function. The block of code we want to execute is placed inside curly brackets.

Syntax:
```
void f() {
    printi(10);
}
f();
```

Function with arguments:
```
int f(int a, int b) {
    return a + b;
}
printi(f(5, 6));
```

#### Variadic functions

Lilang supports functions with variable number of arguments.

Syntax:
```
int f(int ...b) {
    return b[0] + b[2];
}
printi(f(1, 3, 4));
```


### Type casting

Type casting refers to changing an entity of one datatype into another.

Syntax:
```
bool a = bool(10);
int b = int(a);
```


### Command line arguments

There are two variables:

1. `argc` which is int and contains number of arguments. If no argument is supplied, argc will be 1 (name of program itself counts as 1)
2. `argv` which is array of strings and contains arguments names. argv[0] holds the name of program.

Syntax:
```
for (int i = 0; i < argc; i += 1;) {
    prints(argv[i]);
}
```

More examples can be found in 'tests' directory.