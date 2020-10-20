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
    * `python setup.py sdist bdist_wheel`
    * `pip install sdist/lilang-*.whl`

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

Lilang only supports printing integer numbers so the simplest example will be printing number.

Filename: hello_world.li
```
printi(1);
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

#### Array type

An Array is a collection of multiple values. Lilang supports only arrays of integers. In Lilang, the values going into an array are written as a comma-separated list inside square brackets.

Syntax:
```
int[] x = [1, 2, 3, 4];
printi(x[0]);
```

### If statement
Use the if statement to specify a block of code to be executed if a condition is true.

`If` statement start with `if` keyword, which is followed by condition in parentheses. The block of code we want to execute if the condition is true is placed after the condition inside curly brackets.

Syntax:

```
int x = 1;
if (x < 5) {
    printi(x);
}
```

There is no 'else' clause.

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

More examples can be found in 'tests' directory.