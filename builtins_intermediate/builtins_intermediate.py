"""
Python Intermediate Built-ins — A Self-Guided Lesson
=====================================================
Run this file (with `python builtins_intermediate.py`) and follow along.

This is the SECOND step after `builtins_basics`. The basics taught the core
language. Here we cover the practical, everyday *standard library* modules
and syntax that make Python truly productive — all built-in, nothing to
`pip install`. We focus on:

  1. Working with text files using `pathlib.Path`
  2. The `json` module — Python's universal data-exchange format
  3. The `datetime` module — dates, times, formatting, and math
  4. The `collections` module — Counter, defaultdict, namedtuple, deque
  5. Comprehensions — list, dict, and set in one line
  6. Generators — lazy sequences with `yield`
  7. `*args` / `**kwargs` — flexible function parameters
  8. `lambda` + `map` / `filter` — anonymous functions & functional tools
  9. A real-world mini task that combines everything

Sample data lives in this folder:
  • notes.txt     — a plain text file (Section 1)
  • settings.json — a JSON config file (Section 2)
  • log.json      — a JSON event log (Section 9 mini task)

Docs: https://docs.python.org/3/library/
"""

import json
from collections import Counter, defaultdict, deque, namedtuple
from datetime import date, datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Path handling
# ---------------------------------------------------------------------------
# Resolve every file path relative to THIS script's folder, so the tutorial
# works no matter where you run it from.

BASE_DIR = Path(__file__).resolve().parent


def data_path(filename):
    """Return a Path to a file inside this script's folder."""
    return BASE_DIR / filename


# ---------------------------------------------------------------------------
# SECTION 1: Working with text files using pathlib
# ---------------------------------------------------------------------------
# pathlib gives us a modern, object-oriented way to work with files and
# folders. Path('hello.txt').read_text() and .write_text() handle open/close
# for us automatically.
# Docs: https://docs.python.org/3/library/pathlib.html


def section_files():
    print("=" * 50)
    print("SECTION 1: Working with text files (pathlib)")
    print("=" * 50)

    path = data_path("notes.txt")

    # Read the whole file as one string.
    contents = path.read_text(encoding="utf-8")
    print("notes.txt contents:")
    print(contents)
    print()

    # Read line-by-line and count non-empty lines.
    lines = path.read_text(encoding="utf-8").splitlines()
    non_empty = [ln for ln in lines if ln.strip()]
    print(f"Total lines: {len(lines)}")
    print(f"Non-empty lines: {len(non_empty)}")
    print()

    # Write a new file (overwrites if it exists).
    out = data_path("copied_notes.txt")
    out.write_text(contents.upper(), encoding="utf-8")
    print(f"Wrote uppercased copy to {out.name}")

    # Check a path exists and get info.
    print("Does notes.txt exist?", path.exists())
    print("notes.txt size:", path.stat().st_size, "bytes")
    print()


# ---------------------------------------------------------------------------
# SECTION 2: The json module
# ---------------------------------------------------------------------------
# JSON is THE lightweight data format used everywhere (APIs, config files).
# Python objects can be serialized to JSON (json.dumps) and parsed back
# (json.loads / json.load).
# Docs: https://docs.python.org/3/library/json.html


def section_json():
    print("=" * 50)
    print("SECTION 2: The json module")
    print("=" * 50)

    # Python dict -> JSON string.
    data = {
        "app_name": "Python Study App",
        "version": "1.0.0",
        "features": ["lessons", "menu", "quizzes"],
        "active": True,
        "max_users": 100,
    }
    json_str = json.dumps(data, indent=2)
    print("Python dict serialized to JSON:")
    print(json_str)
    print()

    # Load a JSON file into a Python dict.
    path = data_path("settings.json")
    with path.open("r", encoding="utf-8") as f:
        loaded = json.load(f)
    print("settings.json parsed back into a dict:")
    print("  app_name =", loaded["app_name"])
    print("  version  =", loaded["version"])
    print()

    # Convert back to a Python object from a string.
    back = json.loads(json_str)
    print("json.loads -> type:", type(back))
    print()


# ---------------------------------------------------------------------------
# SECTION 3: The datetime module
# ---------------------------------------------------------------------------
# Date and time handling. datetime, date, and timedelta let us represent,
# format, and do arithmetic on dates.
# Docs: https://docs.python.org/3/library/datetime.html


