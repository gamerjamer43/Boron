# BoronLang

BoronLang is a statically typed, precision-first programming language designed for expressive control flow, rich data types, and seamless package integration. This README details every aspect of the language—from basic syntax to advanced features—so you can quickly get started writing robust programs.
This is written by ChatGPT and I'll go through and fix it when I'm done :)
---

## Table of Contents

1. [Installation & Running](#installation--running)
2. [Language Overview](#language-overview)
   - [Basic Syntax and Comments](#basic-syntax-and-comments)
   - [Data Types](#data-types)
   - [Variable Declarations](#variable-declarations)
   - [Expressions and Operators](#expressions-and-operators)
   - [Control Structures](#control-structures)
   - [Functions and Returns](#functions-and-returns)
   - [Arrays, Lists, and Ranges](#arrays-lists-and-ranges)
   - [Packages and Imports](#packages-and-imports)
   - [Scope and Variable Visibility](#scope-and-variable-visibility)
3. [Example Program](#example-program)
4. [Future Enhancements](#future-enhancements)

---

## Installation & Running

1. **Download/Clone the Repository:**  
   Clone the BoronLang repository from GitHub or download the source.

2. **Build/Assemble the Language:**  
   Follow the provided build instructions (e.g., using a provided Makefile or build script) to compile the language tools (lexer, parser, interpreter).

3. **Run a Program:**  
   Execute your BoronLang source file (e.g., `program.boron`) using the interpreter:
   
   ```
   python run.py program.boron
   ```

   (Adjust the command according to your project setup.)

---

## Language Overview

### Basic Syntax and Comments

- **Comments:**  
  Use `#!` to add inline comments. Anything after `#!` on a line is ignored by the parser.
  
  ```
  #! This is a comment that explains the code below
  ```

- **Line Breaks and Semicolons:**  
  Newlines (EOL) and semicolons can be used to separate statements.

---

### Data Types

BoronLang enforces types at compile time. The primary built-in types are:

- **Integer:** Whole numbers  
  Example: `42`
- **Decimal:** High‑precision numbers using `Decimal`  
  Example: `3.14`
- **Boolean:** `true` or `false`  
- **String:** Text enclosed in double quotes  
  Example: `"Hello, World!"`
- **List:** Ordered collection of elements  
  Example: `[1, 2, 3]`
- **Array:** Fixed‑size, typed collection  
- **Range:** A range defined by a start, stop, and increment

---

### Variable Declarations

Declare variables by specifying a type, a name, and optionally an initial value. Examples:

```
#! Basic variable declarations
int myInt = 42
dec myDec = 3.14
bool myBool = true
str myStr = "Hello, World!"
```

#### Lists and Arrays

- **List Declaration:**  
  ```
  list myList = [1, 2, 3]
  ```

- **Array Declaration:**  
  Specify the element type and size:
  
  ```
  array myArray[int][5] = [1, 2, 3, 4, 5]
  ```

- **Range Declaration:**  
  Create a range for use in loops:
  
  ```
  range myRange = (1, 9, 1)  #! Defines a range from 1 to 8
  ```

---

### Expressions and Operators

BoronLang supports standard arithmetic, comparison, logical, and compound assignment operators.

- **Arithmetic Operators:**  
  ```
  2 + 3       # Addition
  5 - 2       # Subtraction
  3 * 4       # Multiplication
  10 / 2      # Division
  2 ** 3      # Exponentiation (power)
  10 // 3     # Floor division
  10 % 3      # Modulus
  ```

- **Comparison Operators:**  
  ```
  myInt > 10
  myInt < 10
  myInt == 42
  myInt != 42
  ```

- **Logical Operators:**  
  ```
  bool result = (myInt > 10) and (myBool == true)
  ```

- **Compound Assignments:**  
  ```
  myInt += 1   # Increments myInt by 1
  myInt -= 2   # Decrements myInt by 2
  ```

---

### Control Structures

#### If / Else If / Else

```
if myInt == 42 {
    Console.out("Answer found!")
} else if myInt > 42 {
    Console.out("Too high!")
} else {
    Console.out("Too low!")
}
```

#### For Loops

```
for (int i = 0; i < 5; i++) {
    Console.out(myArray[i])
}
```

#### While Loops

```
bool continueLoop = true
while continueLoop {
    Console.out("Looping...")
    continueLoop = false
}
```

#### Do-While Loops

```
int i = 2
do {
    Console.out("Hi!")
    i--
} while (i > 0)
```

---

### Functions and Returns

```
fn myFunction(int arg1, int arg2) $$ bool {
    if arg1 == arg2 {
        $$ true   # Returns true if the arguments are equal
    }
    $$ false      # Otherwise returns false
}
```

Function calls look like this:
  
```
Console.out(myFunction(1, 1))  # Expected to output true
Console.out(myFunction(1, 2))  # Expected to output false
```

---

## Example Program

```
#! Import a package for console output
import Console

#! Data type declarations
int myInt = 42
dec myDec = 3.14
bool myBool = true
str myStr = "Hello, World!"
list myList = [1, 2, 3]
array myArray[int][5] = [1, 2, 3, 4, 5]
range myRange = (1, 9, 1)

#! Output examples
Console.out(myArray[0])
Console.out(myList[0])

#! Function with early return
fn myFunction(int arg1, int arg2) $$ bool {
    if arg1 == arg2 {
        $$ true
    }
    $$ false
}

Console.out(myFunction(1, 1))  # Should print true
Console.out(myFunction(1, 2))  # Should print false

#! For loop example
for (int i = 0; i < 5; i++) {
    Console.out(myArray[i])
}

#! While loop example
bool flag = true
while flag {
    Console.out("Looping in while...")
    flag = false
}

#! Do-while loop example
int i = 2
do {
    Console.out("In do-while loop!")
    i--
} while (i > 0)
```

---

## Future Enhancements

- **Additional Data Types:** Support for vectors (`vec`), tuples, and sets is planned.
- **Enhanced Scoping:** Better support for closures and nested functions.
- **Package System Improvements:** Allow external package imports.
- **Improved Error Handling:** More descriptive syntax and type error messages.

Enjoy coding in BoronLang!
