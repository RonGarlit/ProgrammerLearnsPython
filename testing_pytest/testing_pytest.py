"""
Python Testing with pytest — A Self-Guided Lesson
==================================================
Run this file (with `python testing_pytest.py`) and follow along.

This is the FOURTH step in the path, right after `builtins_advanced` and
before the CSV lessons. It teaches you how to write automated TESTS for the
pure-Python code you already know how to write. We focus on:

  1. What testing is and why it matters
  2. pytest basics: test functions, `assert`, and running pytest
  3. Fixtures (setup & teardown)
  4. Parametrization (one test, many inputs)
  5. Testing functions & classes (a BankAccount)
  6. Testing exceptions with `pytest.raises`
  7. Markers & skipping
  8. A real-world mini task that combines everything

Everything here uses ONLY the Python standard library plus pytest — no NumPy,
no pandas. The classes you test (BankAccount, Inventory) mirror the ones you
built in `builtins_advanced`, so you are testing "real" code you already wrote.

Docs: https://docs.pytest.org/en/stable/
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Path handling with pathlib
# ---------------------------------------------------------------------------
# Same pattern as every other lesson: resolve paths relative to THIS script's
# folder so the lesson works no matter where you run it from.
# Docs: https://docs.python.org/3/library/pathlib.html

BASE_DIR = Path(__file__).resolve().parent


def data_path(filename):
    """Return the full path to a file inside this script's folder."""
    return BASE_DIR / filename


# ---------------------------------------------------------------------------
# CODE UNDER TEST (module level, so tests can import it)
# ---------------------------------------------------------------------------
# IMPORTANT: In `builtins_advanced`, these classes were defined INSIDE the
# section functions, so they could not be imported by other files. Here we
# define them at MODULE LEVEL on purpose — that is what makes them testable.
# This is the key idea of this lesson: to test code, it must be importable.
# Docs: https://docs.python.org/3/tutorial/modules.html


def add(a, b):
    """Return the sum of two numbers."""
    return a + b


def is_even(n):
    """Return True if n is even, False otherwise."""
    return n % 2 == 0


class BankAccount:
    """A simple bank account (mirrors the one from builtins_advanced)."""

    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return amount
        return 0

    def report(self):
        return f"{self.owner}: ${self.balance}"


