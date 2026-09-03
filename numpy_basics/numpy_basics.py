"""
NumPy Basics with Python — A Self-Guided Lesson
===============================================
Run this file (with `python numpy_basics.py`) and follow along.

NumPy (Numerical Python) is the foundational library for **fast numerical
computing** in Python. It gives us the **ndarray** — a grid of numbers that
supports lightning-fast, element-wise math — plus a huge toolbox of
functions for statistics, linear algebra, and more.

pandas is built ON TOP of NumPy: a DataFrame's columns are NumPy arrays
under the hood. So learning NumPy first makes you a much stronger pandas
user. This lesson is the *basics only*. We will cover intermediate and
advanced NumPy in later folders. Here we focus on:

  1. What NumPy is & how to install it
  2. Creating arrays (from lists, and with np.arange / np.zeros / np.ones)
  3. Exploring an array (shape, size, dtype, ndim)
  4. Indexing & slicing arrays
  5. Vectorized math (element-wise operations — the big speed win)
  6. Universal functions (ufuncs) — np.sqrt, np.round, np.abs, ...
  7. Aggregations (sum, mean, min, max, std)
  8. Saving & loading arrays to/from a file
  9. A real-world mini task that combines everything

The example data is `measurements.csv` — 15 sensor readings from three
sensors (1, 2, 3) over five days.

Docs: https://numpy.org/doc/stable/
"""

# NumPy is NOT built into Python — it must be installed first.
#   pip install numpy
# If this import fails, see the README.md "Prerequisites" section.
from pathlib import Path

import numpy as np

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


def data_path(filename):
    """Return the full path to a file inside this script's folder."""
    return BASE_DIR / filename


# The sample data file used throughout this lesson.
MEASUREMENTS_FILE = data_path("measurements.csv")

# Output files created by the I/O section (and removed by option 0).
TEXT_OUTPUT_FILE = data_path("saved_array.txt")
BINARY_OUTPUT_FILE = data_path("saved_array.npy")


# ---------------------------------------------------------------------------
# SECTION 1: What is NumPy & how to install it
# ---------------------------------------------------------------------------
# NumPy is a third-party library, so it must be installed. It is the
# de-facto standard for numerical computing in Python. The core object is
# the **ndarray** — a fast, homogeneous grid of numbers.
# Docs: https://numpy.org/doc/stable/user/absolute_beginners.html


def section_intro():
    print("=" * 50)
    print("SECTION 1: What is NumPy?")
    print("=" * 50)

    print("NumPy is a Python library for fast numerical computing.")
    print("Its core object is the ndarray (n-dimensional array):\n")
    print("  • 1D array  — like a list of numbers (a vector).")
    print("  • 2D array  — like a table of numbers (a matrix).")
    print("  • 3D+ array — higher-dimensional grids.")
    print()
    print("To install it, run in your terminal:")
    print("  pip install numpy")
    print()
    print("Let's confirm it's installed and see the version:")
    print("  numpy version:", np.__version__)
    print()
    print("Why is NumPy fast? Two reasons:")
    print("  • Homogeneous data — every element is the same type, so it")
    print("    sits in one contiguous block of memory.")
    print("  • Vectorization — operations run across the whole array at")
    print("    once (in C), not element-by-element in a Python loop.")
    print()


# ---------------------------------------------------------------------------
# SECTION 2: Creating arrays
# ---------------------------------------------------------------------------
# The most common ways to make an ndarray:
#   np.array([...])  -> from a Python list
#   np.arange(n)     -> like range(), but returns an array
#   np.zeros(n)      -> an array of zeros
#   np.ones(n)       -> an array of ones
#   np.linspace(a,b,n) -> n evenly spaced numbers from a to b
# Docs: https://numpy.org/doc/stable/reference/routines.array-creation.html


