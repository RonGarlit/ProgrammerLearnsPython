# 🐼 Pandas Basics — `pandas` Library

A single-file, interactive Python lesson that teaches **how to work with
tabular data using pandas** — the powerful data-analysis library. Each section
is its own function, so you can study it in isolation and repeat it as many
times as you like.

> 💡 **How to get the most out of this lesson:** Prefer the **VS Code debugger**
> (see the 🐞 section below) to **step through** the code line by line and watch
> the variables change — it's the best way to really see what each concept does.
> Also **read the comment headers** at the top of each section, and **follow the
> `Docs:` links** in the code for deeper reading and explanations.

> This is the **basics** folder. Intermediate and advanced pandas topics will
> be built out in later folders (`csv_pandas_intermediate`, etc.).

## What you'll learn

| #   | Concept                    | What it shows                                              |
| --- | -------------------------- | ---------------------------------------------------------- |
| 0   | Clean up                   | Deletes the two generated CSV files so you can start fresh |
| 1   | What is pandas?            | `Series` vs `DataFrame`, `pip install pandas`              |
| 2   | Reading with `read_csv`    | CSV → `DataFrame`, automatic type inference & index        |
| 3   | Exploring a DataFrame      | `head`, `tail`, `info`, `describe`, `shape`, `unique`      |
| 4   | Selecting columns & rows   | `df['col']`, `loc` (label), `iloc` (position)              |
| 5   | Filtering by a condition   | Boolean indexing: `df[df['amount'] > 1000]`, `&`, `isin`   |
| 6   | Adding & modifying columns | New columns from existing ones; `apply`                    |
| 7   | Grouping & aggregating     | `groupby` + `sum`/`mean`/`count`, `.agg`, `reset_index`    |
| 8   | Writing with `to_csv`      | DataFrame → CSV, `index=False`                             |
| 9   | Mini task                  | Top product & best region — grouping + aggregating         |

> 💡 **Key idea:** pandas turns a CSV into a **DataFrame** — a labeled 2D table.
> Unlike the built-in `csv` module (which returns strings), pandas **infers
> types** automatically, so `amount` and `quantity` come in as numbers and math
> just works.

---

## ✅ Prerequisites

- **Python 3.9 or newer** (pandas requires a recent Python).
- **pandas** installed:

  ```powershell
  pip install pandas
  ```

- **VS Code** with the **Python extension** (by Microsoft) installed.
  - The extension gives you IntelliSense, the debugger, and the Run button.

Check your Python version and pandas:

```powershell
python --version
python -c "import pandas; print(pandas.__version__)"
```

> If `pip install pandas` fails, try `python -m pip install pandas`.

---

## ▶️ How to run the program

### Option A — Run from the terminal

1. Open a terminal in this folder.
2. Run the script:

   ```powershell
   python pandas_basics.py
   ```

3. You'll see a menu. Type a number `0`–`9` to run a section, or `q` to quit.

> 💡 **Tip:** The script resolves all file paths relative to its own folder, so
> it also works from the project root:
>
> ```powershell
> python csv_pandas_basics/pandas_basics.py
> ```
>
> No matter which folder you run it from, it reads and writes the CSV files in
> `csv_pandas_basics/`.

### Option B — Run from VS Code

1. Open this folder in VS Code.
2. Open `pandas_basics.py`.
3. Click the **Run ▶** button in the top-right corner of the editor
   (or press `Ctrl+F5`).
4. The program runs in the **Terminal** panel. Interact with it there.

> 💡 **Tip:** Because the program reads input with `input()`, always run it in
> the **Terminal** panel — not the "Output" panel, which can't accept typed input.

---

## 🗂️ What the program creates

Running the sections creates small CSV data files **in the same folder**. These
are meant to be inspected — open them in VS Code to see the result:

| Section | File created          | Purpose                                                 |
| ------- | --------------------- | ------------------------------------------------------- |
| 0       | (deletes files)       | Removes `high_sales.csv`, `monthly_summary.csv`         |
| 8       | `high_sales.csv`      | Only the rows where `amount > 1000`, filtered & written |
| 8       | `monthly_summary.csv` | Total sales per month, grouped & aggregated             |

> `sales_data.csv` is the **input** sample data (20 sales records) and is never
> modified. The two output files are plain text — open them in VS Code or Excel.

---

## 🐞 Debugging with VS Code (step-by-step, for beginners)

Debugging lets you **pause** the program at any line, **inspect** the values of
variables, and **step through** the code one line at a time. It's the single
best way to understand _what your code is actually doing_.

### Step 1 — Set a breakpoint

A **breakpoint** is a marker that tells the debugger: _"pause here so I can look
around."_

