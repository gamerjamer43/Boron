fn sieve(int limit) -> list {
    if limit < 2 {
        -> []
    }

    list is_prime = []
    for (int i = 0; i <= limit; i += 1) {
        is_prime.append(true)
    }

    is_prime[0] = false
    is_prime[1] = false

    for (int num = 2; num * num <= limit; num += 1) {
        if is_prime[num] {
            for (int m = num * num; m <= limit; m += num) {
                is_prime.append(false)
            }
        }
    }

    list primes = []
    for (int i = 2; i <= limit; i += 1) {
        if is_prime[i] {
            primes.append([i])
        }
    }

    -> primes
}

int max = 50
list primes = sieve(max)
out("Primes up to " + toStr(max) + ": " + toStr(primes))