def section_creating():
    print("=" * 50)
    print("SECTION 2: Creating arrays")
    print("=" * 50)

    # From a Python list.
    a = np.array([10, 20, 30, 40])
    print("np.array([10, 20, 30, 40]):")
    print(" ", a)
    print()

    # A 2D array from a list of lists.
    m = np.array([[1, 2, 3], [4, 5, 6]])
    print("np.array([[1,2,3],[4,5,6]]) — a 2D array:")
    print(m)
    print()

    # np.arange is like range() but returns an array.
    r = np.arange(0, 10, 2)  # start, stop (exclusive), step
    print("np.arange(0, 10, 2):", r)
    print()

    # np.zeros / np.ones — handy for initializing.
    z = np.zeros(4)
    o = np.ones((2, 3))  # a 2x3 grid of ones
    print("np.zeros(4):", z)
    print("np.ones((2, 3)):")
    print(o)
    print()

    # np.linspace — evenly spaced numbers between two endpoints.
    ls = np.linspace(0, 1, 5)  # 5 numbers from 0 to 1 inclusive
    print("np.linspace(0, 1, 5):", ls)
    print()


# ---------------------------------------------------------------------------
# SECTION 3: Exploring an array
# ---------------------------------------------------------------------------
# Before analyzing data, we inspect the array's structure:
#   arr.shape  -> (rows, columns) as a tuple
#   arr.ndim   -> number of dimensions
#   arr.size   -> total number of elements
#   arr.dtype  -> the data type of the elements
# Docs: https://numpy.org/doc/stable/reference/arrays.ndarray.html


def section_explore():
    print("=" * 50)
    print("SECTION 3: Exploring an array")
    print("=" * 50)

    a = np.array([10, 20, 30, 40])
    m = np.array([[1, 2, 3], [4, 5, 6]])

    print("1D array:", a)
    print("  shape:", a.shape, " ndim:", a.ndim, " size:", a.size, " dtype:", a.dtype)
    print()

    print("2D array:")
    print(m)
    print("  shape:", m.shape, " ndim:", m.ndim, " size:", m.size, " dtype:", m.dtype)
    print()

    # dtype matters: integers vs floats behave differently.
    f = np.array([1.5, 2.5, 3.5])
    print("Float array dtype:", f.dtype)
    print()

    # We can force a dtype when creating an array.
    i = np.array([1, 2, 3], dtype=float)
    print("np.array([1,2,3], dtype=float):", i, "->", i.dtype)
    print()


# ---------------------------------------------------------------------------
# SECTION 4: Indexing & slicing arrays
# ---------------------------------------------------------------------------
# Indexing works like lists, but slicing can address multiple dimensions
# at once with a comma: arr[row, col].
# Docs: https://numpy.org/doc/stable/user/basics.indexing.html


def section_indexing():
    print("=" * 50)
    print("SECTION 4: Indexing & slicing arrays")
    print("=" * 50)

    a = np.array([10, 20, 30, 40, 50])
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    print("1D array:", a)
    print("  a[0]:", a[0], "  a[-1]:", a[-1])
    print("  a[1:4]:", a[1:4], "  a[:3]:", a[:3], "  a[::2]:", a[::2])
    print()

    print("2D array:")
    print(m)
    print("  m[0, 1]:", m[0, 1], "  (row 0, col 1)")
    print("  m[2, 2]:", m[2, 2], "  (row 2, col 2)")
    print()

    # Slice a whole row or column.
    print("  m[0, :] (row 0):", m[0, :])
    print("  m[:, 1] (col 1):", m[:, 1])
    print()

    # Slice a sub-block: rows 0-1, cols 1-2.
    print("  m[0:2, 1:3] (sub-block):")
    print(m[0:2, 1:3])
    print()

    # ⚠️ Slicing returns a VIEW, not a copy. Changing it changes the
    # original array. Use .copy() if you want an independent copy.
    view = a[0:3]
    view[0] = 999
    print("After modifying a slice, original a:", a)
    print("  💡 Slices are views — use .copy() to detach.")
    print()


# ---------------------------------------------------------------------------
# SECTION 5: Vectorized math (element-wise operations)
# ---------------------------------------------------------------------------
# This is NumPy's superpower. Instead of looping, we apply an operation to
# the WHOLE array at once. It's faster AND easier to read.
# Docs: https://numpy.org/doc/stable/user/basics.ufuncs.html


