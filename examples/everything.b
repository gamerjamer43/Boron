#! the big bertha of all test files. the dictionary of all dictionaries
#! the book of boron

#import Collections  #! an import statement, deque will be imported from here

#! all current types supported
#! data types, add dict, set, tuple
int myInt = 42
dec myDec = 3.14
bool myBool = true
str myStr = "Hello, World!"
range myRange = (1, 9, 1)  #! make it actually work with the for loop
vec myVec[int] = [2, 3, 4]
array myArray[int][5] = [1, 2, 3, 4, 5]
list myList = [1, 2, 3]
dict myDict = {1: "one", 2: "two", 3: "three"}
auto myAuto = 42  #! auto type inference, doesn't matter what type is assigned

#! adding soon
#! set c = {1, 2, 3} sets are a list right now
#! tuple c = (1, 2, 3) i believe tuples are too


#! all operators currently added (i want to say)
int x = 10
int y = 20

#! binary
int sum = x + y                    #! addition
int difference = x - y             #! subtraction
int product = x * y                #! multiplication
dec divisor = x / y                #! division
int power = x ** y                 #! powers
int floor = x // y                 #! floor division
int modulus = x % y                #! modulus

#! compound assignment
x++                                #! increment
y--                                #! decrement
x -= 1                             #! decrease
y += 1                             #! increase
y /= 2                             #! divide current
y *= 2                             #! multiply current

#! boolean operators
bool boolean = x == y              #! equal
bool boolean2 = x != y             #! not equal
bool boolean3 = x > y              #! bool greater than
bool boolean4 = x < y              #! bool less than
bool boolean5 = true and true      #! and
bool boolean6 = true or false      #! or


#! all control flow supported
#! if statements
out("If statement: Checking if x/5 and x/3")
if x % 5 == 0 and x % 3 == 0 {
    out("FizzBuzz")
} else if x % 3 == 0 {
    out("Fizz")
} else if x % 5 == 0 {
    out("Buzz")
} else {
    out(x)
}

#! for loops
out("Starting for loop: ")
for (int i = 0; i < 5; i++) {
        out(myArray[i])
    }
out("Ended!")

#! while loop
out("Starting while loop: ")
bool case = true
while case == true {
    out("True!")
    case = false
}
out("Broke from case!")

#! do while loop
out("Starting do while loop: ")
int i = 2
do {
    out("Current number: " + toStr(i))
    i--
} while (i > 0)
out("Broke from case!")


#! functions
#! demo function
fn myFunction(int arg1, int arg2) -> bool {
    bool arg1tf
    bool arg2tf

    if arg1 % 2 == 0 {
        arg1tf = true
    } 
    
    if arg2 % 2 == 0 {
        arg2tf = true
    }

    -> arg1tf and arg2tf
}

out(myFunction(1, 2)) #! usage, prints true both numbers % 2 = 0


#! classes
#! class creation
class Integer {
    int number

    fn __init__ (class self, int this) -> {
        self.number = this
    }

    fn add (class self, int that) -> dec {
        -> self.number + that
    }
}

#! instantiation and field/method accesses
Integer mine = new Integer(1)
out("Number: " + toStr(mine.number) + ", Add 2: " + toStr(mine.add(2)))

#! use the deque object imported from collections, just import and you can use all its methods
Deque deque = new Deque()
deque.pushFront(1)

#! with this, you can do literally anything in the language. learn the syntax and fuck around :)