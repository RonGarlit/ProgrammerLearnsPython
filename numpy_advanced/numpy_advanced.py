"""
NumPy Advanced with Python — A Self-Guided Lesson
=================================================
Run this file (with `python numpy_advanced.py`) and follow along.

This is the THIRD step in NumPy. We assume you completed `numpy_basics`
(creating, indexing, vectorized math, aggregations) and `numpy_intermediate`
(reshaping, masking, fancy indexing, broadcasting, random, linear algebra).

Here we go to the advanced level. Advanced NumPy is about **performance,
structure, and real-world scale**. We focus on:

  1. Structured arrays & record arrays — mixed-type, labeled data
  2. Vectorized string operations (np.char)
  3. Advanced broadcasting & meshgrid — building coordinate grids
  4. Performance: vectorization vs loops, and np.vectorize
  5. Memory & dtype control (float32 vs float64, views vs copies)
  6. Advanced indexing with np.take / np.put / np.ix_
  7. Polynomials & curve fitting (np.polyfit)
  8. Working with missing data (np.nan) & masked arrays
  9. A real-world mini task that combines all of it

The example data is `measurements.csv` — 15 sensor readings from three
sensors (1, 2, 3) over five days.

Docs: https://numpy.org/doc/stable/
"""

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


# Sample data file used throughout this lesson.
MEASUREMENTS_FILE = data_path("measurements.csv")


# ---------------------------------------------------------------------------
# SECTION 1: Structured arrays & record arrays
# ---------------------------------------------------------------------------
# A normal ndarray holds ONE type. A structured array lets each "column"
# have its own type and a name — like a mini table. This is the low-level
# ancestor of a pandas DataFrame.
# Docs: https://numpy.org/doc/stable/user/basics.rec.html


def section_structured():
    print("=" * 50)
    print("SECTION 1: Structured arrays & record arrays")
    print("=" * 50)

    # Define a dtype with named, typed fields.
    dtype = [("name", "U10"), ("age", "i4"), ("score", "f8")]
    people = np.array(
        [("Alice", 30, 88.5), ("Bob", 25, 92.0), ("Carol", 35, 79.5)],
        dtype=dtype,
    )
    print("Structured array (name, age, score):")
    print(people)
    print()

    # Access a whole field by name.
    print("people['age']:", people["age"])
    print("people['score'].mean():", people["score"].mean())
    print()

    # Filter on a field.
    print("people[people['score'] > 80]:")
    print(people[people["score"] > 80])
    print()

    # A record array (recarray) lets you use attribute access: people.age
    rec = people.view(np.recarray)
    print("As a recarray: rec.age:", rec.age)
    print()


# ---------------------------------------------------------------------------
# SECTION 2: Vectorized string operations (np.char)
# ---------------------------------------------------------------------------
# NumPy has vectorized string functions that operate on whole arrays of
# strings at once — no Python loop needed.
# Docs: https://numpy.org/doc/stable/reference/routines.char.html


def section_strings():
    print("=" * 50)
    print("SECTION 2: Vectorized string operations (np.char)")
    print("=" * 50)

    names = np.array(["alice", "bob", "carol", "dave"])
    print("names:", names)
    print()

    # Uppercase / lowercase / capitalize.
    print("np.char.upper(names):", np.char.upper(names))
    print("np.char.capitalize(names):", np.char.capitalize(names))
    print()

    # Check for a substring.
    print("np.char.startswith(names, 'a'):", np.char.startswith(names, "a"))
    print("np.char.find(names, 'o'):", np.char.find(names, "o"))
    print()

    # Replace and strip.
    print("np.char.replace(names, 'a', '@'):", np.char.replace(names, "a", "@"))
    messy = np.array(["  hi  ", "  there "])
    print("np.char.strip(messy):", np.char.strip(messy))
    print()


# ---------------------------------------------------------------------------
# SECTION 3: Advanced broadcasting & meshgrid
# ---------------------------------------------------------------------------
# np.meshgrid builds coordinate grids from 1D arrays. Combined with
# broadcasting, it lets us evaluate a function over a whole 2D plane at
# once — the foundation of heatmaps and surface plots.
# Docs: https://numpy.org/doc/stable/reference/generated/numpy.meshgrid.html


def section_meshgrid():
    print("=" * 50)
    print("SECTION 3: Advanced broadcasting & meshgrid")
    print("=" * 50)

    x = np.array([0, 1, 2])
    y = np.array([10, 20, 30])

    # Build coordinate grids.
    X, Y = np.meshgrid(x, y)
    print("x:", x, " y:", y)
    print()
    print("X (x repeated down rows):")
    print(X)
    print()
    print("Y (y repeated across cols):")
    print(Y)
    print()

    # Evaluate a function over the whole grid at once.
    Z = X + Y
    print("Z = X + Y (every combination):")
    print(Z)
    print()

    # A classic: distance from origin over a grid.
    gx = np.linspace(-2, 2, 5)
    gy = np.linspace(-2, 2, 5)
    GX, GY = np.meshgrid(gx, gy)
    dist = np.sqrt(GX**2 + GY**2)
    print("Distance from origin over a 5x5 grid:")
    print(np.round(dist, 2))
    print()


