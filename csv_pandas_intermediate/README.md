# 📊 Pandas Intermediate — Data Manipulation

A single-file, interactive Python lesson that teaches **intermediate pandas
data manipulation**. Building on the `csv_pandas_basics` folder, each section
is its own function, so you can study it in isolation and repeat it as many
times as you like.

> 💡 **How to get the most out of this lesson:** Prefer the **VS Code debugger**
> (see the 🐞 section below) to **step through** the code line by line and watch
> the variables change — it's the best way to really see what each concept does.
> Also **read the comment headers** at the top of each section, and **follow the
> `Docs:` links** in the code for deeper reading and explanations.

> ✅ **Prerequisite:** Complete the **`csv_pandas_basics`** folder first. This
> lesson assumes you know `read_csv`, `groupby` + `sum`, filtering, and
> `to_csv`.

## What you'll learn

| #   | Concept                     | What it shows                                            |
| --- | --------------------------- | -------------------------------------------------------- |
| 0   | Clean up                    | Deletes the generated CSV files so you can start fresh   |
| 1   | Handling missing values     | `isna()`, `dropna()`, `fillna(0)`, mean imputation       |
| 2   | Sorting & ranking           | `sort_values` (single & multi-column), `rank`            |
| 3   | Working with dates & times  | `to_datetime`, `.dt.year/quarter/day_name`, date math    |
| 4   | Merging & joining           | `pd.merge` inner vs left joins on a key column           |
| 5   | Multi-level grouping & pivot| `groupby` on two columns; `pivot_table` + `aggfunc`      |
| 6   | Vectorized & `.apply()`     | Whole-column ops vs row-wise custom functions            |
| 7   | String operations           | `.str.lower/contains/startswith/replace`                 |
| 8   | Writing enriched results    | Persist merged + computed columns and a pivot summary    |
| 9   | Mini task                   | Most profitable product per region                       |

> 💡 **Key idea:** Real data is messy — it has **missing cells**, needs
> **sorting**, combines across **multiple tables**, and includes **dates and
> text**. This lesson gives you the toolkit to handle all of that.

---

## ✅ Prerequisites

- **Python 3.9 or newer** and **pandas** installed:

  ```powershell
  pip install pandas
  ```

- **Complete `csv_pandas_basics` first** (this builds directly on it).
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
   python pandas_intermediate.py
   ```

3. You'll see a menu. Type a number `0`–`9` to run a section, or `q` to quit.

> 💡 **Tip:** The script resolves all file paths relative to its own folder, so
> it also works from the project root:
>
> ```powershell
> python csv_pandas_intermediate/pandas_intermediate.py
> ```

### Option B — Run from VS Code

1. Open this folder in VS Code.
2. Open `pandas_intermediate.py`.
3. Click the **Run ▶** button in the top-right corner of the editor
   (or press `Ctrl+F5`).
4. The program runs in the **Terminal** panel. Interact with it there.

> 💡 **Tip:** Because the program reads input with `input()`, always run it in
> the **Terminal** panel — not the "Output" panel, which can't accept typed input.

---

## 🗂️ What the program creates

Running the sections creates small CSV data files **in the same folder**. These
are meant to be inspected — open them in VS Code to see the result:

| Section | File created             | Purpose                                                       |
| ------- | ------------------------ | ------------------------------------------------------------- |
| 0       | (deletes files)          | Removes `enriched_sales.csv`, `pivot_summary.csv`             |
| 8       | `enriched_sales.csv`     | Sales merged with product info + computed `profit` column     |
| 8       | `pivot_summary.csv`      | Pivot table: total amount per (region, product)               |

> `sales_data.csv` and `product_info.csv` are the **input** files and are never
> modified. The two output files are plain text — open them in VS Code or Excel.

---

## 🐞 Debugging with VS Code (step-by-step, for beginners)

Debugging lets you **pause** the program at any line, **inspect** the values of
variables, and **step through** the code one line at a time.

### Step 1 — Set a breakpoint

1. Open `pandas_intermediate.py`.
2. Click in the **gutter** (the narrow column to the left of the line numbers)
   next to a line of code. A **red dot** appears.

   For example, click next to `df.isna().sum()` inside
   `section_missing_values()`. Watching the missing-data counts appear is a
   great way to understand NaNs.

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

While paused, look at the **VARIABLES** panel for **Locals** (like the
`merged` DataFrame) and **Globals**.

In the **DEBUG CONSOLE**, type expressions to evaluate them right now, e.g.
after Section 4:

```python
merged['profit'].max()
```

### Step 5 — Walk through the tutorial

Suggested session: set a breakpoint at the top of `main()`, press `F5`, then
type `4` to run the merge section. Step Into `section_merging()` and watch the
`merged` DataFrame combine the two tables.

---

## 🧠 Common gotchas

- **`ModuleNotFoundError: No module named 'pandas'`?** Run
  `pip install pandas` (or `python -m pip install pandas`).
- **NaN shows up as `NaN`/`nan`?** That's pandas' marker for a missing value.
  Use `isna()`, `dropna()`, or `fillna()` to handle it.
- **`'.dt' accessor` error?** You called `.dt` on a column that is still text.
  Convert it first with `pd.to_datetime()`.
- **Merge returns way more rows than expected?** One of the join keys has
  duplicates. Pass `validate="many_to_one"` (as this lesson does) to catch it.
- **`SettingWithCopyWarning`?** A pandas warning about chained assignments.
  Use `.copy()` (as Section 1 does) to be safe.
- **Breakpoint not hit?** Make sure the file you're debugging is the one with
  the breakpoint, and start with **Run ▸ Start Debugging** (`F5`), not **Run**
  (`Ctrl+F5`).
- **Can't type input?** Run in the **Terminal** panel, not the Output panel.

---

## 🧭 Project structure

```
csv_pandas_intermediate/      (this folder)
├── pandas_intermediate.py    # the tutorial program
├── sales_data.csv            # sample sales data (20 rows, includes NaNs)
├── product_info.csv          # product lookup table (category / supplier / cost)
├── enriched_sales.csv        # generated by Section 8 (merged + profit)
├── pivot_summary.csv         # generated by Section 8 (pivot summary)
├── Project_Objective.md      # design notes & concept breakdown
└── README.md                 # this file
```

---

## 🚀 Progressing to the next steps

- Try adding a **Section 10** that handles duplicate rows with `drop_duplicates()`.
- Filter `sales_data.csv` to a specific supplier from the merged table and
  write only that subset.
- When you're comfortable here, move on to the **`csv_pandas_advanced`**
  folder, which introduces time-series resampling, window functions,
  `MultiIndex`, `stack`/`unstack` reshaping, and larger-scale data techniques.