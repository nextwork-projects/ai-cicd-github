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


def power(base, exponent):
    """
    Calculate base raised to the power of exponent.
    
    Args:
        base: The base number
        exponent: The power to raise the base to
        
    Returns:
        The result of base^exponent
    """
    return base ** exponent