# ---------------------------------------------------------------------------
# SECTION 4: Performance — vectorization vs loops, and np.vectorize
# ---------------------------------------------------------------------------
# Vectorized code is dramatically faster than Python loops. We measure it
# with timeit. np.vectorize wraps a Python function so it can run on an
# array, but it is NOT a true speedup — it's a convenience.
# Docs: https://numpy.org/doc/stable/reference/generated/numpy.vectorize.html


def section_performance():
    print("=" * 50)
    print("SECTION 4: Performance — vectorization vs loops")
    print("=" * 50)

    import timeit

    n = 1_000_000
    data = np.random.default_rng(0).random(n)

    # Python loop.
    def loop_sum(arr):
        total = 0.0
        for value in arr:
            total += value
        return total

    # Vectorized.
    def vec_sum(arr):
        return arr.sum()

    # Time each (best of 3 runs).
    loop_time = timeit.timeit(lambda: loop_sum(data), number=3)
    vec_time = timeit.timeit(lambda: vec_sum(data), number=3)
    print(f"Array size: {n:,}")
    print(f"  Python loop:  {loop_time:.4f}s")
    print(f"  Vectorized:   {vec_time:.4f}s")
    print(f"  Speedup:      {loop_time / vec_time:.0f}x")
    print()

    # np.vectorize wraps a Python function for array use (convenience, not speed).
    def classify(x):
        return "high" if x > 0.5 else "low"

    vec_classify = np.vectorize(classify)
    small = np.array([0.1, 0.9, 0.4, 0.8])
    print("np.vectorize(classify) on", small, ":")
    print(" ", vec_classify(small))
    print("  💡 np.vectorize is a convenience, not a real speedup.")
    print()


# ---------------------------------------------------------------------------
# SECTION 5: Memory & dtype control
# ---------------------------------------------------------------------------
# Choosing the right dtype saves memory. float32 uses half the bytes of
# float64. We also look at views vs copies and .nbytes.
# Docs: https://numpy.org/doc/stable/user/basics.types.html


def section_memory():
    print("=" * 50)
    print("SECTION 5: Memory & dtype control")
    print("=" * 50)

    big = np.ones(1_000_000)
    big32 = big.astype(np.float32)
    print(f"float64 array: {big.nbytes / 1e6:.1f} MB")
    print(f"float32 array: {big32.nbytes / 1e6:.1f} MB")
    print("  💡 float32 uses half the memory.")
    print()

    # astype makes a COPY; a view shares memory.
    a = np.array([1, 2, 3])
    _copy = a.astype(np.float64)
    _view = a.view(np.int64)
    print("a:", a)
    print("  astype -> new dtype, new memory (a copy).")
    print("  view   -> same memory, reinterpreted.")
    print()

    # .itemsize is bytes per element.
    print("  int64 itemsize:", np.array([1]).itemsize, "bytes")
    print("  float32 itemsize:", np.float32(1).itemsize, "bytes")
    print()


# ---------------------------------------------------------------------------
# SECTION 6: Advanced indexing — np.take / np.put / np.ix_
# ---------------------------------------------------------------------------
# np.take gathers elements by index; np.put scatters values into positions.
# np.ix_ builds an "outer" indexer for selecting rows AND columns at once.
# Docs: https://numpy.org/doc/stable/reference/routines.indexing.html


def section_advanced_indexing():
    print("=" * 50)
    print("SECTION 6: Advanced indexing (take / put / ix_)")
    print("=" * 50)

    a = np.array([10, 20, 30, 40, 50])
    print("a:", a)
    print("  np.take(a, [0, 2, 4]):", np.take(a, [0, 2, 4]))
    print()

    # np.put modifies in place at given indices.
    b = np.array([1, 2, 3, 4, 5])
    np.put(b, [0, 2], [99, 88])
    print("After np.put(b, [0, 2], [99, 88]):", b)
    print()

    # np.ix_ selects specific rows AND columns simultaneously.
    m = np.arange(1, 13).reshape(3, 4)
    print("m:")
    print(m)
    print()
    rows = np.array([0, 2])
    cols = np.array([1, 3])
    print("m[np.ix_(rows, cols)] (rows 0,2 and cols 1,3):")
    print(m[np.ix_(rows, cols)])
    print()


# ---------------------------------------------------------------------------
# SECTION 7: Polynomials & curve fitting (np.polyfit)
# ---------------------------------------------------------------------------
# np.polyfit fits a polynomial to data (least squares). np.polyval
# evaluates it. This is a first taste of modeling real data.
# Docs: https://numpy.org/doc/stable/reference/routines.polynomials.html