def section_vectorized():
    print("=" * 50)
    print("SECTION 5: Vectorized math")
    print("=" * 50)

    a = np.array([1, 2, 3, 4])

    print("a:", a)
    print("  a + 10:", a + 10)
    print("  a * 2:", a * 2)
    print("  a ** 2:", a**2)
    print("  a / 2:", a / 2)
    print()

    # Element-wise between two arrays of the same shape.
    b = np.array([10, 20, 30, 40])
    print("b:", b)
    print("  a + b:", a + b)
    print("  b - a:", b - a)
    print("  a * b:", a * b)
    print()

    # Comparison produces a boolean array.
    print("  a > 2:", a > 2)
    print("  b >= 30:", b >= 30)
    print()

    # Contrast with a Python loop — same result, far more code.
    result = [x * 2 for x in a]
    print("Python loop equivalent:", result)
    print("  💡 Vectorized code is shorter AND faster.")
    print()


# ---------------------------------------------------------------------------
# SECTION 6: Universal functions (ufuncs)
# ---------------------------------------------------------------------------
# NumPy ships with many element-wise functions that operate on whole
# arrays: np.sqrt, np.round, np.abs, np.exp, np.log, np.sin, ...
# Docs: https://numpy.org/doc/stable/reference/ufuncs.html


def section_ufuncs():
    print("=" * 50)
    print("SECTION 6: Universal functions (ufuncs)")
    print("=" * 50)

    a = np.array([1.0, 4.0, 9.0, 16.0])
    print("a:", a)
    print("  np.sqrt(a):", np.sqrt(a))
    print()

    b = np.array([1.234, 5.678, -9.876])
    print("b:", b)
    print("  np.round(b, 1):", np.round(b, 1))
    print("  np.abs(b):", np.abs(b))
    print()

    c = np.array([1, 2, 3])
    print("c:", c)
    print("  np.exp(c):", np.round(np.exp(c), 2))
    print("  np.log(c):", np.round(np.log(c), 2))
    print()

    # np.clip bounds values between a min and max.
    d = np.array([-5, 0, 10, 50])
    print("d:", d)
    print("  np.clip(d, 0, 20):", np.clip(d, 0, 20))
    print()


# ---------------------------------------------------------------------------
# SECTION 7: Aggregations (sum, mean, min, max, std)
# ---------------------------------------------------------------------------
# Aggregations collapse an array down to a single number (or a row/column
# summary). These are the statistics you reach for constantly.
# Docs: https://numpy.org/doc/stable/reference/routines.statistics.html


def section_aggregations():
    print("=" * 50)
    print("SECTION 7: Aggregations")
    print("=" * 50)

    a = np.array([10, 20, 30, 40, 50])
    print("a:", a)
    print("  a.sum():", a.sum())
    print("  a.mean():", a.mean())
    print("  a.min():", a.min())
    print("  a.max():", a.max())
    print("  a.std():", round(a.std(), 2))
    print()

    # Aggregations can run along an axis (dimension).
    # axis=0 -> down columns, axis=1 -> across rows.
    m = np.array([[1, 2, 3], [4, 5, 6]])
    print("2D array:")
    print(m)
    print("  m.sum(axis=0) (column sums):", m.sum(axis=0))
    print("  m.sum(axis=1) (row sums):", m.sum(axis=1))
    print("  m.mean(axis=0) (column means):", m.mean(axis=0))
    print()

    # np.argmax / np.argmin return the INDEX of the max/min value.
    print("  a.argmax():", a.argmax(), " (index of the max)")
    print("  a.argmin():", a.argmin(), " (index of the min)")
    print()


# ---------------------------------------------------------------------------
# SECTION 8: Saving & loading arrays to/from a file
# ---------------------------------------------------------------------------
# np.save / np.load store arrays in a fast binary format (.npy).
# np.savetxt / np.loadtxt use plain text (great for CSV-like data).
# Docs: https://numpy.org/doc/stable/reference/routines.io.html


def save_array(arr, filename):
    """Save a 1D array to a plain-text file (one number per line)."""
    np.savetxt(filename, arr)


