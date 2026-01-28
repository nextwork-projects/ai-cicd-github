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

def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b
  
def factorial(n):
    """Calculate the factorial of n."""
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n <= 1:
        return 1
    return n * factorial(n - 1)
  
def fibonacci(n):
		"""Return the nth Fibonacci number."""
		if n <= 0:
				raise ValueError("Fibonacci not defined for non-positive integers")
		elif n == 1:
				return 0
		elif n == 2:
				return 1
		else:
				a, b = 0, 1
				for _ in range(2, n):
						a, b = b, a + b
				return b