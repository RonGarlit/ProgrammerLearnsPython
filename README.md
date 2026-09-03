# 🐍 Programmer Learns Python

A collection of self-guided, interactive Python lessons. Each lesson is a
single-file program with a menu-driven loop, heavy commenting, and links to the
official Python documentation — designed so you can study one concept at a time
and repeat it as often as you like.

## 📁 What's in this repo

The lessons are ordered as a **learning path** — each builds on the ones before
it. Start at the top and work down.

| #  | Folder                                                          | Status       | What it teaches                                                                                                             |
| -- | --------------------------------------------------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------- |
| 1  | [`builtins_basics/`](builtins_basics/README.md)                 | ✅ Completed | Core Python building blocks: variables, input, conditionals, loops, lists & dicts, functions, error handling, sets & tuples |
| 2  | [`builtins_intermediate/`](builtins_intermediate/README.md)     | ✅ Completed | Practical stdlib: `pathlib`, `json`, `datetime`, `collections`, comprehensions, generators, `*args`/`**kwargs`, `lambda`    |
| 3  | [`builtins_advanced/`](builtins_advanced/README.md)             | ✅ Completed | Design patterns: OOP, inheritance & dunders, decorators, context managers, `itertools`, `functools`, type hints, exceptions |
| 4  | [`testing_pytest/`](testing_pytest/README.md)                   | ✅ Completed | Automated testing with **pytest**: `assert`, fixtures, parametrization, `pytest.raises`, markers                              |
| 5  | [`csv_basics_built_in/`](csv_basics_built_in/README.md)         | ✅ Completed | Reading & writing CSV files using only Python's built-in `csv` module                                                       |
| 6  | [`numpy_basics/`](numpy_basics/README.md)                       | ✅ Completed | NumPy essentials: arrays, indexing, vectorized math, ufuncs, aggregations, saving/loading                                   |
| 7  | [`numpy_intermediate/`](numpy_intermediate/README.md)           | ✅ Completed | Intermediate NumPy: reshape, stacking, masking, fancy indexing, broadcasting, random, linear algebra                        |
| 8  | [`numpy_advanced/`](numpy_advanced/README.md)                   | ✅ Completed | Advanced NumPy: structured arrays, `np.char`, `meshgrid`, performance, dtype control, `polyfit`, missing data               |
| 9  | [`csv_pandas_basics/`](csv_pandas_basics/README.md)             | ✅ Completed | Working with CSV data using **pandas** — `DataFrame`s (introductory)                                                        |
| 10 | [`csv_pandas_intermediate/`](csv_pandas_intermediate/README.md) | ✅ Completed | Intermediate pandas: missing values, sorting, dates, merging, pivots, `.apply()`, strings                                   |
| 11 | [`csv_pandas_advanced/`](csv_pandas_advanced/README.md)         | ✅ Completed | Advanced pandas: `MultiIndex`, reshape, categories, windows, time-series resampling, pipelines                              |

> 💡 **Why this order?** Lessons 1–3 teach the Python language itself. Lesson 4
> introduces **automated testing** with pytest, so you can verify the code you
> write. Lesson 5 introduces data files with the standard library. Lessons 6–8
> teach **NumPy**, the fast array library that **pandas is built on top of**.
> Lessons 9–11 then build pandas on that foundation. Following the path in
> order means every lesson's prerequisites are already covered.

---

## ✅ Completed lessons

### 1. `builtins_basics/` — Python Essentials

A single-file interactive tutorial (`builtins_essentials.py`) that walks through
the core building blocks of the language, one concept per section:

| #   | Concept                  |
| --- | ------------------------ |
| 1   | Variables & Data Types   |
| 2   | Input & Type Conversion  |
| 3   | Conditionals             |
| 4   | Loops                    |
| 5   | Lists & Dictionaries     |
| 6   | Functions                |
| 7   | Error Handling           |
| 8   | Sets & Tuples            |
| 9   | String Methods & Slicing |

Run it from the `builtins_basics/` folder:

```powershell
python builtins_essentials.py
```

### 2. `builtins_intermediate/` — Intermediate Built-ins

A single-file interactive lesson (`builtins_intermediate.py`) that covers the
practical Python **standard library** you reach for right after fundamentals —
files, JSON, dates, specialized containers, and expressive syntax — all built-in:

| #   | Concept                    |
| --- | -------------------------- |
| 0   | Clean up the output files  |
| 1   | Text files with `pathlib`  |
| 2   | The `json` module          |
| 3   | The `datetime` module      |
| 4   | The `collections` module   |
| 5   | Comprehensions             |
| 6   | Generators                 |
| 7   | `*args` / `**kwargs`       |
| 8   | `lambda` + map/filter      |
| 9   | Mini task: summarize a log |

Run it from the `builtins_intermediate/` folder:

```powershell
python builtins_intermediate.py
```

> 💡 **Key ideas:** all built-in (no `pip install`); `pathlib` for files, `json`
> for data exchange, `datetime` for time, `collections` for containers.