def section_polyfit():
    print("=" * 50)
    print("SECTION 7: Polynomials & curve fitting")
    print("=" * 50)

    # Some "noisy" data that follows a line: y = 2x + 1.
    x = np.array([0, 1, 2, 3, 4, 5])
    y = np.array([1.1, 3.2, 4.9, 7.0, 9.1, 11.2])

    # Fit a degree-1 (linear) polynomial.
    slope, intercept = np.polyfit(x, y, 1)
    print("x:", x)
    print("y:", y)
    print(f"  Linear fit: y = {slope:.2f}x + {intercept:.2f}")
    print()

    # Predict with np.polyval.
    predicted = np.polyval([slope, intercept], x)
    print("  Predicted values:", np.round(predicted, 2))
    print()

    # Fit a degree-2 (quadratic) polynomial.
    coeffs = np.polyfit(x, y, 2)
    print("  Quadratic coefficients:", np.round(coeffs, 2))
    print()


# ---------------------------------------------------------------------------
# SECTION 8: Missing data (np.nan) & masked arrays
# ---------------------------------------------------------------------------
# Real data has gaps. np.nan represents a missing number; np.nan* functions
# ignore it. A masked array lets you hide invalid values from calculations.
# Docs: https://numpy.org/doc/stable/reference/maskedarray.html


def section_nan():
    print("=" * 50)
    print("SECTION 8: Missing data (np.nan) & masked arrays")
    print("=" * 50)

    data = np.array([1.0, np.nan, 3.0, np.nan, 5.0])
    print("data:", data)
    print()

    # Plain mean returns NaN if any value is NaN.
    print("  data.mean():", data.mean(), "  (NaN poisons the result)")
    print("  np.nanmean(data):", np.nanmean(data))
    print("  np.nansum(data):", np.nansum(data))
    print()

    # Detect NaN positions.
    print("  np.isnan(data):", np.isnan(data))
    print("  Count of NaN:", np.isnan(data).sum())
    print()

    # Fill NaN with a value.
    filled = np.where(np.isnan(data), 0, data)
    print("  NaN filled with 0:", filled)
    print()

    # A masked array hides invalid values from all operations.
    masked = np.ma.masked_invalid(data)
    print("  Masked array:", masked)
    print("  masked.mean():", masked.mean())
    print()


# ---------------------------------------------------------------------------
# SECTION 9: A real-world mini task (all concepts combined)
# ---------------------------------------------------------------------------
# Task: load sensor data, handle a missing reading, fit a trend line per
# sensor, and report which sensor is rising fastest. This pulls together
# loading, structured data, NaN handling, and polyfit.


def section_summary_task():
    print("=" * 50)
    print("SECTION 9: Mini task — sensor trend analysis")
    print("=" * 50)

    # Load the CSV (skip the header row).
    data = np.loadtxt(MEASUREMENTS_FILE, delimiter=",", skiprows=1)
    sensor_ids = data[:, 0].astype(int)
    readings = data[:, 1]
    days = data[:, 2]
    print("Loaded measurements.csv:", data.shape, "rows")
    print()

    # Simulate a missing reading for sensor 2 on day 3.
    readings = readings.copy()
    readings[(sensor_ids == 2) & (days == 3)] = np.nan
    print("Introduced a NaN for sensor 2, day 3.")
    print()

    # Fit a linear trend (slope) for each sensor, ignoring NaN.
    print("Per-sensor trend (slope of reading vs day):")
    for sensor in np.unique(sensor_ids):
        mask = sensor_ids == sensor
        sr = readings[mask]
        sd = days[mask]
        valid = ~np.isnan(sr)
        slope, _intercept = np.polyfit(sd[valid], sr[valid], 1)
        print(f"  Sensor {sensor}: slope={slope:+.3f} per day")
    print()

    # Which sensor has the steepest rise?
    slopes = {}
    for sensor in np.unique(sensor_ids):
        mask = sensor_ids == sensor
        sr = readings[mask]
        sd = days[mask]
        valid = ~np.isnan(sr)
        slope, _ = np.polyfit(sd[valid], sr[valid], 1)
        slopes[sensor] = slope
    fastest = max(slopes, key=slopes.get)
    print(f"Fastest-rising sensor: {fastest} (slope {slopes[fastest]:+.3f})")
    print()


# ---------------------------------------------------------------------------
# OPTION 0: Clean up the generated files
# ---------------------------------------------------------------------------
# This lesson is predominantly in-memory; it writes no output files. We
# include a cleanup routine for consistency with the rest of the series.


CLEANUP_FILES = []


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
        print("Nothing to remove — this lesson writes no output files.")

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
    "1": ("Structured arrays & record arrays", section_structured),
    "2": ("Vectorized string operations (np.char)", section_strings),
    "3": ("Advanced broadcasting & meshgrid", section_meshgrid),
    "4": ("Performance: vectorization vs loops", section_performance),
    "5": ("Memory & dtype control", section_memory),
    "6": ("Advanced indexing (take / put / ix_)", section_advanced_indexing),
    "7": ("Polynomials & curve fitting (np.polyfit)", section_polyfit),
    "8": ("Missing data (np.nan) & masked arrays", section_nan),
    "9": ("Mini task: sensor trend analysis", section_summary_task),
}


def main():
    print("\n🔢 Welcome to the NumPy Advanced Tutorial!\n")
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