class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the balance."""


class Account:
    """A stricter account that raises on overdraft (mirrors builtins_advanced)."""

    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(
                f"only ${self.balance} available, tried ${amount}"
            )
        self.balance -= amount
        return amount


class OutOfStockError(Exception):
    """Raised when there is not enough stock."""


class Inventory:
    """A small inventory system (mirrors builtins_advanced)."""

    def __init__(self) -> None:
        self.stock: dict[str, int] = {}

    def add(self, item: str, qty: int) -> None:
        self.stock[item] = self.stock.get(item, 0) + qty

    def remove(self, item: str, qty: int) -> None:
        if self.stock.get(item, 0) < qty:
            raise OutOfStockError(
                f"only {self.stock.get(item, 0)} of '{item}' in stock"
            )
        self.stock[item] -= qty

    def report(self) -> str:
        lines = [f"  {k}: {v}" for k, v in sorted(self.stock.items())]
        return "\n".join(lines) if lines else "  (empty)"


# ---------------------------------------------------------------------------
# SECTION 1: What is testing and why does it matter?
# ---------------------------------------------------------------------------
# A TEST is a small piece of code that checks whether another piece of code
# behaves the way you expect. The simplest tool Python gives you is `assert`:
#   assert <condition>
# If <condition> is True, nothing happens. If it is False, Python raises an
# AssertionError and the program stops. That is a test in its most basic form.
# Docs: https://docs.python.org/3/reference/simple_stmts.html#assert


def _demonstrate_failing_assert():
    """Show what a failing assert looks like (used by Section 1)."""
    # This assert is WRONG on purpose so we can see the failure.
    assert add(2, 2) == 5


def section_what_is_testing():
    print("=" * 50)
    print("SECTION 1: What is testing and why does it matter?")
    print("=" * 50)

    # A manual "test" using assert. If add() is correct, nothing prints.
    # Docs: https://docs.python.org/3/reference/simple_stmts.html#assert
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    print("add(2, 3) == 5  -> passed")
    print("add(-1, 1) == 0 -> passed")

    # When an assert fails, Python tells you exactly where.
    print()
    print("Now let's see what a FAILING assert looks like:")
    print("  assert add(2, 2) == 5  # this is wrong on purpose")
    try:
        _demonstrate_failing_assert()
    except AssertionError:
        print("  -> AssertionError raised! The test caught a bug.")
    print()

    print("Why test?")
    print("  1. Catch bugs early, before they reach users.")
    print("  2. Make sure old code still works when you change it (regressions).")
    print("  3. Document what your code is *supposed* to do.")
    print("  4. Give you confidence to refactor without fear.")
    print()

    print("The problem with raw assert: it stops at the FIRST failure and")
    print("gives you no summary. That is where a test FRAMEWORK like pytest")
    print("comes in — it collects all your tests, runs them, and reports.")
    # Docs: https://docs.pytest.org/en/stable/
    print()


# ---------------------------------------------------------------------------
# SECTION 2: pytest basics — test functions, assert, and running pytest
# ---------------------------------------------------------------------------
# pytest is a test framework. Its rules are simple:
#   * Test files are named `test_*.py` or `*_test.py`.
#   * Test functions are named `test_*`.
#   * Inside a test, you use plain `assert` — pytest enhances the failure
#     message automatically.
# You run it from the terminal with the command:  pytest
# Docs: https://docs.pytest.org/en/stable/getting-started.html


def section_pytest_basics():
    print("=" * 50)
    print("SECTION 2: pytest basics")
    print("=" * 50)

    print("pytest discovers tests by NAME:")
    print("  * files:  test_*.py  or  *_test.py")
    print("  * functions:  test_*")
    print()
    print("A minimal test file looks like this:")
    print()
    print("    # test_math_helpers.py")
    print("    from testing_pytest import add")
    print()
    print("    def test_add_positive():")
    print("        assert add(2, 3) == 5")
    print()
    print("    def test_add_negative():")
    print("        assert add(-1, 1) == 0")
    print()
    print("Run it from the terminal:")
    print("    pytest")
    print("    pytest -v          # verbose: shows each test name")
    print("    pytest test_math_helpers.py   # run one file")
    print("    pytest -k add      # run tests whose name contains 'add'")
    # Docs: https://docs.pytest.org/en/stable/how-to/usage.html
    print()

    # Show the real test files that ship with this lesson.
    test_files = sorted(BASE_DIR.glob("test_*.py"))
    print("Test files in this folder:")
    for f in test_files:
        print(f"  - {f.name}")
    print()

    print("Try it now: open a terminal in this folder and run `pytest`.")
    print("You should see a green summary like 'N passed'.")
    print()


# ---------------------------------------------------------------------------
# SECTION 3: Fixtures — shared setup & teardown
# ---------------------------------------------------------------------------
# A FIXTURE is a function that prepares something your tests need (an object,
# a file, a connection) and hands it to your test as an argument. pytest
# manages the lifecycle: it runs the fixture before the test and cleans up
# after. This removes duplicated setup code.
# Docs: https://docs.pytest.org/en/stable/how-to/fixtures.html


def section_fixtures():
    print("=" * 50)
    print("SECTION 3: Fixtures")
    print("=" * 50)

    print("Without a fixture, every test repeats setup:")
    print()
    print("    def test_deposit():")
    print("        acct = BankAccount('Ada', 100)   # setup repeated")
    print("        acct.deposit(50)")
    print("        assert acct.balance == 150")
    print()
    print("    def test_withdraw():")
    print("        acct = BankAccount('Ada', 100)   # setup repeated")
    print("        got = acct.withdraw(30)")
    print("        assert got == 30")
    print()
    print("With a fixture, the setup lives in ONE place:")
    print()
    print("    import pytest")
    print("    from testing_pytest import BankAccount")
    print()
    print("    @pytest.fixture")
    print("    def account():")
    print("        return BankAccount('Ada', 100)")
    print()
    print("    def test_deposit(account):      # pytest injects the fixture")
    print("        account.deposit(50)")
    print("        assert account.balance == 150")
    print()
    print("    def test_withdraw(account):")
    print("        got = account.withdraw(30)")
    print("        assert got == 30")
    print()
    print("Each test gets a FRESH fixture instance — tests stay independent.")
    # Docs: https://docs.pytest.org/en/stable/how-to/fixtures.html#fixtures
    print()


# ---------------------------------------------------------------------------
# SECTION 4: Parametrization — one test, many inputs
# ---------------------------------------------------------------------------
# @pytest.mark.parametrize lets you run the SAME test body with many different
# inputs. Instead of writing 5 near-identical tests, you write one and list
# the cases. pytest reports each case separately.
# Docs: https://docs.pytest.org/en/stable/how-to/parametrize.html


def section_parametrize():
    print("=" * 50)
    print("SECTION 4: Parametrization")
    print("=" * 50)

    print("Instead of many copy-pasted tests:")
    print()
    print("    def test_is_even_2():  assert is_even(2) is True")
    print("    def test_is_even_3():  assert is_even(3) is False")
    print("    def test_is_even_4():  assert is_even(4) is True")
    print()
    print("Write ONE parametrized test:")
    print()
    print("    import pytest")
    print("    from testing_pytest import is_even")
    print()
    print("    @pytest.mark.parametrize('n, expected', [")
    print("        (2, True),")
    print("        (3, False),")
    print("        (4, True),")
    print("        (0, True),")
    print("        (-2, True),")
    print("    ])")
    print("    def test_is_even(n, expected):")
    print("        assert is_even(n) is expected")
    print()
    print("pytest runs the test once per case and shows each one in the")
    print("verbose output, e.g. test_is_even[2-True].")
    # Docs: https://docs.pytest.org/en/stable/how-to/parametrize.html#parametrize
    print()


# ---------------------------------------------------------------------------
# SECTION 5: Testing functions & classes (a BankAccount)
# ---------------------------------------------------------------------------
# Now we test a real class. We check its behavior: deposits add money,
# withdrawals return the amount and reduce the balance, and you cannot
# withdraw more than you have.
# Docs: https://docs.pytest.org/en/stable/how-to/assert.html


def section_testing_classes():
    print("=" * 50)
    print("SECTION 5: Testing functions & classes")
    print("=" * 50)

    print("We test the BankAccount class (mirrored from builtins_advanced):")
    print()
    print("    from testing_pytest import BankAccount")
    print()
    print("    def test_initial_balance():")
    print("        acct = BankAccount('Ada')")
    print("        assert acct.balance == 0")
    print()
    print("    def test_deposit_increases_balance():")
    print("        acct = BankAccount('Ada', 100)")
    print("        acct.deposit(50)")
    print("        assert acct.balance == 150")
    print()
    print("    def test_withdraw_returns_amount():")
    print("        acct = BankAccount('Ada', 100)")
    print("        got = acct.withdraw(30)")
    print("        assert got == 30")
    print("        assert acct.balance == 70")
    print()
    print("    def test_withdraw_more_than_balance_returns_zero():")
    print("        acct = BankAccount('Ada', 10)")
    print("        got = acct.withdraw(100)")
    print("        assert got == 0")
    print("        assert acct.balance == 10  # unchanged")
    print()
    print("Notice each test builds its OWN account. That keeps tests isolated.")
    # Docs: https://docs.pytest.org/en/stable/how-to/assert.html#assert
    print()


# ---------------------------------------------------------------------------
# SECTION 6: Testing exceptions with pytest.raises
# ---------------------------------------------------------------------------
# Sometimes the correct behavior is to RAISE an exception. pytest.raises
# checks that a specific exception is raised — and fails the test if it is not.
# Docs: https://docs.pytest.org/en/stable/how-to/assert.html#assertraises


def section_testing_exceptions():
    print("=" * 50)
    print("SECTION 6: Testing exceptions with pytest.raises")
    print("=" * 50)

    print("The Account class raises InsufficientFundsError on overdraft:")
    print()
    print("    import pytest")
    print("    from testing_pytest import Account, InsufficientFundsError")
    print()
    print("    def test_withdraw_over_balance_raises():")
    print("        acct = Account(50)")
    print("        with pytest.raises(InsufficientFundsError):")
    print("            acct.withdraw(200)")
    print()
    print("You can also inspect the exception message:")
    print()
    print("    def test_withdraw_error_message():")
    print("        acct = Account(50)")
    print("        with pytest.raises(InsufficientFundsError) as exc_info:")
    print("            acct.withdraw(200)")
    print("        assert 'only $50 available' in str(exc_info.value)")
    print()
    print("If no exception is raised, pytest.raises FAILS the test — that is")
    print("the point: it proves the error path actually triggers.")
    # Docs: https://docs.pytest.org/en/stable/how-to/assert.html#assertraises
    print()


# ---------------------------------------------------------------------------
# SECTION 7: Markers & skipping
# ---------------------------------------------------------------------------
# MARKERS tag tests with metadata. Built-in markers include:
#   @pytest.mark.skip        — always skip this test
#   @pytest.mark.skipif      — skip when a condition is True
#   @pytest.mark.xfail       — expect the test to fail (known issue)
# You can also define CUSTOM markers (e.g. @pytest.mark.slow) and run only
# those with `pytest -m slow`.
# Docs: https://docs.pytest.org/en/stable/how-to/mark.html


def section_markers():
    print("=" * 50)
    print("SECTION 7: Markers & skipping")
    print("=" * 50)

    print("Skip a test that is not ready yet:")
    print()
    print("    import pytest")
    print()
    print("    @pytest.mark.skip(reason='not implemented yet')")
    print("    def test_future_feature():")
    print("        ...")
    print()
    print("Skip conditionally (e.g. only on certain platforms):")
    print()
    print("    import sys")
    print()
    print("    @pytest.mark.skipif(sys.platform == 'win32',")
    print("                        reason='does not run on Windows')")
    print("    def test_unix_only():")
    print("        ...")
    print()
    print("Mark a known-failing test so it does not fail the suite:")
    print()
    print("    @pytest.mark.xfail(reason='known bug #42')")
    print("    def test_known_bug():")
    print("        ...")
    print()
    print("Custom markers need registering in pyproject.toml under")
    print("[tool.pytest.ini_options] markers = [...] to avoid warnings.")
    # Docs: https://docs.pytest.org/en/stable/how-to/mark.html#mark
    print()


# ---------------------------------------------------------------------------
# SECTION 8: Mini task — write a full test suite
# ---------------------------------------------------------------------------
# Task: write tests for the Inventory class (mirrored from builtins_advanced).
# Cover: adding stock, removing stock, the report format, and the
# OutOfStockError path. A starter file `test_inventory.py` ships with the
# lesson — try to complete it yourself before peeking at the solution notes.
# Docs: https://docs.pytest.org/en/stable/


def section_mini_task():
    print("=" * 50)
    print("SECTION 8: Mini task — test the Inventory class")
    print("=" * 50)

    print("The Inventory class (from builtins_advanced) has three methods:")
    print("  add(item, qty)      -> adds stock (accumulates)")
    print("  remove(item, qty)   -> removes stock, raises OutOfStockError")
    print("  report()            -> sorted 'item: qty' lines, or '(empty)'")
    print()
    print("Write tests that check:")
    print("  1. add() accumulates: add('laptop', 5) then add('laptop', 3)")
    print("     -> stock['laptop'] == 8")
    print("  2. remove() reduces stock and returns nothing (None)")
    print("  3. remove() with too much raises OutOfStockError")
    print("  4. report() on an empty inventory returns '(empty)'")
    print("  5. report() sorts items alphabetically")
    print()
    print("A starter test_inventory.py is provided. Run `pytest` to see which")
    print("tests pass and which are left for you to write.")
    # Docs: https://docs.pytest.org/en/stable/how-to/assert.html
    print()


# ---------------------------------------------------------------------------
# OPTION 0: Clean up the generated files
# ---------------------------------------------------------------------------
# pytest writes a `.pytest_cache` folder and `__pycache__` folders. This
# helper removes the cache so you can start fresh. (The test files themselves
# are kept — they are the point of the lesson.)


DEFAULT_CLEANUP = [
    data_path(".pytest_cache"),
    data_path("__pycache__"),
]


def _remove_path(path):
    """Delete a file or a directory tree, returning True if anything was removed."""
    if not path.exists():
        return False
    if path.is_dir():
        # Remove a directory tree (cache folders) deepest-first.
        for child in sorted(path.rglob("*"), reverse=True):
            if child.is_file():
                child.unlink()
        path.rmdir()
    else:
        path.unlink()
    return True


def section_cleanup():
    print("=" * 50)
    print("OPTION 0: Cleaning up the generated files")
    print("=" * 50)

    removed = []
    for path in DEFAULT_CLEANUP:
        if _remove_path(path):
            removed.append(path.name)

    if removed:
        print("Removed:")
        for name in removed:
            print(f"  - {name}")
    else:
        print("Nothing to remove — none of the files were found.")

    print()
    print("The caches will be recreated automatically when you run pytest.")
    print()


# ---------------------------------------------------------------------------
# MAIN MENU — brings all sections together
# ---------------------------------------------------------------------------
# The `if __name__ == "__main__":` guard ensures this code only runs
# when the script is executed directly, not when imported as a module.
# This is CRITICAL here: the test files IMPORT this module, and importing
# must NOT launch the menu.

SECTIONS = {
    "0": ("Clean up the generated files", section_cleanup),
    "1": ("What is testing and why?", section_what_is_testing),
    "2": ("pytest basics", section_pytest_basics),
    "3": ("Fixtures", section_fixtures),
    "4": ("Parametrization", section_parametrize),
    "5": ("Testing functions & classes", section_testing_classes),
    "6": ("Testing exceptions", section_testing_exceptions),
    "7": ("Markers & skipping", section_markers),
    "8": ("Mini task: test the Inventory class", section_mini_task),
}


def main():
    print("\n🧪 Welcome to the pytest Testing Tutorial!\n")
    print("You'll explore these concepts, one step at a time:\n")
    for number, (title, _section_function) in SECTIONS.items():
        print(f"  {number}. {title}")
    print()

    keep_going = True
    while keep_going:
        choice = input("Type a number (0-8) to run a section, or q to quit: ").strip()

        if choice.lower() == "q":
            print("Thanks for learning with us. Goodbye!")
            keep_going = False
        elif choice in SECTIONS:
            _title, section_function = SECTIONS[choice]
            section_function()
        else:
            print("Hmm, that isn't a valid option. Try a number 0-8 or 'q'.")


if __name__ == "__main__":
    main()
