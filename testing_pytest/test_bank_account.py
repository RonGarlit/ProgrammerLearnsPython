"""
Test file for the pytest lesson — Section 5: testing functions & classes.

Here we test the BankAccount class (mirrored from builtins_advanced). Each
test builds its OWN account so the tests stay independent.

Run it from this folder with:
    pytest test_bank_account.py -v

Docs: https://docs.pytest.org/en/stable/how-to/assert.html
"""

from testing_pytest import BankAccount


def test_initial_balance_defaults_to_zero():
    acct = BankAccount("Ada")
    assert acct.balance == 0


def test_initial_balance_with_amount():
    acct = BankAccount("Ada", 100)
    assert acct.balance == 100


def test_deposit_increases_balance():
    acct = BankAccount("Ada", 100)
    acct.deposit(50)
    assert acct.balance == 150


def test_withdraw_returns_amount():
    acct = BankAccount("Ada", 100)
    got = acct.withdraw(30)
    assert got == 30


def test_withdraw_reduces_balance():
    acct = BankAccount("Ada", 100)
    acct.withdraw(30)
    assert acct.balance == 70


def test_withdraw_more_than_balance_returns_zero():
    acct = BankAccount("Ada", 10)
    got = acct.withdraw(100)
    assert got == 0


def test_withdraw_more_than_balance_leaves_balance_unchanged():
    acct = BankAccount("Ada", 10)
    acct.withdraw(100)
    assert acct.balance == 10


def test_report_format():
    acct = BankAccount("Ada", 100)
    assert acct.report() == "Ada: $100"
