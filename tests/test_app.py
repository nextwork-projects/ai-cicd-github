"""Tests for app.py - you'll add more!"""

from app import add, is_even, reverse_string, multiple


class TestMath:
    """Tests for math functions."""

    def test_add_positive(self):
        assert add(2, 3) == 5

    def test_add_negative(self):
        assert add(-1, -1) == -2

    def test_multiple(self):
        assert multiple(9,9) == 81


class TestStrings:
    """Tests for string functions."""

    def test_reverse(self):
        assert reverse_string("hello") == "olleh"

    def test_is_even(self):
        assert is_even(4) is True
        assert is_even(3) is False