### 3. `builtins_advanced/` — Advanced Built-ins

A single-file interactive lesson (`builtins_advanced.py`) that takes you into
Python's power features for designing clean, reusable code — still entirely
standard library:

| #   | Concept                     |
| --- | --------------------------- |
| 0   | Clean up the output files   |
| 1   | OOP: classes                |
| 2   | Inheritance & dunders       |
| 3   | Decorators                  |
| 4   | Context managers            |
| 5   | The `itertools` module      |
| 6   | The `functools` module      |
| 7   | Type hints                  |
| 8   | Deep error handling         |
| 9   | Mini task: inventory system |

Run it from the `builtins_advanced/` folder:

```powershell
python builtins_advanced.py
```

> 💡 **Key ideas:** classes & inheritance, decorators, custom context managers,
> `itertools`/`functools`, type hints, and custom exceptions.

### 4. `testing_pytest/` — Testing with pytest

A single-file interactive lesson (`testing_pytest.py`) that teaches how to
write **automated tests** for the pure-Python code you already know how to
write. It ships with multiple `test_*.py` files (one per concept) so you can
run `pytest` and see real pass/fail reports:

| #   | Concept                        |
| --- | ------------------------------ |
| 0   | Clean up the generated files   |
| 1   | What is testing & why          |
| 2   | pytest basics                  |
| 3   | Fixtures                       |
| 4   | Parametrization                |
| 5   | Testing functions & classes    |
| 6   | Testing exceptions             |
| 7   | Markers & skipping             |
| 8   | Mini task: test the Inventory  |

Run it from the `testing_pytest/` folder:

```powershell
pip install pytest
python testing_pytest.py
pytest
```

> 💡 **Key ideas:** `assert`, pytest discovery rules, fixtures, parametrization,
> `pytest.raises` for exceptions, and markers. The classes under test mirror
> the ones from `builtins_advanced`.

### 5. `csv_basics_built_in/` — CSV with the built-in `csv` module

A single-file interactive lesson (`csv_basics.py`) that teaches how to read and
write CSV files using only Python's standard library — no third-party packages:

| #   | Concept                          |
| --- | -------------------------------- |
| 0   | Clean up the generated CSV files |
| 1   | What is a CSV file?              |
| 2   | Reading with `DictReader`        |
| 3   | Writing with `DictWriter`        |
| 4   | Filtering & writing results      |
| 5   | `reader` / `writer` (lists)      |
| 6   | Quoting tricky data              |
| 7   | Mini task: average salary        |

Run it from the `csv_basics_built_in/` folder:

```powershell
python csv_basics.py
```

> 💡 **Tip:** Sections 2–6 create small `.csv` files (`employees.csv`,
> `managers.csv`, `numbers.csv`, `tricky.csv`) in the folder. Use menu option
> **0** to delete them all and start fresh.

### 6. `numpy_basics/` — NumPy essentials

A single-file interactive lesson (`numpy_basics.py`) that teaches the
foundational library for fast numerical computing. pandas is built on top of
NumPy, so this is the foundation for everything that follows:

| #   | Concept                      |
| --- | ---------------------------- |
| 0   | Clean up the generated files |
| 1   | What is NumPy?               |
| 2   | Creating arrays              |
| 3   | Exploring an array           |
| 4   | Indexing & slicing arrays    |
| 5   | Vectorized math              |
| 6   | Universal functions (ufuncs) |
| 7   | Aggregations                 |
| 8   | Saving & loading arrays      |
| 9   | Mini task: sensor summary    |

Run it from the `numpy_basics/` folder:

```powershell
pip install numpy
python numpy_basics.py
```

> 💡 **Key ideas:** the `ndarray`, vectorized element-wise math, ufuncs, and
> aggregations — the building blocks of fast numerical computing.

### 7. `numpy_intermediate/` — Intermediate NumPy

A single-file interactive lesson (`numpy_intermediate.py`) that takes the next
step beyond the basics. It teaches the tools for **selecting and combining**
numerical data:

| #   | Concept                      |
| --- | ---------------------------- |
| 0   | Clean up the generated files |
| 1   | Reshaping & transposing      |
| 2   | Stacking & splitting         |
| 3   | Boolean masking              |
| 4   | Fancy indexing               |
| 5   | Broadcasting                 |
| 6   | Random numbers (`np.random`) |
| 7   | Linear algebra basics        |
| 8   | Advanced aggregation         |
| 9   | Mini task: sensor anomalies  |

Run it from the `numpy_intermediate/` folder:

```powershell
pip install numpy
python numpy_intermediate.py
```

> 💡 **Key ideas:** filtering with boolean masks, fancy indexing, broadcasting
> shapes together, and reproducible random numbers for simulations.

### 8. `numpy_advanced/` — Advanced NumPy

A single-file interactive lesson (`numpy_advanced.py`) that completes the NumPy
series. It teaches the tools for **performance, structure, and real-world
scale**:

