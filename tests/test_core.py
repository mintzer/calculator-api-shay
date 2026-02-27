"""Tests for the core calculator functions."""

import pytest

from core import add, divide, multiply, subtract


class TestAdd:
    """Tests for the add function."""

    def test_add_positive_integers(self):
        assert add(1, 2) == 3

    def test_add_negative_numbers(self):
        assert add(-1, -2) == -3

    def test_add_mixed_signs(self):
        assert add(-5, 3) == -2

    def test_add_floats(self):
        assert add(1.5, 2.3) == pytest.approx(3.8)

    def test_add_zeros(self):
        assert add(0, 0) == 0


class TestSubtract:
    """Tests for the subtract function."""

    def test_subtract_positive_integers(self):
        assert subtract(5, 3) == 2

    def test_subtract_negative_result(self):
        assert subtract(3, 5) == -2

    def test_subtract_negative_numbers(self):
        assert subtract(-1, -2) == 1

    def test_subtract_floats(self):
        assert subtract(5.5, 2.3) == pytest.approx(3.2)

    def test_subtract_zeros(self):
        assert subtract(0, 0) == 0


class TestMultiply:
    """Tests for the multiply function."""

    def test_multiply_positive_integers(self):
        assert multiply(3, 4) == 12

    def test_multiply_negative_numbers(self):
        assert multiply(-3, -4) == 12

    def test_multiply_mixed_signs(self):
        assert multiply(-3, 4) == -12

    def test_multiply_by_zero(self):
        assert multiply(5, 0) == 0

    def test_multiply_floats(self):
        assert multiply(2.5, 4.0) == pytest.approx(10.0)


class TestDivide:
    """Tests for the divide function."""

    def test_divide_positive_integers(self):
        assert divide(10, 2) == 5.0

    def test_divide_negative_numbers(self):
        assert divide(-10, -2) == 5.0

    def test_divide_mixed_signs(self):
        assert divide(-10, 2) == -5.0

    def test_divide_floats(self):
        assert divide(7.5, 2.5) == pytest.approx(3.0)

    def test_divide_by_zero_raises_value_error(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)

    def test_divide_zero_by_nonzero(self):
        assert divide(0, 5) == 0.0
