# 🚀 Pandas Advanced — Hierarchical, Time-Based, and Large-Scale Data

A single-file, interactive Python lesson that teaches **advanced pandas**. This
is the third and final step in the pandas series, building directly on the
`csv_pandas_intermediate` folder. Each section is its own function, so you can
study it in isolation and repeat it as many times as you like.

> 💡 **How to get the most out of this lesson:** Prefer the **VS Code debugger**
> (see the 🐞 section below) to **step through** the code line by line and watch
> the variables change — it's the best way to really see what each concept does.
> Also **read the comment headers** at the top of each section, and **follow the
> `Docs:` links** in the code for deeper reading and explanations.

> ✅ **Prerequisites:** Complete **`csv_pandas_basics`** and
> **`csv_pandas_intermediate`** first. This lesson assumes you know
> `groupby`, merging, dates, and pivot tables.

## What you'll learn

| #   | Concept                   | What it shows                                                     |
| --- | ------------------------- | ----------------------------------------------------------------- |
| 0   | Clean up                  | Removes the optional output file so you can start fresh           |
| 1   | MultiIndex                | Hierarchical labels; `set_index`, `.loc` tuples, `.xs`            |
| 2   | `stack` / `unstack`       | Pivot index levels between rows and columns (long ↔ wide)         |
| 3   | `melt` (wide → long)      | Unpivot a wide table into long format                             |
| 4   | Categorical data          | `astype('category')`; memory savings; ordered categories          |
| 5   | Window functions          | `.rolling()` moving average/sum; `.expanding()` running totals    |
| 6   | Time-series resampling    | `resample('ME'/'W')` downsampling; upsampling with `ffill()`      |
| 7   | Function pipelines        | `.pipe()` composes functions into a readable data pipeline        |
| 8   | Advanced aggregation      | Named aggs, custom callables, mixed per-column `agg`              |
| 9   | Mini task                 | Weekly profit & 4-week rolling report                             |

> 💡 **Key idea:** Advanced pandas is about **structure and time**. You learn
> to reshape data (`stack`/`unstack`/`melt`), label it hierarchically
> (`MultiIndex`), make it fast (`category`), and analyze it over time
> (`rolling`, `expanding`, `resample`).

---

## ✅ Prerequisites

- **Python 3.9 or newer** and **pandas** installed:

  ```powershell
  pip install pandas
  ```

- **Complete `csv_pandas_basics` and `csv_pandas_intermediate` first.**
- **VS Code** with the **Python extension** (by Microsoft) installed.

Check your Python version and pandas:

```powershell
python --version
python -c "import pandas; print(pandas.__version__)"
```

---

## ▶️ How to run the program

### Option A — Run from the terminal

1. Open a terminal in this folder.
2. Run the script:

   ```powershell
   python pandas_advanced.py
   ```

3. You'll see a menu. Type a number `0`–`9` to run a section, or `q` to quit.

> 💡 **Tip:** The script resolves all file paths relative to its own folder, so
> it also works from the project root:
>
> ```powershell
> python csv_pandas_advanced/pandas_advanced.py
> ```

### Option B — Run from VS Code

1. Open this folder in VS Code.
2. Open `pandas_advanced.py`.
3. Click the **Run ▶** button in the top-right corner of the editor
   (or press `Ctrl+F5`).
4. The program runs in the **Terminal** panel. Interact with it there.

> 💡 **Tip:** Because the program reads input with `input()`, always run it in
> the **Terminal** panel — not the "Output" panel, which can't accept typed input.

---

## 🗂️ What the program creates

This lesson is **predominantly in-memory** — most sections build new DataFrames
without writing files. The only output is optional:

| Section | File created         | Purpose                                                  |
| ------- | -------------------- | -------------------------------------------------------- |
| 0       | (deletes files)      | Removes `pipeline_output.csv`                            |
| —       | `pipeline_output.csv`| Optional export produced by the pipeline section         |