def section_datetime():
    print("=" * 50)
    print("SECTION 3: The datetime module")
    print("=" * 50)

    # Current date and time.
    now = datetime.now()
    print("Now:", now)
    print("Date only:", now.date())
    print("Time only:", now.strftime("%H:%M:%S"))
    print()

    # Build a specific date.
    birthday = date(2000, 6, 15)
    print("A specific date:", birthday)
    print()

    # Formatting with strftime (string from time).
    print("Formats:")
    print("  %Y-%m-%d :", now.strftime("%Y-%m-%d"))
    print("  %A, %B %d :", now.strftime("%A, %B %d"))
    print()

    # Date arithmetic with timedelta.
    future = now + timedelta(days=30)
    print("30 days from now:", future.strftime("%Y-%m-%d"))
    print()

    # Difference between two dates.
    delta = date(2024, 12, 31) - date(2024, 1, 1)
    print("Days from Jan 1 to Dec 31 2024:", delta.days)
    print()


# ---------------------------------------------------------------------------
# SECTION 4: The collections module
# ---------------------------------------------------------------------------
# Specialized container data types that extend lists/dicts/tuples.
#   Counter      — count occurrences of items
#   defaultdict  — dict that supplies a default value for missing keys
#   namedtuple   — tuple with named fields
#   deque        — fast appends/pops from both ends
# Docs: https://docs.python.org/3/library/collections.html


def section_collections():
    print("=" * 50)
    print("SECTION 4: The collections module")
    print("=" * 50)

    # Counter counts hashable items.
    words = ["apple", "banana", "apple", "cherry", "apple", "banana"]
    counter = Counter(words)
    print("Counter:", counter)
    print("Most common:", counter.most_common(2))
    print()

    # defaultdict provides a default for missing keys (no KeyError).
    counts = defaultdict(int)
    for word in words:
        counts[word] += 1
    print("defaultdict count for 'apple':", counts["apple"])
    # Accessing a missing key returns the default without error.
    print("Missing key 'grape' defaults to:", counts["grape"])
    print()

    # namedtuple gives fields a name.
    Point = namedtuple("Point", ["x", "y"])
    p = Point(3, 4)
    print("namedtuple:", p)
    print("  p.x =", p.x, "| p.y =", p.y)
    print()

    # deque is efficient for appending/popping at either end.
    dq = deque([1, 2, 3])
    dq.appendleft(0)
    dq.append(4)
    print("deque after appendleft/append:", list(dq))
    print("Popped right:", dq.pop(), "| popped left:", dq.popleft())
    print()


# ---------------------------------------------------------------------------
# SECTION 5: Comprehensions
# ---------------------------------------------------------------------------
# Build lists, dicts, and sets in a single expressive line. They are more
# readable AND faster than manual for-loops.
# Docs: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions


def section_comprehensions():
    print("=" * 50)
    print("SECTION 5: Comprehensions")
    print("=" * 50)

    # List comprehension: squares of 0..9.
    squares = [x * x for x in range(10)]
    print("Squares:", squares)
    print()

    # List comprehension with a condition: even squares.
    evens = [x * x for x in range(10) if x % 2 == 0]
    print("Even squares:", evens)
    print()

    # Dict comprehension: character -> count for a word.
    word = "banana"
    letter_counts = {ch: word.count(ch) for ch in set(word)}
    print("Dict comprehension (letter counts):", letter_counts)
    print()

    # Set comprehension: unique lengths of the words.
    lengths = {len(w) for w in ["cat", "dog", "elephant", "mouse"]}
    print("Set comprehension (unique lengths):", lengths)
    print()


# ---------------------------------------------------------------------------
# SECTION 6: Generators
# ---------------------------------------------------------------------------
# A generator yields values ONE AT A TIME instead of building a whole list in
# memory. Great for big/infinite sequences — lazy evaluation.
# Docs: https://docs.python.org/3/howto/functional.html#generators


def section_generators():
    print("=" * 50)
    print("SECTION 6: Generators")
    print("=" * 50)

    # A generator function uses yield, not return.
    def count_up_to(n):
        i = 1
        while i <= n:
            yield i
            i += 1

    gen = count_up_to(5)
    print("Generator object:", gen)
    print("Values (lazy):", list(gen))
    print()

    # Generator expression (like a list comprehension but lazy).
    squares_gen = (x * x for x in range(5))
    print("Generator expression sum:", sum(squares_gen))
    print()

    # Memory advantage: a generator doesn't build the whole sequence.
    big = (x for x in range(1_000_000))  # noqa: RUF005
    print("Summing big generator (1,000,000 numbers):", sum(big))
    print()


# ---------------------------------------------------------------------------
# SECTION 7: *args and **kwargs
# ---------------------------------------------------------------------------
# *args collects extra positional arguments into a tuple. **kwargs collects
# extra keyword arguments into a dict. This makes functions flexible.
# Docs: https://docs.python.org/3/tutorial/controlflow.html#arbitrary-argument-lists


