# 🔢 NumPy Intermediate with Python

Below is a complete, runnable Python application designed to take a learner
**from basics to intermediate-level NumPy**. Building on the `numpy_basics`
folder, this interactive "study session" covers the tools used for **selecting
and combining** numerical data: reshaping, stacking, boolean masking, fancy
indexing, broadcasting, random numbers, linear algebra, and advanced
aggregation — all with real working examples, heavy commenting, and links to
the official NumPy documentation.

> This folder covers **intermediate NumPy**. It is the second NumPy lesson in
> this series (after `numpy_basics`, before `numpy_advanced`).

---

## Code Analysis Summary

- **Purpose:** A single-file interactive teaching tool that demonstrates
  intermediate NumPy techniques on a 15-row sensor dataset.
- **Concepts covered:** `reshape`/`ravel`/`transpose`, `concatenate`/
  `vstack`/`hstack`/`split`, boolean masking, fancy indexing, broadcasting,
  `np.random` (seeded & reproducible), linear algebra (`dot`, `@`, `inv`),
  advanced aggregation (`percentile`, `unique`, `where`, `any`/`all`), and a
  capstone mini task.
- **Style:** Heavily commented so each construct is explained _where it
  appears_; safe for learners continuing from basics.
- **Notable patterns:** Reuses the `data_path()` helper for folder-relative
  paths (works from any folder); a `main()` menu loop and the classic
  `if __name__ == "__main__"` guard. This lesson is **predominantly
  in-memory** — it writes no output files, but includes a cleanup routine for
  consistency.

---

## The Concepts (one per section)

| #   | Concept                 | What it shows                                                      |
| --- | ----------------------- | ------------------------------------------------------------------ |
| 1   | Reshaping & transposing | `reshape`, `ravel`, `transpose`/`.T`; views vs copies              |
| 2   | Stacking & splitting    | `concatenate`, `vstack`, `hstack`, `split`                         |
| 3   | Boolean masking         | Filter with conditions; `&`/`\|`; count & replace with masks       |
| 4   | Fancy indexing          | Select with arrays of indices; `np.where`                          |
| 5   | Broadcasting            | How arrays of different shapes work together (scalar, row, column) |
| 6   | Random numbers          | `np.random.default_rng`, seeds, distributions, simulations         |
| 7   | Linear algebra          | `np.dot`, `@`/`matmul`, transpose, `np.linalg.inv`                 |
| 8   | Advanced aggregation    | `percentile`, `median`, `unique`, `where`, `any`/`all`             |
| 9   | Mini task               | Sensor anomaly detection — masking + aggregation                   |

---

## Design Principles

### 1. Continues the series' progression

Basics taught the essentials (creating, indexing, vectorized math). This
lesson teaches the _selection and combination_ tools: reshaping, stacking,
masking, fancy indexing, and broadcasting. Every concept builds on earlier
sections.

### 2. Selection is the theme

The heart of intermediate NumPy is **selecting the data you want**. Boolean
masks and fancy indexing are the two ways to do that, and both are taught with
real comparisons to pandas filtering (which the learner may already know).

### 3. Reproducibility from the start

Random numbers are introduced with a **seed** (`np.random.default_rng(42)`),
so every learner sees the same "random" output. This is essential for a
tutorial — the results are predictable and debuggable.

### 4. Progressive, self-contained sections

Each section is an independent function with its own docstring and docs links.
A learner can run Section 9 (the mini task) without re-reading Sections 1–8,
because each section re-creates the data it needs.

---

## How to run

```powershell
pip install numpy
python numpy_intermediate.py
```

Type a number `0`–`9` to run a section, or `q` to quit.
