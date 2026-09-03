"""
Test file for the pytest lesson — Section 6: testing exceptions.

pytest.raises checks that a specific exception is raised. If the exception is
NOT raised, the test FAILS — which is exactly what we want: it proves the
error path actually triggers.

Run it from this folder with:
    pytest test_exceptions.py -v

Docs: https://docs.pytest.org/en/stable/how-to/assert.html#assertraises
"""

import pytest

from testing_pytest import Account, InsufficientFundsError


def test_withdraw_within_balance_succeeds():
    acct = Account(50)
    got = acct.withdraw(30)
    assert got == 30
    assert acct.balance == 20


def test_withdraw_over_balance_raises():
    acct = Account(50)
    with pytest.raises(InsufficientFundsError):
        acct.withdraw(200)


def test_withdraw_error_message():
    acct = Account(50)
    with pytest.raises(InsufficientFundsError) as exc_info:
        acct.withdraw(200)
    assert "only $50 available" in str(exc_info.value)


def test_withdraw_exact_balance_succeeds():
    acct = Account(50)
    got = acct.withdraw(50)
    assert got == 50
    assert acct.balance == 0
