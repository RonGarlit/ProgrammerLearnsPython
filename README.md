# 🐍 Programmer Learns Python

A collection of self-guided, interactive Python lessons. Each lesson is a
single-file program with a menu-driven loop, heavy commenting, and links to the
official Python documentation — designed so you can study one concept at a time
and repeat it as often as you like.

## 📑 Table of contents

- [What's in this repo](#-whats-in-this-repo)
- [How to use these lessons](#-how-to-use-these-lessons)
- [Completed lessons](#-completed-lessons)
- [Upcoming lessons](#-upcoming-lessons)
- [Prerequisites](#-prerequisites)

---

## 🚀 How to use these lessons

Every lesson follows the same pattern, so once you've done one you know how to
do them all:

1. **Open the folder** for the lesson you want (see the table below).
2. **Read that folder's `README.md`** — it explains the concepts, the
   prerequisites, and how to run the program.
3. **Run the program** from that folder (or from the project root — every
   script resolves its own file paths, so it works either way).
4. **Pick a menu option** — each lesson is menu-driven, so you can run one
   section at a time and repeat any section as often as you like.
5. **Step through it with the debugger** — every lesson's README includes a
   🐞 debugging walkthrough. Setting a breakpoint and watching variables change
   is the best way to really understand each concept.

> 💡 **Tip:** The lessons are ordered as a **learning path** — each builds on
> the ones before it. Start at the top and work down.

---

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
| 12 | [`py_sql_server_basics/`](py_sql_server_basics/README.md)       | ✅ Completed | SQL Server basics: `pyodbc`, `CREATE TABLE` for every type family, CSV → SQL type casting, `OUTPUT` clause, spatial/`HIERARCHYID`/`XML` |
| 13 | [`py_sql_server_intermediate/`](py_sql_server_intermediate/README.md) | ✅ Completed | SQL Server intermediate: the full **CRUD** cycle — `SELECT`/filtering/aggregates/`JOIN`s, `INSERT`/`UPDATE`/`DELETE`, transactions, and stored procedures |

> 💡 **Why this order?** Lessons 1–3 teach the Python language itself. Lesson 4
> introduces **automated testing** with pytest, so you can verify the code you
> write. Lesson 5 introduces data files with the standard library. Lessons 6–8
> teach **NumPy**, the fast array library that **pandas is built on top of**.
> Lessons 9–11 then build pandas on that foundation. Lessons 12–13 turn to a
> **relational database** — first getting CSV data into SQL Server (basics),
> then querying and manipulating it with the full CRUD cycle (intermediate).
> Following the path in order means every lesson's prerequisites are already
> covered.

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

### 12. `py_sql_server_basics/` — SQL Server basics with `pyodbc`

A lesson (`create_pytesttable.sql`, `pytesttable_data.csv`,
`load_pytesttable.py`) that teaches how to connect Python to **SQL Server** and
load CSV data into a table covering **every major SQL Server type family** —
including the tricky ones (`XML`, `HIERARCHYID`, `GEOGRAPHY`, `GEOMETRY`,
`SQL_VARIANT`). It's **menu-driven**, so you can set up, load, or clean up from
one script:

| # | Menu action | What it does                                                     |
| - | ----------- | ---------------------------------------------------------------- |
| 1 | **Setup**   | Runs `create_pytesttable.sql` to create `dbo.PyTestTable` (idempotent — safe to re-run) |
| 2 | **Load**    | `pyodbc` connect + parameterized `INSERT` with `OUTPUT`; casts CSV strings to SQL types; commits; verifies |
| 3 | **Cleanup** | Drops `dbo.PyTestTable` so you can start fresh                   |

The concepts the load step teaches:

| #   | Concept                          |
| --- | -------------------------------- |
| 1   | `CREATE TABLE` for every type family |
| 2   | Three rows of boundary/edge/NULL test data |
| 3   | `pyodbc` connect + parameterized `INSERT` with `OUTPUT` |
| 4   | Casting CSV strings to SQL types (`CAST`/`CONVERT`) |
| 5   | Spatial types, `HIERARCHYID`, `XML`, `SQL_VARIANT` |
| 6   | Transactions (`autocommit=False` + `commit()`) |
| 7   | Verification query |

Run it from the `py_sql_server_basics/` folder (after creating the `PyTestDb`
database once):

```powershell
pip install pyodbc
python load_pytesttable.py
```

Then pick an action from the menu — tip: choose **Setup**, then **Load**.

> 💡 **Key ideas:** CSV cells are always strings, so you must **cast** each one
> to the right SQL type; `OUTPUT INSERTED.Id` captures the identity value;
> `CONVERT(VARBINARY, ?, 1)` handles `0x`-prefixed hex; spatial WKT goes through
> `GEOGRAPHY::STGeomFromText(?, 4326)`; `HIERARCHYID` is set with a follow-up
> `UPDATE`.

### 13. `py_sql_server_intermediate/` — SQL Server intermediate with `pyodbc`

A menu-driven lesson (`create_pytestdb.sql`, `sql_server_intermediate.py`) that
takes the next step: the **full CRUD cycle** against a small, realistic
relational store schema (`Customers`, `Products`, `Orders`, `OrderItems`). It
covers CRUD **two ways** — with plain SQL statements, then with **logical
stored procedures** — plus transactions:

| # | Menu | What it teaches                                                        |
| - | ---- | ---------------------------------------------------------------------- |
| 0 | Setup       | Runs `create_pytestdb.sql` to build the schema, seed data, and stored procedures |
| c | Cleanup     | Drops the tables + stored procedures so you can start fresh            |
| 1 | SELECT basics | `WHERE`, `ORDER BY`, `TOP`, `DISTINCT`, column aliases               |
| 2 | Filtering   | `LIKE`, `IN`, `BETWEEN`, `IS NULL`                                     |
| 3 | Aggregates  | `COUNT`/`SUM`/`AVG`/`MIN`/`MAX`, `GROUP BY`, `HAVING`                  |
| 4 | JOINs       | `INNER`, `LEFT`, and a multi-table JOIN                                |
| 5 | CREATE      | Parameterized `INSERT` with `OUTPUT INSERTED.Id`                       |
| 6 | UPDATE      | `UPDATE ... SET ... WHERE` with `OUTPUT`                               |
| 7 | DELETE      | `DELETE ... WHERE` with `OUTPUT`                                       |
| 8 | Transactions| `BEGIN`/`COMMIT`/`ROLLBACK` with a forced error to show rollback       |
| 9 | Stored procedures | `EXEC` with input + output params; walking multiple result sets  |
| 10 | Mini task   | A full CRUD workflow combining everything                              |

Run it from the `py_sql_server_intermediate/` folder:

```powershell
pip install pyodbc
python sql_server_intermediate.py
```

Pick **0** (Setup) first to create and seed the schema — or just run the CRUD
sections. Use **c** (Cleanup) anytime to reset.

> 💡 **Key ideas:** real database work is **CRUD** — Create, Read, Update,
> Delete. You can do it all with plain SQL, or wrap repeated logic in **stored
> procedures** and just call them. This lesson shows both, and uses
> `autocommit=False` + explicit transactions so a failure rolls back cleanly.

---

## 🚧 Upcoming lessons

Ideas for future lessons (the pandas series and the SQL Server basics +
intermediate lessons are complete):

- **SQL Server advanced** — views, indexes, query tuning, dynamic SQL, and
  bridging query results into pandas.
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
>
> The `py_sql_server_basics/` and `py_sql_server_intermediate/` lessons require
> **pyodbc** (plus a local SQL Server and the ODBC Driver 18 for SQL Server):
>
> ```powershell
> pip install pyodbc
> ```
