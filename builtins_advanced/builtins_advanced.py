"""
Python Advanced Built-ins — A Self-Guided Lesson
=================================================
Run this file (with `python builtins_advanced.py`) and follow along.

This is the THIRD step after `builtins_basics` and `builtins_intermediate`.
Basics covered the core language; intermediate covered everyday stdlib tools.
Here we go deeper into Python's power features — the ones that let you design
clean, reusable, professional code. We focus on:

  1. Object-oriented programming (classes)
  2. Inheritance & dunder ("double underscore") methods
  3. Decorators
  4. Context managers (custom `with` blocks)
  5. The `itertools` module
  6. The `functools` module
  7. Type hints with the `typing` module
  8. Deep error handling (custom exceptions)
  9. A real-world mini task that combines everything

Docs: https://docs.python.org/3/
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from functools import cache, partial, reduce
from itertools import chain, count, groupby, product
from pathlib import Path
from typing import Union

# ---------------------------------------------------------------------------
# Path handling with pathlib
# ---------------------------------------------------------------------------
# pathlib is the modern, object-oriented way to handle file paths (the
# intermediate lesson teaches it in Section 1). `Path(__file__)` is this
# script's own location; `.resolve()` makes it absolute; `.parent` walks up
# to the folder containing it. The `/` operator joins path pieces — much
# cleaner than os.path.join().
# Docs: https://docs.python.org/3/library/pathlib.html

BASE_DIR = Path(__file__).resolve().parent


def data_path(filename):
    """Return the full path to a file inside this script's folder."""
    return BASE_DIR / filename


# ---------------------------------------------------------------------------
# SECTION 1: Object-oriented programming (classes)
# ---------------------------------------------------------------------------
# A class is a blueprint for creating OBJECTS — things that bundle data
# (attributes) and behavior (methods) together.
# Docs: https://docs.python.org/3/tutorial/classes.html


def section_oop():
    print("=" * 50)
    print("SECTION 1: Object-oriented programming (classes)")
    print("=" * 50)

    class BankAccount:
        """A simple bank account."""

        def __init__(self, owner, balance=0):
            self.owner = owner  # an attribute (data)
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

    # Create objects (instances) from the class.
    ada = BankAccount("Ada", 100)
    grace = BankAccount("Grace")

    ada.deposit(50)
    print("Created two accounts.")
    print("ada.report()  ->", ada.report())
    print("grace.report() ->", grace.report())
    print("ada.withdraw(30) ->", ada.withdraw(30))
    print("ada.balance ->", ada.balance)
    print()

    # --- @dataclass: a class for mostly-data, with the boilerplate done ---
    # Many classes just hold values. @dataclass auto-generates __init__,
    # __repr__, and __eq__ from the declared fields — the same dunders we
    # hand-wrote in Section 2, written for you.
    # Docs: https://docs.python.org/3/library/dataclasses.html
    @dataclass
    class Product:
        name: str  # a "field" — like an attribute with a type hint
        price: float
        tags: list = field(default_factory=list)  # safe default: a NEW list

    pen = Product("Pen", 1.50, ["office", "writing"])
    book = Product("Book", 12.00)
    print("@dataclass Product:")
    print("  pen  =", pen)  # __repr__ was generated for us!
    print("  book =", book)
    print("  pen.price ->", pen.price)
    print(
        "  pen == Product('Pen', 1.50, ['office', 'writing'])? ->",
        pen == Product("Pen", 1.50, ["office", "writing"]),
    )  # __eq__ too
    print()


# ---------------------------------------------------------------------------
# SECTION 2: Inheritance & dunder methods
# ---------------------------------------------------------------------------
# INHERITANCE: a class can extend another, keeping its behavior and adding
# its own. DUNDER methods (__str__, __eq__, __repr__) customize how objects
# print and compare.
# Docs: https://docs.python.org/3/tutorial/classes.html#inheritance
# Docs: https://docs.python.org/3/reference/datamodel.html#special-method-names


