"""
NumPy Intermediate with Python — A Self-Guided Lesson
=====================================================
Run this file (with `python numpy_intermediate.py`) and follow along.

This is the SECOND step in NumPy. We assume you already completed
`numpy_basics` (creating arrays, indexing, vectorized math, ufuncs,
aggregations, and saving/loading). Here we level up with the tools you
reach for on real data:

  1. Reshaping & transposing arrays (reshape, ravel, transpose)
  2. Stacking & splitting arrays (concatenate, vstack, hstack, split)
  3. Boolean masking — filtering with conditions
  4. Fancy indexing — selecting with arrays of indices
  5. Broadcasting — how arrays of different shapes work together
  6. Random numbers (np.random) — simulations & reproducibility
  7. Linear algebra basics (dot, matmul, transpose, inverse)
  8. Advanced aggregation (percentiles, unique, where, any/all)
  9. A real-world mini task that combines everything

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
# SECTION 1: Reshaping & transposing arrays
# ---------------------------------------------------------------------------
# reshape() changes the shape of an array WITHOUT changing its data or
# element count. ravel() flattens to 1D. transpose() (or .T) swaps axes.
# Docs: https://numpy.org/doc/stable/reference/routines.array-manipulation.html


def section_reshape():
    print("=" * 50)
    print("SECTION 1: Reshaping & transposing arrays")
    print("=" * 50)

    a = np.arange(1, 13)  # 1..12
    print("a = np.arange(1, 13):", a)
    print()

    # Reshape 12 elements into a 3x4 grid.
    m = a.reshape(3, 4)
    print("a.reshape(3, 4):")
    print(m)
    print()

    # -1 lets NumPy infer that dimension from the total size.
    m2 = a.reshape(2, -1)  # 2 rows, columns inferred -> 6
    print("a.reshape(2, -1):")
    print(m2)
    print()

    # ravel() flattens back to 1D.
    print("m.ravel():", m.ravel())
    print()

    # transpose() / .T swaps rows and columns.
    print("m.T (transpose):")
    print(m.T)
    print()

    # reshape returns a VIEW when possible — changing it changes the
    # original. Use .copy() if you need independence.
    view = a.reshape(3, 4)
    view[0, 0] = 999
    print("After modifying a reshape, original a:", a)
    print("  💡 reshape can return a view — use .copy() to detach.")
    print()


# ---------------------------------------------------------------------------
# SECTION 2: Stacking & splitting arrays
# ---------------------------------------------------------------------------
# np.concatenate joins arrays along an existing axis. np.vstack / np.hstack
# stack vertically (rows) or horizontally (columns). np.split divides.
# Docs: https://numpy.org/doc/stable/reference/routines.array-manipulation.html


def section_stacking():
    print("=" * 50)
    print("SECTION 2: Stacking & splitting arrays")
    print("=" * 50)

    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])

    # Concatenate along the only axis (1D).
    print("np.concatenate([a, b]):", np.concatenate([a, b]))
    print()

    # vstack makes them rows; hstack makes them columns.
    print("np.vstack([a, b]):")
    print(np.vstack([a, b]))
    print()
    print("np.hstack([a, b]):", np.hstack([a, b]))
    print()

    # Split an array into parts.
    arr = np.arange(10)
    parts = np.split(arr, [3, 7])  # split before index 3 and 7
    print("np.split(np.arange(10), [3, 7]):")
    for i, part in enumerate(parts):
        print(f"  part {i}: {part}")
    print()


# ---------------------------------------------------------------------------
# SECTION 3: Boolean masking — filtering with conditions
# ---------------------------------------------------------------------------
# A boolean mask is an array of True/False. Indexing an array with a mask
# keeps only the elements where the mask is True. This is the NumPy
# equivalent of pandas filtering.
# Docs: https://numpy.org/doc/stable/user/basics.indexing.html#boolean-array-indexing


def section_masking():
    print("=" * 50)
    print("SECTION 3: Boolean masking")
    print("=" * 50)

    data = np.array([12.5, 22.4, 8.2, 14.2, 24.5, 8.6])
    print("data:", data)
    print()

    # Build a mask with a comparison.
    mask = data > 15
    print("mask = data > 15:", mask)
    print("data[mask]:", data[mask])
    print()

    # Combine conditions with & (and) and | (or). Parentheses required!
    between = data[(data > 10) & (data < 20)]
    print("data[(data > 10) & (data < 20)]:", between)
    print()

    # Count how many satisfy a condition.
    print("Count > 15:", (data > 15).sum())
    print("Fraction > 15:", (data > 15).mean())
    print()

    # Replace values using a mask (like df.loc in pandas).
    clipped = data.copy()
    clipped[clipped > 20] = 20
    print("Values > 20 replaced with 20:", clipped)
    print()


# ---------------------------------------------------------------------------
# SECTION 4: Fancy indexing — selecting with arrays of indices
# ---------------------------------------------------------------------------
# Instead of a boolean mask, we can index with an ARRAY of integer
# positions. This lets us pick any subset, in any order, with repeats.
# Docs: https://numpy.org/doc/stable/user/basics.indexing.html#integer-array-indexing


def section_fancy():
    print("=" * 50)
    print("SECTION 4: Fancy indexing")
    print("=" * 50)

    a = np.array([10, 20, 30, 40, 50])
    print("a:", a)
    print()

    # Select specific positions.
    print("a[[0, 2, 4]]:", a[[0, 2, 4]])
    print("a[[4, 3, 2, 1, 0]] (reversed):", a[[4, 3, 2, 1, 0]])
    print()

    # Repeats are allowed.
    print("a[[0, 0, 1, 1]]:", a[[0, 0, 1, 1]])
    print()

    # Fancy indexing on a 2D array: pick rows.
    m = np.arange(1, 13).reshape(3, 4)
    print("m:")
    print(m)
    print()
    print("m[[0, 2]] (rows 0 and 2):")
    print(m[[0, 2]])
    print()

    # Combine with a mask to get indices of values meeting a condition.
    # np.nonzero returns the indices where the condition is True.
    idx = np.nonzero(a > 30)
    print("np.nonzero(a > 30):", idx, "->", a[idx])
    print()


# ---------------------------------------------------------------------------
# SECTION 5: Broadcasting — how arrays of different shapes work together
# ---------------------------------------------------------------------------
# Broadcasting lets NumPy apply an operation between arrays of DIFFERENT
# shapes by stretching the smaller one to match. It's what makes
# `arr + scalar` and `matrix + row_vector` work without explicit loops.
# Docs: https://numpy.org/doc/stable/user/basics.broadcasting.html


def section_broadcasting():
    print("=" * 50)
    print("SECTION 5: Broadcasting")
    print("=" * 50)

    # Scalar broadcasting: a scalar stretches to match the array.
    a = np.array([1, 2, 3])
    print("a:", a)
    print("  a + 10:", a + 10, "  (scalar broadcast)")
    print()

    # Row vector broadcast across rows of a matrix.
    m = np.array([[1, 2, 3], [4, 5, 6]])
    row = np.array([10, 20, 30])
    print("m:")
    print(m)
    print("row:", row)
    print("  m + row:")
    print(m + row)
    print()

    # Column vector broadcast down columns.
    col = np.array([[100], [200]])
    print("col:")
    print(col)
    print("  m + col:")
    print(m + col)
    print()

    # Normalize: subtract the column mean from each column.
    data = np.array([[10.0, 20.0], [30.0, 40.0], [50.0, 60.0]])
    col_means = data.mean(axis=0)
    print("data:")
    print(data)
    print("column means:", col_means)
    print("  data - col_means (centered):")
    print(data - col_means)
    print()


# ---------------------------------------------------------------------------
# SECTION 6: Random numbers (np.random)
# ---------------------------------------------------------------------------
# np.random generates random data for simulations, sampling, and testing.
# A SEED makes the "random" sequence reproducible — essential for lessons
# and debugging.
# Docs: https://numpy.org/doc/stable/reference/random/index.html


def section_random():
    print("=" * 50)
    print("SECTION 6: Random numbers")
    print("=" * 50)

    # Seed for reproducibility — same seed, same numbers.
    rng = np.random.default_rng(42)
    print("rng = np.random.default_rng(42) — reproducible:\n")

    # Uniform random floats in [0, 1).
    print("rng.random(5):", np.round(rng.random(5), 3))
    print()

    # Integers in a range.
    print("rng.integers(1, 7, size=5) (like dice):", rng.integers(1, 7, size=5))
    print()

    # Normal (Gaussian) distribution.
    print("rng.normal(0, 1, 5) (mean 0, std 1):", np.round(rng.normal(0, 1, 5), 3))
    print()

    # Simulate: 1000 coin flips, count heads.
    flips = rng.integers(0, 2, size=1000)
    print(f"1000 coin flips -> heads: {flips.sum()}, tails: {1000 - flips.sum()}")
    print()


# ---------------------------------------------------------------------------
# SECTION 7: Linear algebra basics
# ---------------------------------------------------------------------------
# NumPy has a full linear-algebra toolbox. The most common operations are
# dot products, matrix multiplication, and transposes.
# Docs: https://numpy.org/doc/stable/reference/routines.linalg.html


def section_linalg():
    print("=" * 50)
    print("SECTION 7: Linear algebra basics")
    print("=" * 50)

    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])

    # Dot product: sum of element-wise products.
    print("a:", a, " b:", b)
    print("  np.dot(a, b):", np.dot(a, b), "  (1*4 + 2*5 + 3*6)")
    print()

    # Matrix multiplication with @ (or np.matmul).
    m1 = np.array([[1, 2], [3, 4]])
    m2 = np.array([[5, 6], [7, 8]])
    print("m1:")
    print(m1)
    print("m2:")
    print(m2)
    print("  m1 @ m2:")
    print(m1 @ m2)
    print()

    # Transpose swaps rows and columns.
    print("m1.T:")
    print(m1.T)
    print()

    # Inverse of a square matrix.
    inv = np.linalg.inv(m1)
    print("np.linalg.inv(m1):")
    print(np.round(inv, 2))
    print("  m1 @ inv (should be identity):")
    print(np.round(m1 @ inv, 2))
    print()


# ---------------------------------------------------------------------------
# SECTION 8: Advanced aggregation (percentiles, unique, where, any/all)
# ---------------------------------------------------------------------------
# Beyond sum/mean/min/max, NumPy offers percentiles, unique values,
# np.where (conditional selection), and any/all (reduce booleans).
# Docs: https://numpy.org/doc/stable/reference/routines.statistics.html


def section_advanced_agg():
    print("=" * 50)
    print("SECTION 8: Advanced aggregation")
    print("=" * 50)

    data = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    print("data:", data)
    print()

    # Percentiles.
    print("  np.percentile(data, 25):", np.percentile(data, 25))
    print("  np.percentile(data, 50) (median):", np.percentile(data, 50))
    print("  np.percentile(data, 75):", np.percentile(data, 75))
    print("  np.median(data):", np.median(data))
    print()

    # Unique values and their counts.
    vals = np.array([1, 2, 2, 3, 3, 3, 4])
    uniq, counts = np.unique(vals, return_counts=True)
    print("vals:", vals)
    print("  np.unique:", uniq)
    print("  counts:", counts)
    print()

    # np.where(condition, x, y) — element-wise conditional selection.
    a = np.array([1, 5, 3, 8, 2])
    result = np.where(a > 4, "high", "low")
    print("a:", a)
    print("  np.where(a > 4, 'high', 'low'):", result)
    print()

    # any() / all() reduce a boolean array.
    print("  (a > 4).any():", (a > 4).any(), "  (a > 4).all():", (a > 4).all())
    print()


# ---------------------------------------------------------------------------
# SECTION 9: A real-world mini task (all concepts combined)
# ---------------------------------------------------------------------------
# Task: analyze sensor readings. Load the CSV, compute per-sensor stats,
# flag readings above a threshold, and report the results. This pulls
# together loading, masking, fancy indexing, and aggregation.


def section_summary_task():
    print("=" * 50)
    print("SECTION 9: Mini task — sensor anomaly detection")
    print("=" * 50)

    # Load the CSV (skip the header row).
    data = np.loadtxt(MEASUREMENTS_FILE, delimiter=",", skiprows=1)
    sensor_ids = data[:, 0].astype(int)
    readings = data[:, 1]
    print("Loaded measurements.csv:", data.shape, "rows")
    print()

    # Per-sensor summary using a mask.
    print("Per-sensor summary:")
    for sensor in np.unique(sensor_ids):
        mask = sensor_ids == sensor
        sr = readings[mask]
        print(
            f"  Sensor {sensor}: mean={sr.mean():.2f}, "
            f"max={sr.max():.2f}, std={sr.std():.2f}"
        )
    print()

    # Flag readings above the overall 75th percentile as "high".
    threshold = np.percentile(readings, 75)
    high_mask = readings > threshold
    print(f"75th percentile threshold: {threshold:.2f}")
    print(f"High readings ({high_mask.sum()}): {readings[high_mask]}")
    print()

    # Which sensors produced the high readings?
    high_sensors = sensor_ids[high_mask]
    print("Sensors with high readings:", np.unique(high_sensors))
    print()

    # Overall stats.
    print(f"Overall mean: {readings.mean():.2f}")
    print(f"Overall std:  {readings.std():.2f}")
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
    "1": ("Reshaping & transposing arrays", section_reshape),
    "2": ("Stacking & splitting arrays", section_stacking),
    "3": ("Boolean masking", section_masking),
    "4": ("Fancy indexing", section_fancy),
    "5": ("Broadcasting", section_broadcasting),
    "6": ("Random numbers (np.random)", section_random),
    "7": ("Linear algebra basics", section_linalg),
    "8": ("Advanced aggregation", section_advanced_agg),
    "9": ("Mini task: sensor anomaly detection", section_summary_task),
}


def main():
    print("\n🔢 Welcome to the NumPy Intermediate Tutorial!\n")
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
