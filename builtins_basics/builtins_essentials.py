"""
Python Essentials — A Self-Guided Lesson
========================================
Run this file (with `python builtins_essentials.py`) and follow along.
Each section teaches ONE core concept with a real example.

Every section includes a reference link to the official Python docs
(https://docs.python.org/3/) for further reading.
"""

# ---------------------------------------------------------------------------
# SECTION 0: Welcome & Comments
# ---------------------------------------------------------------------------
# Comments are notes for HUMANS, not the computer.
# Anything after a `#` symbol is ignored by Python when it runs.

# You can also write multi-line comments using triple quotes,
# which is exactly what this big text block at the top is.


# ---------------------------------------------------------------------------
# SECTION 1: Variables & Basic Data Types
# ---------------------------------------------------------------------------
# A *variable* is a named box that stores a value.
# Python figures out the *type* of the value automatically (dynamic typing).
# Docs: https://docs.python.org/3/library/stdtypes.html


def section_variables():
    print("\n" + "=" * 50)
    print("SECTION 1: Variables & Data Types")
    print("=" * 50)

    # Integer (whole number)
    player_score = 10
    print("player_score is set to:", player_score)

    # Float (decimal number)
    average_grade = 85.5
    print("average_grade is set to:", average_grade)

    # String (text) — note the quotes around it
    player_name = "Peter Python"
    print("player_name is set to:", player_name)

    # Boolean (True or False)
    is_playing = True
    print("is_playing is set to:", is_playing)

    print()

    # Print each variable (type() tells us the data type)
    print(player_name, "has score", player_score)
    print("The type of player_score is:", type(player_score))
    print("The type of average_grade is:", type(average_grade))
    print("The type of player_name is:", type(player_name))
    print("The type of is_playing is:", type(is_playing))
    print()

    # f-strings let us embed variables directly inside text
    # Docs: https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals
    greeting = f"Hello, {player_name}! Your grade is {average_grade}."
    print(greeting)
    print()


# ---------------------------------------------------------------------------
# HELPER: ask_int — safely read an integer from the user
# ---------------------------------------------------------------------------
# input() always returns a STRING, and int("abc") crashes with a ValueError.
# This helper combines two ideas you'll see later in this lesson:
#   • a `while True` loop (Section 4) that repeats until we get good input
#   • try/except (Section 7) to catch the crash and re-ask instead
# Docs: https://docs.python.org/3/tutorial/errors.html
# Docs:  https://docs.python.org/3/reference/compound_stmts.html#while


def ask_int(prompt):
    """
    Keep asking the user with `prompt` until they type a valid integer,
    then return that integer.
    """
    while True:  # loop forever until `return` hands back a value
        try:
            # Try to convert the typed text into an integer.
            return int(input(prompt))
        except ValueError:
            # int() raised ValueError → the text wasn't a number.
            # Print a friendly message and the loop asks again.
            print("✖ That wasn't a whole number — please try again.")


# ---------------------------------------------------------------------------
# SECTION 2: Getting Input & Type Conversion
# ---------------------------------------------------------------------------
# input() reads text typed by the user. It ALWAYS returns a string,
# so we convert it with int() or float() when we need numbers.
# Docs: https://docs.python.org/3/library/functions.html#input


def section_input():
    print("=" * 50)
    print("SECTION 2: Reading Input & Converting Types")
    print("=" * 50)

    # Get a number from the user. input() ALWAYS returns a string, so we
    # use ask_int() below — it keeps asking until the user types a valid
    # integer, instead of crashing with a traceback on "abc".
    # (We'll learn WHY this works in Section 7: Error Handling.)
    age = ask_int("Enter your age: ")

    # Do arithmetic and print it
    age_in_months = age * 12
    print(f"You are approximately {age_in_months} months old.")
    print()


# ---------------------------------------------------------------------------
# SECTION 3: Conditionals (if / elif / else)
# ---------------------------------------------------------------------------
# Conditionals let the program make DECISIONS based on comparisons.
# Docs: https://docs.python.org/3/tutorial/controlflow.html#More-control-flow-tools