| #   | Concept                        |
| --- | ------------------------------ |
| 0   | Clean up the generated files   |
| 1   | Structured arrays              |
| 2   | Vectorized strings (`np.char`) |
| 3   | `meshgrid` & broadcasting      |
| 4   | Performance: vectorization     |
| 5   | Memory & dtype control         |
| 6   | Advanced indexing              |
| 7   | Curve fitting (`np.polyfit`)   |
| 8   | Missing data (`np.nan`)        |
| 9   | Mini task: sensor trends       |

Run it from the `numpy_advanced/` folder:

```powershell
pip install numpy
python numpy_advanced.py
```

> 💡 **Key ideas:** dtype & memory control, handling missing data, fitting
> trend lines with `polyfit`, and structured arrays — the skills you need
> before moving to pandas and beyond.

### 9. `csv_pandas_basics/` — CSV with pandas

A single-file interactive lesson (`pandas_basics.py`) that teaches how to work
with tabular data using **pandas** and its `DataFrame` object. Unlike the
built-in `csv` module, pandas **infers data types automatically**, so numbers
come in as numbers and math just works:

| #   | Concept                          |
| --- | -------------------------------- |
| 0   | Clean up the generated CSV files |
| 1   | What is pandas?                  |
| 2   | Reading with `read_csv`          |
| 3   | Exploring a DataFrame            |
| 4   | Selecting columns & rows         |
| 5   | Filtering by a condition         |
| 6   | Adding & modifying columns       |
| 7   | Grouping & aggregating           |
| 8   | Writing with `to_csv`            |
| 9   | Mini task: top product & region  |

Run it from the `csv_pandas_basics/` folder:

```powershell
pip install pandas
python pandas_basics.py
```

> 💡 **Tip:** Section 8 creates `high_sales.csv` and `monthly_summary.csv` in
> the folder. Use menu option **0** to delete them and start fresh.

### 10. `csv_pandas_intermediate/` — Intermediate pandas

A single-file interactive lesson (`pandas_intermediate.py`) that takes the next
step beyond the basics. It uses **two** related tables (and some deliberately
messy data with missing values) to teach the tools you reach for on real work:

| #   | Concept                           |
| --- | --------------------------------- |
| 0   | Clean up the generated CSV files  |
| 1   | Handling missing values (NaN)     |
| 2   | Sorting & ranking data            |
| 3   | Working with dates & times        |
| 4   | Merging & joining DataFrames      |
| 5   | Multi-level grouping & pivots     |
| 6   | Vectorized & `.apply()` functions |
| 7   | String operations on text         |
| 8   | Writing enhanced results          |
| 9   | Mini task: profit per region      |

Run it from the `csv_pandas_intermediate/` folder:

```powershell
pip install pandas
python pandas_intermediate.py
```

> 💡 **Key ideas:** handling missing values, merging tables like a SQL join,
> pivot tables, computing derived columns (e.g. `profit`), and avoiding the
> classic `SettingWithCopyWarning` trap by assigning with `.loc`.

### 11. `csv_pandas_advanced/` — Advanced pandas

A single-file interactive lesson (`pandas_advanced.py`) that completes the
pandas series. It uses **six months of daily sales** to teach the tools for
hierarchical, time-based, and large-scale data:

| #   | Concept                      |
| --- | ---------------------------- |
| 0   | Clean up the optional output |
| 1   | MultiIndex (hierarchical)    |
| 2   | `stack` / `unstack` reshape  |
| 3   | `melt` (wide → long)         |
| 4   | Categorical data             |
| 5   | Window functions (rolling)   |
| 6   | Time-series resampling       |
| 7   | Function pipelines (`.pipe`) |
| 8   | Advanced aggregation         |
| 9   | Mini task: weekly profit     |

Run it from the `csv_pandas_advanced/` folder:

```powershell
pip install pandas
python pandas_advanced.py
```

> 💡 **Key ideas:** MultiIndex labels, reshaping between long & wide, rolling/
> expanding windows, and downsampling/upsampling time-series data.

---

## 🚧 Upcoming lessons

All planned lessons are complete. Ideas for future lessons:

- **Plotting & visualization** with `matplotlib` / `plotly` (`df.plot()`).
- **Performance & big data** — chunked reading, `numba`, `dask`.
- **Machine learning intro** — preparing DataFrames for `scikit-learn`.

---

## ✅ Prerequisites

- **Python 3.11 or newer** (matches `requires-python` in `pyproject.toml`).
- **VS Code** with the **Python extension** (by Microsoft) installed.

Check your Python version:

```powershell
python --version
```

> 💡 **Note:** The `builtins_basics/`, `builtins_intermediate/`,
> `builtins_advanced/`, and `csv_basics_built_in/` lessons use only the Python
> standard library — nothing to `pip install`. All three NumPy lessons
> (`numpy_basics/`, `numpy_intermediate/`, `numpy_advanced/`) require **NumPy**,
> and all three pandas lessons (`csv_pandas_basics/`,
> `csv_pandas_intermediate/`, `csv_pandas_advanced/`) require **pandas**:
>
> ```powershell
> pip install pandas numpy
> ```
