"""
Test file for the pytest lesson — Section 8: mini task.

Task: complete the tests for the Inventory class (mirrored from
builtins_advanced). The first test is written for you as an example.
Fill in the rest, then run `pytest` to check your work.

Run it from this folder with:
    pytest test_inventory.py -v

Docs: https://docs.pytest.org/en/stable/how-to/assert.html
"""

from testing_pytest import Inventory


def test_add_accumulates():
    store = Inventory()
    store.add("laptop", 5)
    store.add("laptop", 3)
    assert store.stock["laptop"] == 8


# TODO: write a test that add() stores a brand-new item correctly.
#   store = Inventory()
#   store.add("mouse", 20)
#   assert store.stock["mouse"] == 20


# TODO: write a test that remove() reduces stock.
#   store = Inventory()
#   store.add("laptop", 5)
#   store.remove("laptop", 2)
#   assert store.stock["laptop"] == 3


# TODO: write a test that remove() with too much raises OutOfStockError.
#   store = Inventory()
#   store.add("mouse", 1)
#   with pytest.raises(OutOfStockError):
#       store.remove("mouse", 500)


# TODO: write a test that report() on an empty inventory returns "(empty)".
#   store = Inventory()
#   assert store.report() == "  (empty)"


# TODO: write a test that report() sorts items alphabetically.
#   store = Inventory()
#   store.add("zebra", 1)
#   store.add("apple", 2)
#   assert store.report() == "  apple: 2\n  zebra: 1"
