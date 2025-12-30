fn fibonacci(int n) -> int {
    if n <= 0 {
        -> 0
    }
    if n == 1 {
        -> 1
    }
    -> fibonacci(n - 1) + fibonacci(n - 2)
}

int n = toInt(inp("> "))
out("Fibonacci of " + toStr(n) + " " + toStr(fibonacci(n)))