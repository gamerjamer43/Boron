fn factorial(int n) -> int {
    if n <= 1 {
        -> 1
    }
    -> n * factorial(n - 1)
}

int num = 100
out("Factorial of " + toStr(num) + " is " + toStr(factorial(num)))