def section_conditionals():
    print("=" * 50)
    print("SECTION 3: Conditionals")
    print("=" * 50)

    score = ask_int("Enter your quiz score (0-100): ")

    # Python evaluates conditions top to bottom,
    # stopping at the FIRST condition that is True.
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"

    print(f"Score {score} earns grade {grade}.")
    print()


# ---------------------------------------------------------------------------
# SECTION 4: Loops (for and while)
# ---------------------------------------------------------------------------
# Loops repeat work. `for` loops iterate over collections;
# `while` loops repeat while a condition stays True.
# Docs: https://docs.python.org/3/tutorial/controlflow.html#for
#       https://docs.python.org/3/tutorial/controlflow.html#the-while-statement


def section_loops():
    print("=" * 50)
    print("SECTION 4: Loops")
    print("=" * 50)

    print("Counting 1 to 5 with a FOR loop:")
    for number in range(1, 6):  # range(1,6) → 1,2,3,4,5
        print(f"  {number}")

    print("\nCounting down with a WHILE loop:")
    countdown = 3
    while countdown > 0:
        print(f"  {countdown}...")
        countdown -= 1  # shorthand for countdown = countdown - 1
    print("  Liftoff!")

    # --- enumerate(): loop with an automatic counter -----------------------
    # Beginners often write `i = 0` ... `i += 1` to number items. Python's
    # enumerate() hands you the position AND the item together.
    # Docs: https://docs.python.org/3/library/functions.html#enumerate
    print("\nNumbering a list with ENUMERATE:")
    fruits = ["apple", "banana", "cherry"]
    for position, fruit in enumerate(fruits, start=1):  # start=1 → count from 1
        print(f"  {position}. {fruit}")

    # --- zip(): loop over TWO lists at the same time -----------------------
    # zip() pairs items up: ("apple", 1), ("banana", 2), ("cherry", 3).
    # Docs: https://docs.python.org/3/library/functions.html#zip
    print("\nPairing two lists with ZIP:")
    prices = [1.20, 0.50, 3.00]
    for fruit, price in zip(fruits, prices):
        print(f"  {fruit} costs ${price:.2f}")
    print()


# ---------------------------------------------------------------------------
# SECTION 5: Lists & Dictionaries
# ---------------------------------------------------------------------------
# A *list* is an ordered sequence of items.
# A *dictionary* maps keys (labels) to values.
# Docs: https://docs.python.org/3/tutorial/datastructures.html


def section_collections():
    print("=" * 50)
    print("SECTION 5: Lists & Dictionaries")
    print("=" * 50)

    # --- List of favorite colors ---
    colors = ["blue", "green", "purple"]
    colors.append("orange")  # add an item to the end
    print("Current colors:", colors)
    print("The first color is:", colors[0])  # lists are 0-indexed!
    print("We have", len(colors), "colors.")  # len() counts items

    print()

    # --- Dictionary to describe one person ---
    person = {"name": "Ada", "age": 36, "city": "London"}
    print("Person:", person)
    print("Their name is:", person["name"])

    # Loop through a dictionary (get the key *and* value)
    for key, value in person.items():
        print(f"  {key} = {value}")

    print()

    # --- List comprehension: build a new list from an existing one ---
    # A *list comprehension* is a compact way to create a list in one line.
    # It reads like: "for each number in numbers, keep number * 2".
    # Docs: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    numbers = [1, 2, 3, 4, 5]
    doubled = [number * 2 for number in numbers]  # → [2, 4, 6, 8, 10]
    print("Original numbers:", numbers)
    print("Doubled (list comprehension):", doubled)

    # You can also add a condition (an `if`) to filter items.
    # Keep only the even numbers, then square them.
    evens_squared = [n * n for n in numbers if n % 2 == 0]  # → [4, 16]
    print("Even numbers squared:", evens_squared)
    print()