1. Open `pandas_basics.py`.
2. Click in the **gutter** (the narrow column to the left of the line numbers)
   next to a line of code. A **red dot** appears — that's your breakpoint.

   For example, click next to `return pd.read_csv(filename)` inside
   `read_csv_pandas()`. Watching a `DataFrame` appear is a great way to see how
   a CSV becomes a labeled table.

   - Click the red dot again to remove it.
   - You can set as many breakpoints as you want.

### Step 2: Start the debugger

1. Press **`F5`** (or go to **Run ▸ Start Debugging**).
2. The program starts, runs normally, and **pauses** when it hits your
   breakpoint.

> 💡 **Tip:** If you don't have a `launch.json` yet, VS Code will prompt you to
> create one. Choose **Python** and the **"Python: Current File"** configuration
> with `console: "integratedTerminal"` so `input()` works. Here's the config:

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

When the program pauses, a small toolbar appears at the top of the screen:

| Button        | Shortcut        | What it does                                                               |
| ------------- | --------------- | -------------------------------------------------------------------------- |
| **Continue**  | `F5`            | Run until the next breakpoint (or the end).                                |
| **Step Over** | `F10`           | Run the current line, then pause on the next. Skips _into_ function calls. |
| **Step Into** | `F11`           | Run the current line; if it calls a function, jump _inside_ that function. |
| **Step Out**  | `Shift+F11`     | Finish the current function and pause back at the caller.                  |
| **Restart**   | `Ctrl+Shift+F5` | Start the debug session over.                                              |
| **Stop**      | `Shift+F5`      | End the debug session.                                                     |

### Step 4: Inspect variables

While paused, look at the **VARIABLES** panel (usually on the left, or in the
**Run and Debug** view):

- **Locals** — variables in the current function (like the `df` DataFrame).
- **Globals** — variables defined at the top level of the module.

You can also **hover** your mouse over any variable in the editor to see its
current value in a tooltip.

### Step 5 — Use the Debug Console

The **DEBUG CONSOLE** panel lets you type Python expressions and evaluate them
_right now_, using the current state of the program.

For example, while paused after reading `sales_data.csv`, type:

```python
df['amount'].mean()
```

and press Enter — it returns the average sale amount.

### Step 6 — Walk through the tutorial

Here's a suggested debugging session to learn the flow:

1. Set a breakpoint on the first line of `main()`.
2. Press `F5` to start.
3. Use **Step Over** (`F10`) to watch the menu print.
4. When the program asks for input, type `2` in the terminal and press Enter.
5. The debugger now pauses inside `section_reading()`.
6. Use **Step Into** (`F11`) to follow the call into `read_csv_pandas()`.
7. Step through and watch the `df` DataFrame appear in the **VARIABLES** panel.

> 💡 **Tip:** When the program is waiting for `input()`, the debugger is _not_
> paused — it's running normally. Type your answer in the terminal, then the
> debugger will pause again at the next breakpoint.

---

## 🧠 Common gotchas

- **`ModuleNotFoundError: No module named 'pandas'`?** pandas isn't installed.
  Run `pip install pandas` (or `python -m pip install pandas`).
- **Breakpoint not hit?** Make sure the file you're debugging is the one with
  the breakpoint, and that you started with **Run ▸ Start Debugging** (`F5`),
  not just **Run** (`Ctrl+F5`). `Ctrl+F5` runs _without_ debugging and ignores
  breakpoints.
- **Can't type input?** The program reads from the **Terminal** panel. If you're
  looking at the Output panel, switch to Terminal.
- **`SettingWithCopyWarning`?** This is a pandas warning about chained
  assignments. In this lesson we modify the DataFrame directly, so it's safe —
  but it's good to know the warning exists.
- **My CSV looks wrong in Excel?** That's Excel's number formatting, not the
  file. Open the `.csv` in a plain-text editor (or VS Code) to see the real
  saved data.
- **Where did my data go?** Section 8 overwrites `high_sales.csv` and
  `monthly_summary.csv` each run. Use option **0** to delete them at once.

---

## 🧭 Project structure

```
csv_pandas_basics/            (this folder)
├── pandas_basics.py          # the tutorial program
├── sales_data.csv            # sample input data (20 sales records)
├── high_sales.csv            # generated by Section 8 (filtered rows)
├── monthly_summary.csv       # generated by Section 8 (grouped summary)
├── Project_Objective.md      # design notes & concept breakdown
└── README.md                 # this file
```

---

## 🚀 Progressing to the next steps

- Try adding a **Section 10** that sorts the DataFrame by `amount` before
  writing (`df.sort_values('amount', ascending=False)`).
- Add a `department` or `category` column to `sales_data.csv` and re-run the
  grouping sections.
- When you're comfortable here, move on to the **`csv_pandas_intermediate`**
  folder, which introduces merging, pivoting, handling missing data, and more
  advanced pandas techniques.
