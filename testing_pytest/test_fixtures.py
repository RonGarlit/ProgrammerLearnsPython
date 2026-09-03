"""
Test file for the pytest lesson — Section 3: fixtures.

A FIXTURE is a function that prepares something your tests need and hands it
to the test as an argument. pytest runs the fixture before each test that
asks for it, so every test gets a FRESH instance.

Run it from this folder with:
    pytest test_fixtures.py -v

Docs: https://docs.pytest.org/en/stable/how-to/fixtures.html
"""

import pytest

from testing_pytest import BankAccount

"""_summary_
    This fixture provides a fresh BankAccount instance for each test.
    Look in the local variables of the test function to see the account instance.
    As you step through the tests, you'll see the account instance in the local variables.
    """


@pytest.fixture
def account():
    """A fresh BankAccount for each test that asks for it."""
    return BankAccount("Ada", 100)


def test_deposit(account):
    account.deposit(50)
    assert account.balance == 150


def test_withdraw(account):
    got = account.withdraw(30)
    assert got == 30
    assert account.balance == 70


def test_report(account):
    assert account.report() == "Ada: $100"


def test_fixture_is_fresh(account):
    # Each test gets its own account, so this starts at 100 again.
    assert account.balance == 100
