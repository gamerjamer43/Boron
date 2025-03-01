import random

def randint(minimum: int, maximum: int) -> int:
    """Returns a random integer in the range [min_val, max_val]"""
    return random.randint(minimum, maximum)

def fill(k: int, maximum: int):
    return [random.randint(0, maximum) for _ in range(k)]

def rand() -> float:
    """Returns a random float between 0 and 1"""
    return random.random()

def choice(seq):
    """Returns a random element from the provided sequence"""
    return random.choice(seq)

def shuffle(seq):
    """Shuffles the sequence in place"""
    random.shuffle(seq)
    return seq

def sample(seq, k: int):
    """Returns a random sample of k elements from the sequence (without replacement)"""
    return random.sample(seq, k)

def choices(seq, k: int):
    """Returns a list of k random elements from the sequence (with replacement)"""
    return random.choices(seq, k=k)

def uniform(a: float, b: float) -> float:
    """Returns a random float between a and b"""
    return random.uniform(a, b)