# ---------------------------------------------------------------------------
# SECTION 6: Functions
# ---------------------------------------------------------------------------
# Functions package a block of reusable code with a name.
# Docs: https://docs.python.org/3/tutorial/controlflow.html#defining-functions


def greet(name, greeting="Hello"):
    """
    Return a friendly message. This triple-quoted text is a *docstring*,
    which describes what the function does.
    """
    return f"{greeting}, {name}!"


def section_functions():
    print("=" * 50)
    print("SECTION 6: Functions")
    print("=" * 50)

    # Call the function above
    message = greet("Sam")  # greeting uses the default
    print(message)
    print(greet("Sam", "Welcome back"))  # custom greeting provided

    # Output a simple written result
    result = add(5, 3)
    print("5 + 3 =", result)
    print()


def add(a, b):
    """Return the sum of a and b."""
    return a + b


# ---------------------------------------------------------------------------
# SECTION 7: Error Handling (try / except)
# ---------------------------------------------------------------------------
# Programs crash when they hit an error. try/except lets you handle
# errors gracefully instead of crashing.
# Docs: https://docs.python.org/3/tutorial/errors.html


def section_errors():
    print("=" * 50)
    print("SECTION 7: Error Handling")
    print("=" * 50)

    try:
        # If the user types something that is not a number, int() raises a ValueError
        number = ask_int("Enter a number to divide 10 by: ")
        print(f"10  / {number} = {10 / number}")

    except ValueError:
        print("✖ That wasn't a number. Please type digits only.")

    except ZeroDivisionError:
        print("✖ You cannot divide by zero!")

    except Exception as overall_error:
        # A safety net that catches any other unexpected error
        print(f"Something went wrong: {overall_error}")
    print()


# ---------------------------------------------------------------------------
# SECTION 8: Sets & Tuples
# ---------------------------------------------------------------------------
# A *set* is an unordered collection of UNIQUE items (no duplicates).
# A *tuple* is an ordered, IMMUTABLE sequence (cannot be changed after creation).
# Docs: https://docs.python.org/3/tutorial/datastructures.html#sets
#       https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences


def section_sets_tuples():
    print("=" * 50)
    print("SECTION 8: Sets & Tuples")
    print("=" * 50)

    # --- Set: unique items, order is not guaranteed ---
    favorite_numbers = {3, 7, 42}  # sets automatically keep only unique items
    print("Set (unique items):", favorite_numbers)

    # Add an item and check membership
    favorite_numbers.add(99)
    print("After adding 99:", favorite_numbers)
    print("Is 7 in the set?", 7 in favorite_numbers)

    # Set operations: union (|) and intersection (&)
    set_a = {1, 2, 3}
    set_b = {3, 4, 5}
    print("set_a | set_b (union):", set_a | set_b)  # everything in either
    print("set_a & set_b (intersection):", set_a & set_b)  # only what's in both

    print()

    # --- Tuple: ordered and immutable ---
    # A tuple is like a list, but you CANNOT change it after creation.
    # Use it for data that should never change, like coordinates.
    point = (3, 4)  # an (x, y) coordinate
    print("Tuple point:", point)
    print("x coordinate:", point[0])  # tuples are also 0-indexed
    print("y coordinate:", point[1])

    # Unpacking: assign each element to a variable in one line
    x, y = point
    print(f"Unpacked: x = {x}, y = {y}")

    # Tuples are immutable — this would raise an error:
    # point[0] = 10  # ❌ TypeError: 'tuple' object does not support item assignment
    print()


# ---------------------------------------------------------------------------
# SECTION 9: String Methods & Slicing
# ---------------------------------------------------------------------------
# Strings come with built-in "methods" — functions attached to the string
# itself, called with a dot: text.upper(). These are used constantly in
# real programs (cleaning user input, parsing files, building messages).
# Docs: https://docs.python.org/3/library/stdtypes.html#string-methods