> `sales_data.csv` is the **input** file (50 daily sales records) and is never
> modified. `pipeline_output.csv` is optional and ignored by git.

---

## 🐞 Debugging with VS Code (step-by-step, for beginners)

Debugging lets you **pause** the program at any line, **inspect** the values of
variables, and **step through** the code one line at a time.

### Step 1 — Set a breakpoint

1. Open `pandas_advanced.py`.
2. Click in the **gutter** (the narrow column to the left of the line numbers)
   next to a line of code. A **red dot** appears.

   For example, click next to the `.rolling(window=7).mean()` call inside
   `section_window()`. Watching the rolling window compute one row at a time
   is a great way to understand moving averages.

### Step 2: Start the debugger

1. Press **`F5`** (or go to **Run ▸ Start Debugging**).
2. The program starts and **pauses** when it hits your breakpoint.

> 💡 **Tip:** If you don't have a `launch.json` yet, VS Code will prompt you to
> create one. Choose **Python** and the **"Python: Current File"** configuration
> with `console: "integratedTerminal"` so `input()` works.

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    }
  ]
}
```

### Step 3: Use the debugging toolbar

| Button        | Shortcut        | What it does                                                               |
| ------------- | --------------- | -------------------------------------------------------------------------- |
| **Continue**  | `F5`            | Run until the next breakpoint (or the end).                                |
| **Step Over** | `F10`           | Run the current line, then pause on the next. Skips _into_ function calls. |
| **Step Into** | `F11`           | Run the current line; if it calls a function, jump _inside_ that function. |
| **Step Out**  | `Shift+F11`     | Finish the current function and pause back at the caller.                  |
| **Restart**   | `Ctrl+Shift+F5` | Start the debug session over.                                              |
| **Stop**      | `Shift+F5`      | End the debug session.                                                     |

### Step 4: Inspect variables & use the Debug Console

While paused, look at the **VARIABLES** panel for **Locals** (like the `rolling`
Series) and **Globals**.

In the **DEBUG CONSOLE**, type expressions to evaluate them right now, e.g.
after Section 6:

```python
monthly
```

### Step 5 — Walk through the tutorial

Suggested session: set a breakpoint at the top of `main()`, press `F5`, then
type `6` to run the resampling section. Step Into `section_resample()` and
watch `daily.resample('ME').sum()` aggregate days into months.

---

## 🧠 Common gotchas

- **`ModuleNotFoundError: No module named 'pandas'`?** Run
  `pip install pandas` (or `python -m pip install pandas`).
- **`PerformanceWarning: indexing past lexsort depth`?** The MultiIndex wasn't
  sorted. Call `.sort_index()` on it (this lesson does) before slicing.
- **`.dt` accessor error?** The column is still text. Convert with
  `pd.to_datetime()` first.
- **Resample error / `ME` not recognized?** On older pandas use `'M'` instead
  of `'ME'`. `'ME'` is correct for pandas ≥ 2.2.
- **`SettingWithCopyWarning`?** Use `.copy()` when modifying a slice.
- **Breakpoint not hit?** Make sure the file you're debugging is the one with
  the breakpoint, and start with **Run ▸ Start Debugging** (`F5`).

---

## 🧭 Project structure

```
csv_pandas_advanced/          (this folder)
├── pandas_advanced.py        # the tutorial program
├── sales_data.csv            # sample input data (50 daily records, 6 months)
├── pipeline_output.csv       # optional output (produced by section 7)
├── Project_Objective.md      # design notes & concept breakdown
└── README.md                 # this file
```

---

## 🚀 Where to go next

The pandas series is now complete (basics → intermediate → advanced). To keep
growing:

- **Plotting** — combine pandas with `matplotlib` or `plotly` to visualize
  these DataFrames (`df.plot()`).
- **Performance** — explore `numba`, chunked reading, and `dask` for
  out-of-memory datasets.
- **Data pipelines** — apply the `.pipe()` pattern to build a full
  extract-transform-load (ETL) workflow.