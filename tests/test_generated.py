import pytest

# Tests for add from app.py
import pytest

def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

def test_add_positive_integers():
    """Test addition of two positive integers."""
    assert add(2, 3) == 5
    assert add(100, 200) == 300

def test_add_negative_integers():
    """Test addition of two negative integers."""
    assert add(-2, -3) == -5
    assert add(-10, -5) == -15

def test_add_mixed_integers():
    """Test addition of a positive and a negative integer."""
    assert add(5, -2) == 3
    assert add(-8, 3) == -5
    assert add(10, -10) == 0

def test_add_with_zero():
    """Test addition involving zero."""
    assert add(0, 7) == 7
    assert add(-5, 0) == -5
    assert add(0, 0) == 0

def test_add_with_none_input():
    """Test addition when one or both inputs are None, expecting a TypeError."""
    with pytest.raises(TypeError):
        add(None, 5)
    with pytest.raises(TypeError):
        add(10, None)
    with pytest.raises(TypeError):
        add(None, None)

# Tests for is_even from app.py
import pytest

def is_even(n: int) -> bool:
    """Check if a number is even."""
    return n % 2 == 0

def test_is_even_positive_even_number():
    """Test with a positive even integer."""
    assert is_even(4) is True

def test_is_even_positive_odd_number():
    """Test with a positive odd integer."""
    assert is_even(7) is False

def test_is_even_zero():
    """Test with zero, which is considered an even number."""
    assert is_even(0) is True

def test_is_even_negative_even_number():
    """Test with a negative even integer."""
    assert is_even(-6) is True

def test_is_even_negative_odd_number():
    """Test with a negative odd integer."""
    assert is_even(-3) is False

def test_is_even_with_none_input():
    """Test that passing None raises a TypeError."""
    with pytest.raises(TypeError):
        is_even(None)

def test_is_even_with_float_input():
    """Test with a float, expecting it to be handled or raise error as per modulo behavior."""
    # In Python, 2.0 % 2 == 0.0, 2.5 % 2 == 0.5.
    # The function logic `n % 2 == 0` would evaluate to `0.0 == 0`, which is True.
    # While type hint is `int`, Python's dynamic typing allows floats.
    assert is_even(2.0) is True
    assert is_even(3.0) is False
    assert is_even(4.5) is False # 4.5 % 2 == 0.5, which is not 0

# Tests for reverse_string from app.py
```python
import pytest

def reverse_string(s: str) -> str:
    """Reverse a string."""
    return s[::-1]

def test_reverse_normal_string():
    """Test reversing a standard string."""
    assert reverse_string("hello") == "olleh"

def test_reverse_empty_string():
    """Test reversing an empty string."""
    assert reverse_string("") == ""

def test_reverse_single_character_string():
    """Test reversing a string with a single character."""
    assert reverse_string("a") == "a"

def test_reverse_string_with_spaces_and_numbers():
    """Test reversing a string containing spaces, numbers, and special characters."""
    assert reverse_string("Hello World 123!") == "!321 dlroW olleH"

def test_reverse_palindrome_string():
    """Test reversing a palindrome string (should remain unchanged)."""
    assert reverse_string("madam") == "madam"
```

# Tests for multiply from app.py
```python
import pytest

# The function to be tested (provided in the problem description)
def multiply(a,b):
    """Multiply two integers, a and b"""
    return a * b

def test_multiply_positive_integers():
    """Test multiplication of two positive integers."""
    assert multiply(3, 4) == 12
    assert multiply(1, 100) == 100
    assert multiply(1, 1) == 1

def test_multiply_negative_integers():
    """Test multiplication of two negative integers."""
    assert multiply(-2, -5) == 10
    assert multiply(-10, -1) == 10
    assert multiply(-1, -1) == 1

def test_multiply_mixed_sign_integers():
    """Test multiplication of integers with mixed positive and negative signs."""
    assert multiply(7, -3) == -21
    assert multiply(-4, 9) == -36

def test_multiply_by_zero():
    """Test multiplication when one or both operands are zero."""
    assert multiply(0, 5) == 0
    assert multiply(-12, 0) == 0
    assert multiply(0, 0) == 0

def test_multiply_with_none_input_raises_type_error():
    """Test that multiplying with None raises a TypeError."""
    with pytest.raises(TypeError):
        multiply(None, 5)
    with pytest.raises(TypeError):
        multiply(10, None)
    with pytest.raises(TypeError):
        multiply(None, None)

def test_multiply_with_float_inputs():
    """Test multiplication with float inputs, checking the actual behavior."""
    assert multiply(2.5, 2.0) == 5.0
    assert multiply(-1.5, 3.0) == -4.5
    assert multiply(0.5, 0.5) == 0.25
```

# Tests for factorial from app.py
```python
import pytest

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

def test_factorial_negative_number_raises_value_error():
    """Test that factorial raises ValueError for negative numbers."""
    with pytest.raises(ValueError, match="Factorial not defined for negative numbers"):
        factorial(-5)

def test_factorial_none_input_raises_type_error():
    """Test that factorial raises TypeError for None input."""
    with pytest.raises(TypeError):
        factorial(None)
```