def load_array(filename):
    """Load a 1D array from a plain-text file."""
    return np.loadtxt(filename)


def section_io():
    print("=" * 50)
    print("SECTION 8: Saving & loading arrays")
    print("=" * 50)

    a = np.array([1.5, 2.5, 3.5, 4.5])

    # Save to a text file, then load it back.
    save_array(a, TEXT_OUTPUT_FILE)
    loaded = load_array(TEXT_OUTPUT_FILE)
    print("Saved:", a)
    print("Loaded:", loaded)
    print("  Equal?", np.array_equal(a, loaded))
    print()

    # Binary format is faster and preserves dtype exactly.
    np.save(BINARY_OUTPUT_FILE, a)
    loaded_bin = np.load(BINARY_OUTPUT_FILE)
    print("Binary .npy loaded:", loaded_bin, "dtype:", loaded_bin.dtype)
    print()

    # np.loadtxt can read a CSV with a header and delimiter.
    data = np.loadtxt(MEASUREMENTS_FILE, delimiter=",", skiprows=1)
    print("measurements.csv loaded with np.loadtxt (skiprows=1):")
    print("  shape:", data.shape)
    print("  first 3 rows:")
    print(data[:3])
    print()


# ---------------------------------------------------------------------------
# SECTION 9: A real-world mini task (all concepts combined)
# ---------------------------------------------------------------------------
# Task: analyze sensor readings. Load the CSV, extract each sensor's
# readings, and report the mean and max per sensor. This pulls together
# loading, slicing, and aggregating — everything in this lesson.


def section_summary_task():
    print("=" * 50)
    print("SECTION 9: Mini task — sensor reading summary")
    print("=" * 50)

    # Load the CSV (skip the header row).
    data = np.loadtxt(MEASUREMENTS_FILE, delimiter=",", skiprows=1)
    print("Loaded measurements.csv:")
    print("  shape:", data.shape)
    print()

    # Columns: [sensor_id, reading, day]. Sensor ids are 1, 2, 3 (A, B, C).
    sensor_ids = data[:, 0].astype(int)
    readings = data[:, 1]

    # For each sensor, find its rows and summarize.
    for sensor in np.unique(sensor_ids):
        mask = sensor_ids == sensor
        sensor_readings = readings[mask]
        print(f"Sensor {sensor}:")
        print(f"  readings: {sensor_readings}")
        print(f"  mean: {sensor_readings.mean():.2f}")
        print(f"  max:  {sensor_readings.max():.2f}")
        print()

    # Overall stats across all sensors.
    print(f"Overall mean reading: {readings.mean():.2f}")
    print(f"Overall max reading:  {readings.max():.2f}")
    print()


# ---------------------------------------------------------------------------
# OPTION 0: Clean up the generated files
# ---------------------------------------------------------------------------
# The I/O section creates two files. This helper deletes them so you can
# start fresh. We only delete a file if it exists, so it's safe to run any
# time.


CLEANUP_FILES = [TEXT_OUTPUT_FILE, BINARY_OUTPUT_FILE]


def section_cleanup():
    print("=" * 50)
    print("OPTION 0: Cleaning up the generated files")
    print("=" * 50)

    removed = []
    for filename in CLEANUP_FILES:
        if filename.exists():  # pathlib: no os.path.exists() needed
            filename.unlink()  # pathlib's "delete this file"
            removed.append(filename.name)  # .name = just the filename part

    if removed:
        print("Removed:")
        for filename in removed:
            print(f"  - {filename}")
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
    "1": ("What is NumPy & how to install it", section_intro),
    "2": ("Creating arrays", section_creating),
    "3": ("Exploring an array", section_explore),
    "4": ("Indexing & slicing arrays", section_indexing),
    "5": ("Vectorized math", section_vectorized),
    "6": ("Universal functions (ufuncs)", section_ufuncs),
    "7": ("Aggregations (sum, mean, min, max, std)", section_aggregations),
    "8": ("Saving & loading arrays", section_io),
    "9": ("Mini task: sensor reading summary", section_summary_task),
}


def main():
    print("\n🔢 Welcome to the NumPy Basics Tutorial!\n")
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
