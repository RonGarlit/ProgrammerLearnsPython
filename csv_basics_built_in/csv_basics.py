"""
CSV Basics with Python's Built-in `csv` Module — A Self-Guided Lesson
=====================================================================
Run this file (with `python csv_basics.py`) and follow along.

CSV stands for **Comma-Separated Values**. It's a plain-text format that
stores tabular (spreadsheet-like) data. One line = one row, and commas
separate the columns (fields) in each row.

Python ships with a built-in `csv` module — no installation required —
that handles all the messy details for us: splitting by commas, quoting
fields that contain commas or newlines, and converting rows to nice
data structures.

Every section includes a reference link to the official Python docs
(https://docs.python.org/3/library/csv.html) for further reading.

The example data used here is `employees.csv` (created in Section 2).
"""

# We need the `csv` module (built into Python). If this import failed,
# your Python install is unusual — normally it works out of the box.
import csv
from pathlib import Path

# ---------------------------------------------------------------------------
# Path handling with pathlib
# ---------------------------------------------------------------------------
# pathlib is the modern, object-oriented way to handle file paths (the
# intermediate built-ins lesson teaches it in depth). `Path(__file__)` is
# this script's own location; `.resolve()` makes it absolute; `.parent`
# walks up to the folder containing it. The `/` operator joins path pieces.
# Using BASE_DIR means the lesson works no matter WHERE you run it from.
# Docs: https://docs.python.org/3/library/pathlib.html

BASE_DIR = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# SECTION 1: What is a CSV file?
# ---------------------------------------------------------------------------
# A CSV file is just text. Before we use the `csv` module, let's look at
# the RAW text to understand what we're working with.
# Docs: https://docs.python.org/3/library/csv.html#module-csv


def section_csv_overview():
    print("=" * 50)
    print("SECTION 1: What is a CSV file?")
    print("=" * 50)

    # We built employees.csv in Section 2. Let's peek at its raw contents.
    try:
        with open("employees.csv") as file:
            raw_text = file.read()
    except FileNotFoundError:
        print("Run Section 2 first to create employees.csv.")
        print()
        return

    print("Raw contents of employees.csv:\n")
    print(raw_text)

    print("--- What this means ---")
    print("  • Line 1 is the *header row* — it names each column.")
    print("  • Each later line is one *record* (one employee).")
    print("  • The very first field of each row is the employee's id.")
    print()
    print("The csv module will parse this text into lists or dicts for us.")
    print()


# ---------------------------------------------------------------------------
# SECTION 2: Reading a CSV file with csv.DictReader
# ---------------------------------------------------------------------------
# csv.DictReader reads each row as a *dictionary*, using the header row
# as the keys. This is the friendliest way to work with CSV data because
# you access columns by NAME instead of by position.
# Docs: https://docs.python.org/3/library/csv.html#csv.DictReader


def read_csv_builtin(filename):
    """Read a CSV file and return a list of dictionaries (one per row)."""
    data = []
    with open(filename, newline="") as file:
        reader = csv.DictReader(file)  # first row becomes the column names
        for row in reader:
            data.append(row)  # each `row` is an OrderedDict
    return data


def section_reading():
    print("=" * 50)
    print("SECTION 2: Reading a CSV file with DictReader")
    print("=" * 50)

    # Create a small sample file so the lesson always has data to work with.
    write_sample_csv()

    employees = read_csv_builtin("employees.csv")
    print(f"Read {len(employees)} employees.\n")

    # Loop through our list of dicts and access fields by name.
    print("Employees and their roles:")
    for emp in employees:
        print(f"  - {emp['name']} ({emp['role']}) earns ${emp['salary']}")

    # A dictionary is a collection of key/value pairs. Ask for a specific one:
    print()
    print("To pick ONE field from one row, we use its column name:")
    print("  employees[0]['name'] ->", employees[0]["name"])
    print()

    # So what does one raw row actually look like under the hood?
    print("One raw row (a dict):")
    print("  ", employees[0])
    print()


