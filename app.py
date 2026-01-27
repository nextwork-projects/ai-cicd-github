"""Simple utility functions - you'll add more!"""


def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


def is_even(n: int) -> bool:
    """Check if a number is even."""
    return n % 2 == 0


def reverse_string(s: str) -> str:
    """Reverse a string."""
    return s[::-1]


def multiply(a,b):
    """Multiply two integers, a and b"""
    return a * b

def factorial(n):
    """Calculate the factorial of n."""

    # Handle invalid input - factorial isn't defined for negatives
    if n < 0:
        raise ValueError(
            "Factorial not defined for negative numbers" 
        )

    # Base case - stop recursion when n is 0 or 1
    if n <= 1:
        return 1

    # Recursive case - n! = n × (n-1)!
    return n * factorial(n-1)