# 🚀 Pandas Advanced with Python

Below is a complete, runnable Python application designed to take a learner
**from intermediate to advanced-level pandas**. Building on the
`csv_pandas_intermediate` folder, this interactive "study session" covers the
tools used for **large, complex, hierarchical, and time-based data**: MultiIndex
labels, reshaping (`stack`/`unstack`/`melt`), categorical dtype, window
functions, time-series resampling, function pipelines, and advanced
aggregation — all with real working examples, heavy commenting, and links to
the official pandas documentation.

> This folder covers **advanced pandas**. It is the final pandas lesson in this
> series (after `csv_pandas_basics` and `csv_pandas_intermediate`).

---

## Code Analysis Summary

- **Purpose:** A single-file interactive teaching tool that demonstrates
  advanced pandas techniques on a 50-row daily sales dataset spanning six months.
- **Concepts covered:** MultiIndex (`set_index`, `.loc` tuples, `.xs`),
  `stack`/`unstack`, `melt` (wide→long), categorical dtype & memory savings,
  `.rolling()` / `.expanding()` window functions, time-series resampling
  (downsample & upsample), `.pipe()` function pipelines, named/custom/mixed
  `agg`, and a capstone mini task.
- **Style:** Heavily commented so each construct is explained *where it
  appears*; safe for learners continuing from intermediate.
- **Notable patterns:** Reuses the `read_csv_pandas()` / `write_csv_pandas()`
  helper convention; `data_path()` for folder-relative paths (works from any
  folder); a `main()` menu loop and the classic `if __name__ == "__main__"`
  guard. This lesson is **predominantly in-memory** — it does not require
  writing many output files, but includes a cleanup routine for consistency.

---

## The Concepts (one per section)

| # | Concept                   | What it shows                                                                  |
|---|---------------------------|--------------------------------------------------------------------------------|
| 1 | MultiIndex                | Hierarchical row/column labels; `set_index`, `.loc` tuples, `.xs`              |
| 2 | `stack` / `unstack`       | Pivot index levels between rows and columns (long ↔ wide)                      |
| 3 | `melt` (wide → long)      | Unpivot a wide table into long format with `id_vars`, `var_name`               |
| 4 | Categorical data          | `astype('category')` memory savings; ordering categories                       |
| 5 | Window functions          | `.rolling()` moving average / sum; `.expanding()` running totals               |
| 6 | Time-series resampling    | `resample('ME'/'W')` downsampling; upsampling with `ffill()`                   |
| 7 | Function pipelines        | `.pipe()` composes small transformation functions into a readable pipeline     |
| 8 | Advanced aggregation      | Named aggs, custom callables, and mixed per-column aggregations via `agg()`    |
| 9 | Mini task                 | Weekly profit & 4-week rolling report — combines everything                    |

---

## Design Principles

### 1. Continues the series' progression
Basics taught the essentials; intermediate taught real-world data handling
(missing values, dates, merges, pivots). Advanced now teaches the *structure*
pandas can impose: hierarchical labels, reshapes, categories, windows, and
time-series frequency. Every concept builds on earlier sections.

### 2. Time-based and relational data
The sample data spans **six months of daily sales** across 4 regions and 4
products. This is deliberately richer than the earlier folders so the
time-series resampling and rolling-window sections are meaningful.

### 3. Predominantly in-memory
Advanced pandas is often about *analysis*, not file I/O. Most sections produce
new DataFrames in memory rather than writing files. This mirrors how advanced
pandas is used in practice and keeps the folder clean.

### 4. One-concept-per-section
Each section is its own function so a learner can study it in isolation and
re-run any part on demand — consistent with every other folder.

### 5. Progression from easy → applied
- Sections 1–3 reshape and restructure data (indexes, stack/unstack, melt).
- Sections 4–6 handle scale and time (categories, windows, resampling).
- Sections 7–8 compose reusable pipelines and flexible aggregations.
- Section 9 ties everything together with a realistic reporting task.

### 6. Good-practice idioms throughout
Sorting the MultiIndex before slicing (avoids `PerformanceWarning`), using
`pd.to_datetime`, `ffill()` for gaps, and `.pipe()` for readability — each
teaches the professional way to use pandas.

---

## Files in this folder

```
csv_pandas_advanced/
├── pandas_advanced.py  # the tutorial program (menu-driven)
├── sales_data.csv      # sample data (50 daily sales records, 6 months)
├── pipeline_output.csv # optional output (see Section 7 / cleanup)
├── Project_Objective.md # design notes & concept breakdown (this file)
└── README.md           # how to run & debug
```

> `pipeline_output.csv` is optional and can be recreated on demand; it is
> ignored by `.gitignore`.

---

## Getting Started

```powershell
pip install pandas
python pandas_advanced.py
```

Type a number `1`–`9` to run a section, or `q` to quit.

See `README.md` for full running and debugging instructions.