"""Unit tests for core calculator functions."""

import pytest

from core import add, divide, multiply, subtract


class TestAdd:
    """Tests for the add function."""

    def test_positive_numbers(self) -> None:
        assert add(2, 3) == 5

    def test_negative_numbers(self) -> None:
        assert add(-1, -2) == -3

    def test_mixed_signs(self) -> None:
        assert add(-1, 3) == 2

    def test_zeros(self) -> None:
        assert add(0, 0) == 0

    def test_floats(self) -> None:
        assert add(1.5, 2.5) == 4.0


class TestSubtract:
    """Tests for the subtract function."""

    def test_positive_numbers(self) -> None:
        assert subtract(5, 3) == 2

    def test_negative_result(self) -> None:
        assert subtract(3, 5) == -2

    def test_negative_numbers(self) -> None:
        assert subtract(-1, -2) == 1

    def test_zeros(self) -> None:
        assert subtract(0, 0) == 0

    def test_floats(self) -> None:
        assert subtract(5.5, 2.5) == 3.0


class TestMultiply:
    """Tests for the multiply function."""

    def test_positive_numbers(self) -> None:
        assert multiply(2, 3) == 6

    def test_negative_numbers(self) -> None:
        assert multiply(-2, -3) == 6

    def test_mixed_signs(self) -> None:
        assert multiply(-2, 3) == -6

    def test_by_zero(self) -> None:
        assert multiply(5, 0) == 0

    def test_floats(self) -> None:
        assert multiply(2.5, 4.0) == 10.0


class TestDivide:
    """Tests for the divide function."""

    def test_positive_numbers(self) -> None:
        assert divide(6, 3) == 2.0

    def test_negative_numbers(self) -> None:
        assert divide(-6, -3) == 2.0

    def test_mixed_signs(self) -> None:
        assert divide(-6, 3) == -2.0

    def test_floats(self) -> None:
        assert divide(7.5, 2.5) == 3.0

    def test_division_by_zero_raises(self) -> None:
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(1, 0)

    def test_result_is_float(self) -> None:
        assert divide(7, 2) == 3.5
