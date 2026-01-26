from app import factorial

def factorial(n):
    """Calculate the factorial of n."""
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def test_factorial_positive_number():
    """Test factorial for a typical positive integer."""
    assert factorial(5) == 120

def test_factorial_zero():
    """Test factorial for n=0, an edge case."""
    assert factorial(0) == 1

def test_factorial_one():
    """Test factorial for n=1, another edge case."""
    assert factorial(1) == 1