def section_args_kwargs():
    print("=" * 50)
    print("SECTION 7: *args and **kwargs")
    print("=" * 50)

    # *args: any number of positional arguments.
    def total(*args):
        return sum(args)

    print("total(1,2,3):", total(1, 2, 3))
    print("total(10, 20):", total(10, 20))
    print("total():", total())
    print()

    # **kwargs: any number of named arguments.
    def greet(**kwargs):
        parts = [f"{k}={v}" for k, v in kwargs.items()]
        return ", ".join(parts)

    print("greet(name='Ada', role='Engineer'):")
    print("  ", greet(name="Ada", role="Engineer"))
    print()

    # Mix them and unpacking.
    def mixed(required, *args, default=10, **kwargs):
        print("required:", required)
        print("args:", args)
        print("default:", default)
        print("kwargs:", kwargs)

    mixed("A", 1, 2, default=99, extra="hi")
    print()


# ---------------------------------------------------------------------------
# SECTION 8: lambda + map / filter
# ---------------------------------------------------------------------------
# A lambda is a tiny anonymous function. map() applies a function to every
# element; filter() keeps elements for which a condition is True.
# Docs: https://docs.python.org/3/howto/functional.html#built-in-functions
# Docs: https://docs.python.org/3/library/functions.html#map
# Docs: https://docs.python.org/3/library/functions.html#filter


def section_lambda():
    print("=" * 50)
    print("SECTION 8: lambda + map / filter")
    print("=" * 50)

    # A lambda is a one-line function.
    square = lambda x: x * x  # noqa: E731
    print("square(5) via lambda:", square(5))
    print()

    # map applies a function to a whole sequence.
    numbers = [1, 2, 3, 4]
    doubled = list(map(lambda x: x * 2, numbers))  # noqa: C417
    print("map double:", doubled)
    print()

    # filter keeps items where the predicate is True.
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print("filter evens:", evens)
    print()

    # Combine map + filter: square the even numbers.
    result = list(map(lambda x: x * x, filter(lambda x: x % 2 == 0, numbers)))  # noqa: C417
    print("Square of evens:", result)
    print()


# ---------------------------------------------------------------------------
# SECTION 9: A real-world mini task (all concepts combined)
# ---------------------------------------------------------------------------
# Task: read log.json, count each user's events with Counter, and write a
# per-user summary to a new JSON file using json + pathlib.


def section_summary_task():
    print("=" * 50)
    print("SECTION 9: Mini task — summarize an event log")
    print("=" * 50)

    path = data_path("log.json")
    with path.open("r", encoding="utf-8") as f:
        log = json.load(f)

    events = log["events"]
    print(f"Loaded {len(events)} events from log.json")

    # Use a Counter to total events per user.
    user_counts = Counter(event["user"] for event in events)
    print("Events per user:")
    for user, count in user_counts.most_common():
        print(f"  {user}: {count}")

    # Build a dict of actions per user using defaultdict.
    actions = defaultdict(list)
    for event in events:
        actions[event["user"]].append(event["action"])

    # Prepare a summary and write it to JSON (pathlib + json combined).
    summary = {
        "total_events": len(events),
        "unique_users": len(user_counts),
        "per_user_events": dict(user_counts),
    }
    out = data_path("log_summary.json")
    with out.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"\nWrote summary to {out.name}")
    print()


# ---------------------------------------------------------------------------
# OPTION 0: Clean up the generated files
# ---------------------------------------------------------------------------
# The lesson writes a few output files. This helper removes them so you can
# start fresh.


CLEANUP_FILES = [
    data_path("copied_notes.txt"),
    data_path("log_summary.json"),
]


def section_cleanup():
    print("=" * 50)
    print("OPTION 0: Cleaning up the generated files")
    print("=" * 50)

    removed = []
    for path in CLEANUP_FILES:
        if path.exists():
            path.unlink()
            removed.append(path.name)

    if removed:
        print("Removed:")
        for name in removed:
            print(f"  - {name}")
    else:
        print("Nothing to remove — none of the files were found.")

    print()
    print("The files will be recreated automatically the next time you run")
    print("the section that needs them.")
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
    "1": ("Text files with pathlib", section_files),
    "2": ("The json module", section_json),
    "3": ("The datetime module", section_datetime),
    "4": ("The collections module", section_collections),
    "5": ("Comprehensions", section_comprehensions),
    "6": ("Generators", section_generators),
    "7": ("*args and **kwargs", section_args_kwargs),
    "8": ("lambda + map / filter", section_lambda),
    "9": ("Mini task: summarize an event log", section_summary_task),
}


def main():
    print("\n🔧 Welcome to the Intermediate Built-ins Tutorial!\n")
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