def section_inheritance():
    print("=" * 50)
    print("SECTION 2: Inheritance & dunder methods")
    print("=" * 50)

    class Pet:
        def __init__(self, name):
            self.name = name

        def speak(self):
            return f"{self.name} makes a sound"

        # Dunder: how the object prints.
        def __str__(self):
            return f"Pet({self.name})"

        # Dunder: how two pets compare equal.
        def __eq__(self, other):
            return isinstance(other, Pet) and self.name == other.name

    class Dog(Pet):
        def speak(self):
            return f"{self.name} says WOOF!"  # override the parent method

    class Cat(Pet):
        def speak(self):
            return f"{self.name} says meow~"

    buddy = Dog("Buddy")
    whiskers = Cat("Whiskers")
    print("Polymorphism — shared name, different behavior:")
    print("  ", buddy.speak())
    print("  ", whiskers.speak())
    print()

    print("__str__:", str(buddy))
    print("__eq__: buddy == Cat('Buddy')?", buddy == Cat("Buddy"))
    print()


# ---------------------------------------------------------------------------
# SECTION 3: Decorators
# ---------------------------------------------------------------------------
# A decorator is a function that wraps another function to add behavior —
# like logging, timing, or access control — without changing its code.
# Docs: https://docs.python.org/3/tutorial/classes.html#decorators


def section_decorators():
    print("=" * 50)
    print("SECTION 3: Decorators")
    print("=" * 50)

    # Define a decorator that logs before and after calling a function.
    def log_call(func):
        def wrapper(*args, **kwargs):
            print(f"  → calling {func.__name__} with args={args}")
            result = func(*args, **kwargs)
            print(f"  ← {func.__name__} returned {result!r}")
            return result

        return wrapper

    @log_call
    def add(a, b):
        return a + b

    print("Decorated add(2, 3):")
    add(2, 3)
    print()

    # Built-in decorators.
    class Circle:
        def __init__(self, radius):
            self._radius = radius

        @property
        def area(self):
            """A property exposes a method as an attribute."""
            return 3.14159 * self._radius**2

        @staticmethod
        def description():
            return "A circle shape"

    c = Circle(5)
    print("Property access c.area ->", c.area)  # no parentheses!
    print("Static method ->", Circle.description())
    print()


# ---------------------------------------------------------------------------
# SECTION 4: Context managers (custom with blocks)
# ---------------------------------------------------------------------------
# The `with` statement guarantees cleanup (like closing a file) even if an
# error occurs. We can build our OWN context manager with __enter__/__exit__.
# Docs: https://docs.python.org/3/reference/datamodel.html#context-managers


