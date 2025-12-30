#! fib tail call version
fn fibonacci_helper(int n, int a, int b) -> int {
    if n <= 0 {
        -> a
    }
    -> fibonacci_helper(n - 1, b, a + b)
}

fn fibonacci_tc(int n) -> int {
    -> fibonacci_helper(n, 0, 1)
}

int n = toInt(inp("> "))
out("Fibonacci of " + toStr(n) + " " + toStr(fibonacci_tc(n)))