def write_sample_csv():
    """Create a small employees.csv in the current folder."""
    fieldnames = ["id", "name", "role", "salary"]
    rows = [
        ["1", "Ada Lovelace", "Engineer", "85000"],
        ["2", "Grace Hopper", "Manager", "95000"],
        ["3", "Alan Turing", "Manager", "92000"],
        ["4", "Mary Jackson", "Engineer", "78000"],
    ]
    with open("employees.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(rows)


# ---------------------------------------------------------------------------
# SECTION 3: Writing a CSV file with csv.DictWriter
# ---------------------------------------------------------------------------
# csv.DictWriter is the *reverse* of DictReader: it takes a list of
# dictionaries and writes them out as CSV. We MUST tell it the column
# order via fieldnames.
# Docs: https://docs.python.org/3/library/csv.html#csv.DictWriter


def write_csv_builtin(data, filename):
    """Write a list of dictionaries to a CSV file."""
    if not data:
        print(f"Nothing to write to {filename} — the list is empty.")
        return

    # Use the keys of the first dictionary as the column names.
    # (DictWriter needs to know the order of the columns.)
    fieldnames = data[0].keys()
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # writes the header row
        writer.writerows(data)  # writes all the data rows


def section_writing():
    print("=" * 50)
    print("SECTION 3: Writing a CSV file with DictWriter")
    print("=" * 50)

    employees = read_csv_builtin("employees.csv")

    # Build a brand-new record as a dictionary.
    new_employee = {
        "id": "5",
        "name": "Katherine Johnson",
        "role": "Manager",
        "salary": "98000",
    }
    employees.append(new_employee)
    write_csv_builtin(employees, "employees.csv")

    print("Added a new employee and re-wrote employees.csv.")
    print("The new contents:")
    for emp in read_csv_builtin("employees.csv"):
        print("  ", emp)
    print()


# ---------------------------------------------------------------------------
# SECTION 4: Filtering data and writing the result
# ---------------------------------------------------------------------------
# Now the fun part — combining what we learned. We READ all records,
# keep only the ones that match some condition, and WRITE them to a new
# file. This is a common, real-world pattern.
# Docs: https://docs.python.org/3/library/csv.html


def section_filter_write():
    print("=" * 50)
    print("SECTION 4: Filtering data and writing the result")
    print("=" * 50)

    employees = read_csv_builtin("employees.csv")

    # A *list comprehension* keeps only rows where role == 'Manager'.
    # It reads: "for each emp in employees, keep emp if role is Manager".
    # Docs: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    managers = [emp for emp in employees if emp["role"] == "Manager"]

    write_csv_builtin(managers, "managers.csv")

    print(f"Found {len(managers)} Managers and wrote them to managers.csv.\n")
    for emp in managers:
        print(f"  - {emp['name']}")

    print()
    print("Compare: managers.csv now contains only the Manager rows.")
    print("You can open both .csv files in VS Code to see the difference.")
    print()


# ---------------------------------------------------------------------------
# SECTION 5: Using the plain csv.reader / csv.writer (lists, not dicts)
# ---------------------------------------------------------------------------
# Not every CSV has a header row. When it doesn't, DictReader/Writer can't
# work — there's no header to name the columns. For those files we use
# csv.reader and csv.writer, which give us plain LISTS instead of dicts.
# Docs: https://docs.python.org/3/library/csv.html#csv.reader


def read_csv_rows(filename):
    """Read a CSV file, returning a list of lists (no header assumption)."""
    rows = []
    with open(filename, newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
    return rows


def section_reader_writer():
    print("=" * 50)
    print("SECTION 5: csv.reader / csv.writer (list-style)")
    print("=" * 50)

    # Create a header-less file: just numbers, no column names.
    with open("numbers.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["1", "10", "100"])
        writer.writerow(["2", "20", "200"])
        writer.writerow(["3", "30", "300"])

    rows = read_csv_rows("numbers.csv")
    print("numbers.csv read as a list of lists:")
    for row in rows:
        print("  ", row)  # each row is just a list

    # With lists, we access columns by POSITION (0, 1, 2), not name.
    print()
    print("With lists we index by position:")
    print("  rows[1][0] ->", rows[1][0])  # row index 1, column 0 → '2'
    print("  rows[2][2] ->", rows[2][2])  # row index 2, column 2 → '300'
    print()

    # Convert each text row into integers so we can do math.
    print("Converting to integers (for math):")
    for row in rows:
        numbers = [int(value) for value in row]  # '1' → 1, '10' → 10
        print(f"  sum of {numbers} = {sum(numbers)}")
    print()


# ---------------------------------------------------------------------------
# SECTION 6: Handling tricky CSV data (quotes, commas, newlines)
# ---------------------------------------------------------------------------
# What if a field itself contains a comma or a newline? The csv module
# handles this automatically using *quoting*. Let's prove it.
# Docs: https://docs.python.org/3/library/csv.html#csv.QUOTE_MINIMAL


def section_quoting():
    print("=" * 50)
    print("SECTION 6: Quoting (data that contains commas)")
    print("=" * 50)

    # This note contains a comma — normally that would break a CSV.
    tricky = [
        ["id", "note"],
        ["1", "Hello, world!"],
        ["2", "line one\nline two"],
    ]

    with open("tricky.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(tricky)

    print("The RAW text of tricky.csv (notice the extra quotes and newline):")
    with open("tricky.csv") as file:
        print(file.read())

    # And reading it back gives us the original values, commas and all.
    with open("tricky.csv", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            print("  ", row)

    print()
    print("The csv module added quotes around 'Hello, world!' so the comma")
    print("is not mistaken for a column separator. It also preserved the")
    print("embedded newline inside the quoted field.")
    print()


# ---------------------------------------------------------------------------
# SECTION 7: A real-world mini task (all concepts combined)
# ---------------------------------------------------------------------------
# Let's do a small, practical task: compute the average salary of all
# employees. This pulls together reading, converting, and filtering.
# Note that csv gives us STRINGS — we convert 'salary' to an int to do math.


def section_summary_task():
    print("=" * 50)
    print("SECTION 7: Mini task — average salary")
    print("=" * 50)

    employees = read_csv_builtin("employees.csv")

    # Map each employee to their salary as an integer, then average it.
    salaries = [int(emp["salary"]) for emp in employees]
    average = sum(salaries) / len(salaries)

    print(f"There are {len(employees)} employees.")
    print(f"Salaries: {salaries}")
    print(f"Average salary: ${average:,.0f}")

    # Compare against each employee to find who is above average.
    print("\nEmployees earning above average:")
    for emp in employees:
        if int(emp["salary"]) > average:
            print(f"  - {emp['name']} (${emp['salary']})")
    print()


# ---------------------------------------------------------------------------
# OPTION 0: Clean up the generated CSV files
# ---------------------------------------------------------------------------
# Every section writes (or overwrites) a CSV file in this script's folder.
# This helper deletes them all so you can start fresh. We only delete a
# file if it exists, so it's safe to run any time.
# Docs: https://docs.python.org/3/library/pathlib.html#pathlib.Path.unlink


CLEANUP_FILES = ["employees.csv", "managers.csv", "numbers.csv", "tricky.csv"]


def section_cleanup():
    print("=" * 50)
    print("OPTION 0: Cleaning up the CSV files")
    print("=" * 50)

    removed = []
    for filename in CLEANUP_FILES:
        path = BASE_DIR / filename  # build the full path with pathlib's /
        if path.exists():
            path.unlink()  # pathlib's "delete this file"
            removed.append(filename)

    if removed:
        print("Removed:")
        for filename in removed:
            print(f"  - {filename}")
    else:
        print("Nothing to remove — none of the CSV files were found.")

    print()
    print("The files will be recreated automatically the next time you run")
    print("the section that needs them.")
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
    "0": ("Clean up the generated CSV files", section_cleanup),
    "1": ("What is a CSV file?", section_csv_overview),
    "2": ("Reading with DictReader", section_reading),
    "3": ("Writing with DictWriter", section_writing),
    "4": ("Filtering & writing results", section_filter_write),
    "5": ("csv.reader / csv.writer (lists)", section_reader_writer),
    "6": ("Quoting tricky data", section_quoting),
    "7": ("Mini task: average salary", section_summary_task),
}


def main():
    print("\n📄 Welcome to the CSV Basics Tutorial!\n")
    print("You'll explore these concepts, one step at a time:\n")
    # Print the menu straight from the SECTIONS dict — no duplication.
    for number, (title, _section_function) in SECTIONS.items():
        print(f"  {number}. {title}")
    print()

    keep_going = True
    while keep_going:
        choice = input("Type a number (0-7) to run a section, or q to quit: ").strip()

        if choice.lower() == "q":
            print("Thanks for learning with us. Goodbye!")
            keep_going = False
        elif choice in SECTIONS:
            # dict lookup: we've already checked membership with `in`,
            # so indexing SECTIONS[choice] is safe here.
            _title, section_function = SECTIONS[choice]
            section_function()  # call the function stored in the dict!
        else:
            print("Hmm, that isn't a valid option. Try a number 0-7 or 'q'.")


if __name__ == "__main__":
    main()
