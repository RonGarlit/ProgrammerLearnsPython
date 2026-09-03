"""
Test file for the pytest lesson — Section 2: pytest basics.

This file demonstrates the CORE pytest rules:
  * Files are named `test_*.py`.
  * Test functions are named `test_*`.
  * Inside a test you use plain `assert`.

Run it from this folder with:
    pytest
    pytest -v
    pytest test_math_helpers.py

Docs: https://docs.pytest.org/en/stable/getting-started.html
"""

from testing_pytest import add, is_even


def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-1, 1) == 0


def test_add_zero():
    assert add(0, 0) == 0


def test_add_floats():
    assert add(1.5, 2.5) == 4.0


def test_is_even_true():
    assert is_even(4) is True


def test_is_even_false():
    assert is_even(3) is False
