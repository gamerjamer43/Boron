# Boron

Boron is a statically typed, precision-first programming language designed for expressive control flow, rich data types, and seamless package integration. This README details every aspect of the language—from basic syntax to advanced features—so you can quickly get started writing robust programs.

---

The goal of this language is to be a simple introduction to programming that slightly abstracts, but also expands on python to make it a mix of Java, Python, and C++ to give beginners an introduction to Object Oriented Programming.

## Table of Contents

1. [Installation & Running](#installation--running)
2. [Language Overview](#language-overview)
   - [Basic Syntax and Comments](#basic-syntax-and-comments)
   - [Data Types](#data-types)
   - [Variable Declarations](#variable-declarations)
   - [Expressions and Operators](#expressions-and-operators)
   - [Control Structures](#control-structures)
   - [Functions and Returns](#functions-and-returns)
   - [Classes](#classes)
   - [Packages and Imports](#packages-and-imports)
3. [Example Program](#example-program)
4. [Future Enhancements](#future-enhancements)

---

## Installation & Running

1. **Download/Clone the Repository:**  
   Clone the Boron repository from GitHub or download the source.

2. **Run a Program:**  
   Execute your Boron source file (e.g., `program.b`) using the interpreter:
   
   ```
   python C:\Users\[user]\Downloads\Boron\boronlang\app.py program.b
   ```

   (Adjust the command according to your project setup.)

That simple! Literally grab, and go!

---

## Language Overview

### Basic Syntax and Comments

- **Comments:**  
  Use `#!` to add inline comments. Anything after `#!` on a line is ignored by the parser.
  
  ```
  #! This is a comment that explains the code below
  ```

- **Line Breaks and Semicolons:**  
  Newlines (EOL) can be used to separate statements. Will be adding semicolon soon but it's unnecessary for right now.

---

### Data Types

Boron enforces types at compile time. The primary built-in types are:

- **Integer:** Whole numbers  
  Example: `42`
- **Decimal:** High‑precision numbers using `Decimal`  
  Example: `3.14`
- **Boolean:** `true` or `false`  
- **String:** Text enclosed in double quotes  
  Example: `"Hello, World!"`
- **List:** Ordered collection of elements, untyped
  Example: `[1, 2, 3]`
- **Array:** Fixed‑size, typed collection  
- **Vector** Unlimited-size, typed collection
- **Range:** A range defined by a start, stop, and increment

**Example:**
```
int myInt = 42
dec myDec = 3.14
bool myBool = true
str myStr = "Hello, World!"
list myList = [1, 2, 3]
array myArray[int][5] = [1, 2, 3, 4, 5]
vec myVec[int] = [2, 3, 4]
range myRange = (1, 9, 1)
```

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

- **Vector Declaration:**  
  Specify the element type:
  
  ```
  vec myVec[int] = [1, 2, 3, 4, 5]
  ```

- **Range Declaration:**  
  Create a range for use in loops:

  ```
  range myRange = (1, 9, 1)  #! Defines a range from 1 to 8
  ```

---

### Expressions and Operators

Boron supports standard arithmetic, comparison, logical, and compound assignment operators.

- **Arithmetic Operators:**  
  ```
  2 + 3       #! Addition
  5 - 2       #! Subtraction
  3 * 4       #! Multiplication
  10 / 2      #! Division
  2 ** 3      #! Exponentiation (power)
  10 // 3     #! Floor division
  10 % 3      #! Modulus
  ```

- **Comparison Operators:**  
  ```
  myInt > 10
  myInt < 10
  myInt == 42
  myInt != 42
  true and true
  true or false
  ```

- **Logical Operators:**  
  ```
  bool result = (myInt > 10) or (myBool == true)
  bool result = (myInt > 10) and (myInt < 20)
  ```

- **Compound Assignments:**  
  ```
  myInt++      #! increments myInt by 1
  myInt += 5   #! increments myInt by 5
  myInt -= 2   #! decrements myInt by 2
  myInt *= 3   #! compound multiplies myint by 3
  myInt /= 4   #! compound divides myint by 4
  ```

---

### Control Structures

#### If / Else If / Else

```
if myInt == 42 {
    out("Answer found!")
} else if myInt > 42 {
    out("Too high!")
} else {
    out("Too low!")
}
```

#### For Loops

```
for (int i = 0; i < 5; i++) {
    out(myArray[i])
}
```

#### While Loops

```
bool continueLoop = true
while continueLoop {
    out("Looping...")
    continueLoop = false
}
```

#### Do-While Loops

```
int i = 2
do {
    out("Hi!")
    i--
} while (i > 0)
```

---

### Functions and Returns

```
fn myFunction(int arg1, int arg2) -> bool {
    if arg1 == arg2 {
        -> true   #! returns true if the arguments are equal
    }
    -> false      #! otherwise returns false
}
```

Function calls look like this:
  
```
out(myFunction(1, 1))  #! expected to print true
out(myFunction(1, 2))  #! expected to print false
```

---

### Classes

Classes are another thing that are simple and fun, to use them just create their fields and methods
```
class Integer {
    int number

    fn __init__ (class self, int this) -> {
        self.number = this
    }

    fn add (class self, int that) -> dec {
        -> self.number + that
    }
}
```

To create an instance of a class, just create a new object of it
```
Integer mine = new Integer(1)
```

Then you can operate on it!
```
out("Number: " + toStr(mine.number) + ", Add 2: " + toStr(mine.add(2)))
```

---

### Packages and Imports

```
#import Math
```

Imports are also really simple, just #import said package, and you can use it's methods!
  
```
Math.sin(0.5)
```

---

## Example Programs

**FizzBuzz:**
```
#! define fizzbuzz function
fn fizzbuzz(int numinput) -> str {
    if numinput % 5 == 0 and numinput % 3 == 0 {
        -> "FizzBuzz"
    } else if numinput % 3 == 0 {
        -> "Fizz"
    } else if numinput % 5 == 0 {
        -> "Buzz"
    } else {
        -> numinput
    }
}

#! while true
while true {
    int numinput = toInt(inp("> ")) #! take input, convert to int
    str fb = toStr(fizzbuzz(numinput)) #! run it thru fizzbuzz function
    out(fb) #! print
}
```

**Quicksort:**
```
#import Random

fn quicksort(list arr) -> list {
    if length(arr) <= 1 {  
        -> arr
    }

    int pivot = arr[length(arr) // 2]
    list left = []
    list right = []
    list equal = []

    for (int i = 0; i < length(arr); i += 1) {
        int value = arr[i]
        if value < pivot {
            left += [value]
        } else if value > pivot {
            right += [value]
        } else {
            equal += [value]
        }
    }

    -> quicksort(left) + equal + quicksort(right)
}

list sample_list = Random.fill(21, 10000)
list sorted_list = quicksort(sample_list)
out("Sorted array: " + toStr(sorted_list))
```

**Factorial:**
```
fn factorial(int n) -> int {
    if n <= 1 {
        -> 1
    }
    -> n * factorial(n - 1)
}

int num = 100
out("Factorial of " + toStr(num) + " is " + toStr(factorial(num)))
```

**99 Bottles of Beer:**
```
for (int i = 99; i > 2; i--) {
    out(toStr(i) + " bottles of beer on the wall, " + toStr(i) + " bottles of beer!")
    out("Take one down, pass it around, " + toStr(i - 1) + " bottles of beer on the wall!")
}

out("1 bottle of beer on the wall, 1 bottle of beer!")
out("Take one down, pass it around, no more bottles of beer on the wall!")
out("No more bottles of beer on the wall, no more bottles of beer!")
out("Go to the store, buy some more, 99 more bottles of beer on the wall!")
```

---

## Future Enhancements

- **Additional Data Types:** Support dictionaries, tuples and sets is planned.
- **Enhanced Scoping:** Better support for closures and nested functions.
- **Improved Error Handling:** More descriptive syntax and type error messages.
- **Other shit:** I have no clue what else to add here. A lot more to come.

If you need more info, refer to **"everything.b"** in the examples folder, and view the other examples.
Enjoy writing Boron, a simple yet complex enough introduction to programming!