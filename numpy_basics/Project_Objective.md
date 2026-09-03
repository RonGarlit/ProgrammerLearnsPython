# 🔢 NumPy Basics with Python

Below is a complete, runnable Python application designed to teach a beginner
**how to work with numerical data using NumPy** — the foundational library for
fast numerical computing in Python. It's a small interactive "study session"
that walks through each concept with real working examples, heavy commenting,
and links to the official NumPy documentation for further reading.

> This folder covers **NumPy basics only**. Intermediate and advanced NumPy
> (broadcasting, boolean masking, linear algebra, random numbers, etc.) will
> be built out in later folders.

---

## Code Analysis Summary

- **Purpose:** A single-file interactive teaching tool that demonstrates
  working with numerical data using **NumPy** and its `ndarray` object.
- **Concepts covered:** what NumPy is & how to install it, creating arrays
  (`np.array`, `arange`, `zeros`, `ones`, `linspace`), exploring with
  `shape`/`ndim`/`size`/`dtype`, indexing & slicing, vectorized math,
  universal functions, aggregations (`sum`/`mean`/`min`/`max`/`std`), saving &
  loading arrays, and combining the concepts in a real mini task.
- **Style:** Heavily commented so each construct is explained _where it
  appears_; safe for beginners — the only files it creates are small data
  files in the same folder (`saved_array.txt`, `saved_array.npy`).
- **Notable patterns:** Uses `save_array()` / `load_array()` helpers, a
  `main()` function as an entry point, a `menu`-driven loop, and a classic
  `if __name__ == "__main__"` guard.

---

## The Concepts (one per section)

| #   | Concept             | What it shows                                                  |
| --- | ------------------- | -------------------------------------------------------------- |
| 1   | What is NumPy?      | A third-party library; the `ndarray`; `pip install numpy`      |
| 2   | Creating arrays     | `np.array`, `np.arange`, `np.zeros`, `np.ones`, `np.linspace`  |
| 3   | Exploring an array  | `shape`, `ndim`, `size`, `dtype`                               |
| 4   | Indexing & slicing  | `arr[i]`, `arr[row, col]`, slices are views (use `.copy()`)    |
| 5   | Vectorized math     | Element-wise `+ - * /`, comparisons, vs a Python loop          |
| 6   | Universal functions | `np.sqrt`, `np.round`, `np.abs`, `np.exp`, `np.log`, `np.clip` |
| 7   | Aggregations        | `sum`, `mean`, `min`, `max`, `std`, `argmax`, axis-based       |
| 8   | Saving & loading    | `np.savetxt`/`np.loadtxt`, `np.save`/`np.load` (.npy)          |
| 9   | Mini task           | Sensor reading summary — loading + slicing + aggregating       |

---

## Design Principles

### 1. Third-party, but one install

Unlike the built-in `csv` module, NumPy must be installed once:

```powershell
pip install numpy
```

After that, everything in this lesson uses NumPy only — no other packages.

### 2. Vectorization first

The single most important idea in NumPy is **vectorization**: operations run
across the whole array at once instead of in a Python loop. The lesson
introduces this early (Section 5) and contrasts it with a list comprehension
so the learner sees both the speed and the readability win.

### 3. Foundation for pandas

pandas is built on top of NumPy — a DataFrame's columns are NumPy arrays.
This lesson frames every concept with that in mind, so the learner builds the
mental model they'll need for the pandas series.

### 4. Progressive, self-contained sections

Each section is an independent function with its own docstring and docs links.
A learner can run Section 9 (the mini task) without re-reading Sections 1–8,
because each section re-creates the data it needs.

---

## How to run

```powershell
pip install numpy
python numpy_basics.py
```

Type a number `0`–`9` to run a section, or `q` to quit. Use option **0** to
delete the generated files and start fresh.