def section_context():
    print("=" * 50)
    print("SECTION 4: Context managers")
    print("=" * 50)

    class Timer:
        """Times how long a with-block takes."""

        def __enter__(self):
            import time

            self.start = time.time()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            import time

            self.elapsed = time.time() - self.start
            print(f"  elapsed: {self.elapsed:.4f}s")
            return False  # don't suppress any exception

    print("Running a timed block:")
    with Timer():
        total = sum(range(1_000_000))
    print("  sum =", total)
    print()

    # The classic use: files close automatically.
    print("Writing then reading with a context manager:")
    path = data_path("managed_file.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("Managed write!")
    with open(path, encoding="utf-8") as f:
        print("  read:", f.read())
    print()


# ---------------------------------------------------------------------------
# SECTION 5: The itertools module
# ---------------------------------------------------------------------------
# itertools provides fast, memory-efficient iterators for combinatorics and
# looping patterns.
# Docs: https://docs.python.org/3/library/itertools.html


def section_itertools():
    print("=" * 50)
    print("SECTION 5: The itertools module")
    print("=" * 50)

    # chain: combine multiple iterables into one.
    chained = list(chain([1, 2], [3, 4], [5, 6]))
    print("chain([1,2],[3,4],[5,6]):", chained)
    print()

    # product: Cartesian product of iterables.
    product_ab = list(product("AB", [1, 2]))
    print("product('AB', [1,2]):", product_ab)
    print()

    # count: infinite counter (take a few with zip/islice).
    counted = list(zip(range(5), count(10)))
    print("count(10) with zip(range(5)):", counted)
    print()

    # groupby: group adjacent items by a key function.
    data = [
        ("fruit", "apple"),
        ("fruit", "banana"),
        ("veg", "carrot"),
        ("veg", "celery"),
    ]
    for key, group in groupby(data, key=lambda item: item[0]):
        print(f"  group '{key}':", [item[1] for item in group])
    print()


# ---------------------------------------------------------------------------
# SECTION 6: The functools module
# ---------------------------------------------------------------------------
# functools has higher-order functions and caching helpers.
#   reduce    — fold a sequence into a single value
#   lru_cache — cache function results (memoization)
#   partial   — fix some arguments of a function
# Docs: https://docs.python.org/3/library/functools.html


def section_functools():
    print("=" * 50)
    print("SECTION 6: The functools module")
    print("=" * 50)

    # reduce: accumulate left-to-right.
    total = reduce(lambda a, b: a + b, [1, 2, 3, 4, 5])
    print("reduce(add, [1..5]):", total)
    print()

    # lru_cache: memoize expensive function calls.
    @cache
    def fib(n):
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    print("fib(30) with lru_cache:", fib(30))
    print("  cache info:", fib.cache_info())
    print()

    # partial: pre-fill some arguments.
    def power(base, exponent):
        return base**exponent

    square = partial(power, exponent=2)
    print("partial(square)(5):", square(5))
    print()


# ---------------------------------------------------------------------------
# SECTION 7: Type hints with the typing module
# ---------------------------------------------------------------------------
# Type hints document what a function expects and returns. Tools (mypy,
# Pylance) can catch bugs before you run the code.
# Docs: https://docs.python.org/3/library/typing.html


def section_type_hints():
    print("=" * 50)
    print("SECTION 7: Type hints")
    print("=" * 50)

    def add(a: int, b: int) -> int:
        """Add two integers. The -> int names the return type."""
        return a + b

    def describe(items: list[str]) -> str:
        return f"{len(items)} items: {', '.join(items)}"

    # Optional and Union model "maybe this type, maybe None".
    def safe_int(value: str | None = None) -> int | None:
        if value is None:
            return None
        try:
            return int(value)
        except ValueError:
            return None

    print("add(2, 3):", add(2, 3))
    print("describe(['a','b']):", describe(["a", "b"]))
    print("safe_int('42'):", safe_int("42"))
    print("safe_int()   :", safe_int())
    print("safe_int('hi'):", safe_int("hi"))
    # Union[int, str] is the classic spelling; modern Python allows `int | str`.
    # We show Union here on purpose — you'll see it in lots of existing code.
    print("Union example type:", Union[int, str])  # noqa: UP007
    print("Callable type:", Callable[[int, int], int])
    print()


# ---------------------------------------------------------------------------
# SECTION 8: Deep error handling (custom exceptions)
# ---------------------------------------------------------------------------
# Beyond the basic try/except, we can RAISE exceptions and define our OWN
# exception classes for clearer error handling.
# Docs: https://docs.python.org/3/tutorial/errors.html


def section_errors():
    print("=" * 50)
    print("SECTION 8: Deep error handling")
    print("=" * 50)

    # Define a custom exception type.
    class InsufficientFundsError(Exception):
        """Raised when a withdrawal exceeds the balance."""

    class Account:
        def __init__(self, balance):
            self.balance = balance

        def withdraw(self, amount):
            if amount > self.balance:
                raise InsufficientFundsError(
                    f"only ${self.balance} available, tried ${amount}"
                )
            self.balance -= amount
            return amount

    acct = Account(50)
    try:
        acct.withdraw(200)
    except InsufficientFundsError as e:
        print("Caught custom exception:", e)
    print()

    # try / except / else / finally — else runs on success, finally always runs.
    def divide(a, b):
        try:
            result = a / b
        except ZeroDivisionError:
            return "division by zero"
        else:
            return f"result = {result}"
        finally:
            print("  (finally block always runs)")

    print("divide(10, 2):", divide(10, 2))
    print("divide(10, 0):", divide(10, 0))
    print()


# ---------------------------------------------------------------------------
# SECTION 9: A real-world mini task (combines everything)
# ---------------------------------------------------------------------------
# Task: build a small inventory system using a class, custom exception,
# type hints, and a dataclass-like report — pulling the whole lesson together.


def section_summary_task():
    print("=" * 50)
    print("SECTION 9: Mini task — inventory system")
    print("=" * 50)

    # A custom exception from Section 8.
    class OutOfStockError(Exception):
        """Raised when there is not enough stock."""

    # A class with type-hinted methods (Sections 1, 7).
    class Inventory:
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

    store = Inventory()
    store.add("laptop", 5)
    store.add("mouse", 20)
    store.add("laptop", 3)
    print("Stock after adds:")
    print(store.report())
    print()

    store.remove("laptop", 4)
    print("After removing 4 laptops:")
    print(store.report())
    print()

    # Use a decorator idea: wrap the removal in try/except with a custom error.
    try:
        store.remove("mouse", 500)
    except OutOfStockError as e:
        print("Caught OutOfStockError:", e)
    print()


# ---------------------------------------------------------------------------
# OPTION 0: Clean up the generated files
# ---------------------------------------------------------------------------
# Some sections write small output files. This helper removes them so you can
# start fresh.


DEFAULT_CLEANUP = [
    data_path("managed_file.txt"),
]


def section_cleanup():
    print("=" * 50)
    print("OPTION 0: Cleaning up the generated files")
    print("=" * 50)

    removed = []
    for path in DEFAULT_CLEANUP:
        if path.exists():  # pathlib: no os.path.exists() needed
            path.unlink()  # pathlib's "delete this file"
            removed.append(path.name)  # .name = just the filename part

    if removed:
        print("Removed:")
        for name in removed:
            print(f"  - {name}")
    else:
        print("Nothing to remove — none of the files were found.")

    print()
    print("The files will be recreated automatically when needed.")
    print()


# ---------------------------------------------------------------------------
# MAIN MENU — brings all sections together
# ---------------------------------------------------------------------------
# The `if __name__ == "__main__":` guard ensures this code only runs
# when the script is executed directly, not when imported as a module.

# A DICT as a "dispatch table": each menu number maps to a (title, function)
# pair. This replaces a long if/elif chain — to add a section you just add
# one line here, and the menu printing + lookup below handle the rest.
# Docs: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
SECTIONS = {
    "0": ("Clean up the generated files", section_cleanup),
    "1": ("OOP: classes", section_oop),
    "2": ("Inheritance & dunder methods", section_inheritance),
    "3": ("Decorators", section_decorators),
    "4": ("Context managers", section_context),
    "5": ("The itertools module", section_itertools),
    "6": ("The functools module", section_functools),
    "7": ("Type hints", section_type_hints),
    "8": ("Deep error handling", section_errors),
    "9": ("Mini task: an inventory system", section_summary_task),
}


def main():
    print("\n🚀 Welcome to the Advanced Built-ins Tutorial!\n")
    print("You'll explore these concepts, one step at a time:\n")
    # Print the menu straight from the SECTIONS dict — no duplication.
    for number, (title, _section_function) in SECTIONS.items():
        print(f"  {number}. {title}")
    print()

    keep_going = True
    while keep_going:
        choice = input("Type a number (0-9) to run a section, or q to quit: ").strip()

        if choice.lower() == "q":
            print("Thanks for learning with us. Goodbye!")
            keep_going = False
        elif choice in SECTIONS:
            # dict lookup: we've already checked membership with `in`,
            # so indexing SECTIONS[choice] is safe here.
            _title, section_function = SECTIONS[choice]
            section_function()  # call the function stored in the dict!
        else:
            print("Hmm, that isn't a valid option. Try a number 0-9 or 'q'.")


if __name__ == "__main__":
    main()
