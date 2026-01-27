from app import add, is_even, reverse_string, multiply, factorial
import pytest

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-1, -4) == -5

def test_add_positive_and_negative():
    assert add(5, -2) == 3

def test_add_with_zero():
    assert add(0, 7) == 7

def test_is_even_positive_even():
    assert is_even(4) is True

def test_is_even_positive_odd():
    assert is_even(7) is False

def test_is_even_zero():
    assert is_even(0) is True

def test_is_even_negative_even():
    assert is_even(-2) is True

def test_is_even_negative_odd():
    assert is_even(-5) is False

def test_reverse_string_normal_case():
    assert reverse_string("hello") == "olleh"

def test_reverse_string_palindrome():
    assert reverse_string("madam") == "madam"

def test_reverse_string_with_spaces():
    assert reverse_string("hello world") == "dlrow olleh"

def test_reverse_string_empty():
    assert reverse_string("") == ""

def test_reverse_string_single_character():
    assert reverse_string("a") == "a"

def test_multiply_positive_numbers():
    assert multiply(2, 3) == 6

def test_multiply_one_positive_one_negative():
    assert multiply(5, -2) == -10

def test_multiply_two_negative_numbers():
    assert multiply(-3, -4) == 12

def test_multiply_by_zero():
    assert multiply(0, 7) == 0

def test_multiply_by_one():
    assert multiply(1, 10) == 10

def test_factorial_positive_number():
    assert factorial(5) == 120

def test_factorial_zero():
    assert factorial(0) == 1

def test_factorial_one():
    assert factorial(1) == 1

def test_factorial_negative_number_raises_error():
    with pytest.raises(ValueError, match="Factorial not defined for negative numbers"):
        factorial(-1)

def test_factorial_larger_number():
    assert factorial(7) == 5040