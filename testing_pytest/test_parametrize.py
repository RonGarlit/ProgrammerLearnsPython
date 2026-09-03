"""
Test file for the pytest lesson — Section 4: parametrization.

@parametrize runs the SAME test body with many different inputs. pytest
reports each case separately, so you can see exactly which input failed.

Run it from this folder with:
    pytest test_parametrize.py -v

Docs: https://docs.pytest.org/en/stable/how-to/parametrize.html
"""

import pytest

from testing_pytest import is_even


@pytest.mark.parametrize(
    "n, expected",
    [
        (2, True),
        (4, True),
        (0, True),
        (-2, True),
        (3, False),
        (7, False),
        (-1, False),
    ],
)
def test_is_even(n, expected):
    assert is_even(n) is expected
