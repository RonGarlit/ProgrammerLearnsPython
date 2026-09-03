# 🔢 NumPy Advanced with Python

Below is a complete, runnable Python application designed to take a learner
**from intermediate to advanced-level NumPy**. Building on the
`numpy_intermediate` folder, this interactive "study session" covers the tools
used for **performance, structure, and real-world scale**: structured arrays,
vectorized strings, `meshgrid`, performance measurement, memory & dtype
control, advanced indexing, curve fitting, and missing-data handling — all
with real working examples, heavy commenting, and links to the official NumPy
documentation.

> This folder covers **advanced NumPy**. It is the final NumPy lesson in this
> series (after `numpy_basics` and `numpy_intermediate`).

---

## Code Analysis Summary

- **Purpose:** A single-file interactive teaching tool that demonstrates
  advanced NumPy techniques on a 15-row sensor dataset.
- **Concepts covered:** structured arrays & `recarray`, `np.char` string
  operations, `np.meshgrid` & advanced broadcasting, vectorization vs loops
  (measured with `timeit`), memory & dtype control (`float32`/`float64`,
  `astype` vs `view`), advanced indexing (`np.take`/`np.put`/`np.ix_`),
  curve fitting (`np.polyfit`/`np.polyval`), missing data (`np.nan`,
  `np.nanmean`, masked arrays), and a capstone mini task.
- **Style:** Heavily commented so each construct is explained _where it
  appears_; safe for learners continuing from intermediate.
- **Notable patterns:** Reuses the `data_path()` helper for folder-relative
  paths (works from any folder); a `main()` menu loop and the classic
  `if __name__ == "__main__"` guard. This lesson is **predominantly
  in-memory** — it writes no output files, but includes a cleanup routine for
  consistency.

---

## The Concepts (one per section)

| #   | Concept                   | What it shows                                                               |
| --- | ------------------------- | --------------------------------------------------------------------------- |
| 1   | Structured arrays         | Mixed-type, named fields; `recarray` attribute access                       |
| 2   | Vectorized strings        | `np.char` — `upper`, `capitalize`, `startswith`, `find`, `replace`, `strip` |
| 3   | `meshgrid` & broadcasting | Build coordinate grids; evaluate functions over a whole plane               |
| 4   | Performance               | Vectorization vs loops (measured); `np.vectorize` convenience               |
| 5   | Memory & dtype            | `float32` vs `float64`; `astype` (copy) vs `view`; `.nbytes`                |
| 6   | Advanced indexing         | `np.take`, `np.put`, `np.ix_`                                               |
| 7   | Curve fitting             | `np.polyfit` / `np.polyval` — fit a line to noisy data                      |
| 8   | Missing data              | `np.nan`, `np.nanmean`, `np.isnan`, `np.where` fill, masked arrays          |
| 9   | Mini task                 | Sensor trend analysis — NaN handling + `polyfit`                            |

---

## Design Principles

### 1. Continues the series' progression

Basics taught the essentials; intermediate taught selection & combination.
Advanced now teaches the _performance and scale_ tools: dtype control, missing
data, curve fitting, and structured data. Every concept builds on earlier
sections.

### 2. Performance is measured, not asserted

Section 4 doesn't just claim vectorization is faster — it **measures** it with
`timeit` and prints the speedup (typically 100x+). This gives the learner
concrete evidence for why NumPy exists.

### 3. Real-world data handling

Missing data (`np.nan`) and masked arrays are taught because real data always
has gaps. The mini task deliberately introduces a NaN and shows how to fit a
trend line around it — exactly the kind of problem a data analyst faces.

### 4. Bridges to pandas

Structured arrays are framed as "the low-level ancestor of a pandas
DataFrame," and missing-data handling mirrors pandas' `NaN` handling. This
ties the NumPy series back to the pandas series the learner may already know.

### 5. Progressive, self-contained sections

Each section is an independent function with its own docstring and docs links.
A learner can run Section 9 (the mini task) without re-reading Sections 1–8,
because each section re-creates the data it needs.

---

## How to run

```powershell
pip install numpy
python numpy_advanced.py
```

Type a number `0`–`9` to run a section, or `q` to quit.