def section_strings():
    print("=" * 50)
    print("SECTION 9: String Methods & Slicing")
    print("=" * 50)

    messy = "  Hello, Python World!  "

    # .strip() removes whitespace (spaces, tabs) from BOTH ends.
    # Essential for cleaning up user input before using it.
    clean = messy.strip()
    print("Before strip:", repr(messy))  # repr() shows the hidden spaces
    print("After  strip:", repr(clean))

    # .upper() / .lower() change the case — handy for comparing text
    # so "YES", "yes", and "Yes" all match.
    print("upper():", clean.upper())
    print("lower():", clean.lower())

    # .replace(old, new) swaps every occurrence of a piece of text.
    print("replace():", clean.replace("Python", "🐍 Python"))

    # .split() cuts a string into a LIST of pieces. By default it splits
    # on whitespace; you can pass your own separator.
    words = clean.split()  # → ['Hello,', 'Python', 'World!']
    print("split():", words)

    # .join() is the opposite of split(): glue a list of strings back
    # together with a separator in between.
    print("join():", "-".join(words))

    # .startswith() / .endswith() answer yes/no questions about text.
    print("startswith('Hello')?", clean.startswith("Hello"))
    print("endswith('World!')?", clean.endswith("World!"))

    print()

    # --- Slicing: grab a PIECE of a sequence with [start:stop:step] -------
    # Works on strings, lists, and tuples. The stop index is NOT included!
    # Docs: https://docs.python.org/3/tutorial/introduction.html#strings
    text = "Python"
    print("text      =", text)
    print("text[0]   =", text[0], "   # first character (index 0)")
    print("text[-1]  =", text[-1], "   # last character (negative = from end)")
    print("text[0:3] =", text[0:3], "  # characters 0,1,2 (3 not included)")
    print("text[:3]  =", text[:3], "  # start defaults to the beginning")
    print("text[3:]  =", text[3:], "  # end defaults to the end")
    print("text[::-1]= ", text[::-1], "  # step -1 walks backwards → reversed!")
    print()


# ---------------------------------------------------------------------------
# MAIN MENU — brings all sections together
# ---------------------------------------------------------------------------
# The `if __name__ == "__main__":` guard ensures this code only runs
# when the script is executed directly, not when imported as a module.
# Docs: https://docs.python.org/3/library/__main__.html

# A DICT as a "dispatch table": each menu number maps to a (title, function)
# pair. This replaces a long if/elif chain — to add a section you just add
# one line here, and the menu printing + lookup below handle the rest.
# Docs: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
SECTIONS = {
    "1": ("Variables & Data Types", section_variables),
    "2": ("Input & Type Conversion", section_input),
    "3": ("Conditionals", section_conditionals),
    "4": ("Loops", section_loops),
    "5": ("Lists & Dictionaries", section_collections),
    "6": ("Functions", section_functions),
    "7": ("Error Handling", section_errors),
    "8": ("Sets & Tuples", section_sets_tuples),
    "9": ("String Methods & Slicing", section_strings),
}


def main():
    print("\n🐍 Welcome to the Python Beginner Tutorial!\n")
    print("You will explore these concepts, one step at a time:\n")
    # Print the menu straight from the SECTIONS dict — no duplication.
    for number, (title, _section_function) in SECTIONS.items():
        print(f"  {number}. {title}")
    print()

    keep_going = True
    while keep_going:
        choice = input("Type a number (1-9) to run a section, or q to quit: ").strip()

        if choice.lower() == "q":
            print("Thanks for learning with us. Goodbye!")
            keep_going = False
        elif choice in SECTIONS:
            # dict lookup: .get() would return None for a bad key, but we've
            # already checked membership with `in`, so this is safe.
            _title, section_function = SECTIONS[choice]
            section_function()  # call the function stored in the dict!
        else:
            print("Hmm, that isn't a valid option. Try a number 1-9 or 'q'.")


if __name__ == "__main__":
    main()
